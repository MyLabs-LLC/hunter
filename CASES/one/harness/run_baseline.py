from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import mlflow
import numpy as np
from sklearn.model_selection import train_test_split

from model_pipeline import compare, tracking
from ra_harness import build_models, evaluate_model, load_geo_series_matrix


ROOT = Path(__file__).resolve().parent


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _metric_payload(result: object) -> dict[str, float]:
    return {key: float(value) for key, value in result.scalar_metrics().items()}


def main() -> None:
    config = json.loads((ROOT / "config.json").read_text())
    matrix_path = ROOT / config["dataset"]["matrix_path"]
    if not matrix_path.exists():
        raise FileNotFoundError(f"download the configured GEO matrix first: {matrix_path}")

    series = load_geo_series_matrix(matrix_path)
    label_col = "response_to_anti-tnf_therapy"
    raw_labels = series.metadata[label_col].str.upper()
    positive = set(config["dataset"]["positive_labels"])
    negative = set(config["dataset"]["negative_labels"])
    selected = raw_labels.isin(positive | negative)
    X = series.expression.loc[selected]
    y = raw_labels.loc[selected].isin(positive).astype(int)

    eval_config = config["evaluation"]
    seed = int(eval_config["split_seed"])
    sample_ids = np.asarray(X.index)
    train_ids, holdout_ids = train_test_split(
        sample_ids,
        test_size=float(eval_config["holdout_fraction"]),
        random_state=seed,
        stratify=y.loc[sample_ids],
    )
    X_train, y_train = X.loc[train_ids], y.loc[train_ids]
    X_holdout, y_holdout = X.loc[holdout_ids], y.loc[holdout_ids]

    checksum = _digest(matrix_path)
    dataset_meta = {
        "name": config["dataset"]["accession"],
        "digest": checksum,
        "platform": config["dataset"]["platform"],
    }
    manifest = {
        "accession": config["dataset"]["accession"],
        "source_url": config["dataset"]["source_url"],
        "sha256": checksum,
        "n_total": int(len(series.expression)),
        "n_labeled": int(len(X)),
        "class_counts": {str(key): int(value) for key, value in y.value_counts().sort_index().items()},
        "n_probes": int(X.shape[1]),
        "held_in_sample_ids": sorted(train_ids.tolist()),
        "sealed_holdout_sample_ids": sorted(holdout_ids.tolist()),
        "split_seed": seed,
    }
    (ROOT / "data" / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    mlruns = ROOT / "mlruns"
    os.environ["MLFLOW_TRACKING_URI"] = mlruns.resolve().as_uri()
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])

    results: dict[str, dict[str, object]] = {}
    held_out_results: dict[str, object] = {}
    with tracking.pipeline_run(config["project"], experiment=config["experiment"]):
        with tracking.pipeline_stage("setup"):
            tracking.log_pipeline_setup(project=str(ROOT))
            mlflow.log_dict(manifest, "dataset_manifest.json")

        with tracking.pipeline_stage("eval"):
            for model_name, estimator in build_models(
                seed=seed,
                threads=int(config["compute"]["threads"]),
            ).items():
                with tracking.evaluation_run(model_name, description=f"CPU baseline: {model_name}"):
                    outcome = evaluate_model(
                        estimator,
                        X_train,
                        y_train,
                        X_holdout,
                        y_holdout,
                        cv_folds=int(eval_config["cv_folds"]),
                        seed=seed,
                        n_resamples=int(eval_config["bootstrap_resamples"]),
                        confidence=float(eval_config["confidence"]),
                        dataset=dataset_meta,
                        model_name=model_name,
                    )
                    tracking.log_evaluation(outcome.held_in, prefix="held_in")
                    tracking.log_evaluation(outcome.held_out, prefix="held_out")
                    results[model_name] = {
                        "held_in": _metric_payload(outcome.held_in),
                        "held_out": _metric_payload(outcome.held_out),
                    }
                    held_out_results[model_name] = outcome.held_out

    report = {
        "project": config["project"],
        "primary_metric": eval_config["primary_metric"],
        "dataset": manifest,
        "models": results,
    }
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)
    (reports_dir / "baseline.json").write_text(json.dumps(report, indent=2) + "\n")
    (reports_dir / "baseline.md").write_text(
        "# Baseline sealed-holdout comparison\n\n" + compare(held_out_results) + "\n"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
