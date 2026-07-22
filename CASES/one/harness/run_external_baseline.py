from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import mlflow

from model_pipeline import compare, tracking
from ra_harness import (
    build_models,
    evaluate_model,
    load_geo_supplementary_counts,
    log_counts_per_million,
)


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
    config = json.loads((ROOT / "config_gse129705.json").read_text())
    dataset_config = config["dataset"]
    metadata_path = ROOT / dataset_config["metadata_path"]
    counts_path = ROOT / dataset_config["counts_path"]
    for path in (metadata_path, counts_path):
        if not path.exists():
            raise FileNotFoundError(f"download the configured GEO file first: {path}")

    series = load_geo_supplementary_counts(metadata_path, counts_path)
    metadata = series.metadata
    labels = metadata["eular_response"].str.upper()
    positive = set(dataset_config["positive_labels"])
    negative = set(dataset_config["negative_labels"])
    selected = (
        metadata["visit_time"].eq(dataset_config["visit"])
        & labels.isin(positive | negative)
    )
    metadata = metadata.loc[selected]
    X = log_counts_per_million(series.expression.loc[selected])
    y = labels.loc[selected].isin(positive).astype(int)

    held_in_cohort = dataset_config["held_in_cohort"]
    sealed_cohort = dataset_config["sealed_cohort"]
    held_in_ids = metadata.index[metadata["cohort"].eq(held_in_cohort)]
    sealed_ids = metadata.index[metadata["cohort"].eq(sealed_cohort)]
    if not len(held_in_ids) or not len(sealed_ids):
        raise ValueError("configured held-in or sealed cohort is empty")
    if set(metadata.loc[held_in_ids, "subject_id"]) & set(
        metadata.loc[sealed_ids, "subject_id"]
    ):
        raise ValueError("subjects overlap between held-in and sealed cohorts")
    if metadata.loc[held_in_ids, "subject_id"].duplicated().any():
        raise ValueError("held-in baseline cohort contains duplicate subjects")
    if metadata.loc[sealed_ids, "subject_id"].duplicated().any():
        raise ValueError("sealed baseline cohort contains duplicate subjects")

    X_train, y_train = X.loc[held_in_ids], y.loc[held_in_ids]
    X_holdout, y_holdout = X.loc[sealed_ids], y.loc[sealed_ids]
    eval_config = config["evaluation"]
    seed = int(eval_config["split_seed"])
    checksums = {
        "metadata_sha256": _digest(metadata_path),
        "counts_sha256": _digest(counts_path),
    }
    dataset_meta = {
        "name": dataset_config["accession"],
        "digest": checksums["counts_sha256"],
        "platform": dataset_config["platform"],
    }
    manifest = {
        "accession": dataset_config["accession"],
        "source_urls": [dataset_config["metadata_url"], dataset_config["counts_url"]],
        **checksums,
        "normalization": "per-sample log2(CPM + 1)",
        "visit": dataset_config["visit"],
        "n_source_samples": int(len(series.expression)),
        "n_labeled_baseline": int(len(X)),
        "n_genes": int(X.shape[1]),
        "held_in": {
            "cohort": held_in_cohort,
            "sample_ids": sorted(held_in_ids.tolist()),
            "class_counts": {
                str(key): int(value)
                for key, value in y_train.value_counts().sort_index().items()
            },
        },
        "sealed_holdout": {
            "cohort": sealed_cohort,
            "sample_ids": sorted(sealed_ids.tolist()),
            "class_counts": {
                str(key): int(value)
                for key, value in y_holdout.value_counts().sort_index().items()
            },
        },
        "cv_seed": seed,
    }
    manifest_path = ROOT / "data" / "gse129705_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

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
                with tracking.evaluation_run(
                    model_name,
                    description=f"CPU external-cohort baseline: {model_name}",
                ):
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
    (reports_dir / "gse129705_baseline.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    (reports_dir / "gse129705_baseline.md").write_text(
        "# GSE129705 external-cohort comparison\n\n"
        + compare(held_out_results)
        + "\n"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
