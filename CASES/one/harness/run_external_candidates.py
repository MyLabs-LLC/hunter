from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import mlflow

from model_pipeline import tracking
from ra_harness import (
    build_logistic_model,
    evaluate_model,
    load_geo_supplementary_counts,
    log_counts_per_million,
)


ROOT = Path(__file__).resolve().parent
PRIMARY = "roc_auc"

CANDIDATES = [
    {
        "id": "round3_a_logistic_selector_20",
        "change": {"selector_k": 20},
        "mechanism": "reduce high-dimensional coefficient and selection variance",
        "surface": "train-fold feature count",
        "expected_effect": "retain a smaller, more stable baseline transcript set",
        "regression_risk": "discard a diffuse cell-composition signal",
    },
    {
        "id": "round3_b_logistic_selector_100",
        "change": {"selector_k": 100},
        "mechanism": "capture a more distributed whole-blood response signature",
        "surface": "train-fold feature count",
        "expected_effect": "retain complementary weak expression effects",
        "regression_risk": "increase coefficient variance in the 34-person cohort",
    },
    {
        "id": "round3_c_logistic_c_0_1",
        "change": {"regularization_c": 0.1},
        "mechanism": "shrink unstable logistic coefficients",
        "surface": "logistic L2 regularization strength",
        "expected_effect": "improve ranking stability and external calibration",
        "regression_risk": "overshrink the already weak response signal",
    },
]


def _metrics(result: Any) -> dict[str, float]:
    return {key: float(value) for key, value in result.scalar_metrics().items()}


def _accept(delta_in: float, delta_ho: float) -> bool:
    return delta_in >= 0.0 and delta_ho >= 0.0 and max(delta_in, delta_ho) > 0.0


def main() -> None:
    config = json.loads((ROOT / "config_gse129705.json").read_text())
    manifest = json.loads((ROOT / "data" / "gse129705_manifest.json").read_text())
    baseline = json.loads((ROOT / "reports" / "gse129705_baseline.json").read_text())
    dataset_config = config["dataset"]
    series = load_geo_supplementary_counts(
        ROOT / dataset_config["metadata_path"],
        ROOT / dataset_config["counts_path"],
    )

    metadata = series.metadata
    labels = metadata["eular_response"].str.upper()
    selected = (
        metadata["visit_time"].eq(dataset_config["visit"])
        & labels.isin(
            set(dataset_config["positive_labels"])
            | set(dataset_config["negative_labels"])
        )
    )
    X = log_counts_per_million(series.expression.loc[selected])
    y = labels.loc[selected].isin(set(dataset_config["positive_labels"])).astype(int)
    train_ids = manifest["held_in"]["sample_ids"]
    holdout_ids = manifest["sealed_holdout"]["sample_ids"]
    X_train, y_train = X.loc[train_ids], y.loc[train_ids]
    X_holdout, y_holdout = X.loc[holdout_ids], y.loc[holdout_ids]

    seed = int(config["evaluation"]["split_seed"])
    dataset_meta = {
        "name": dataset_config["accession"],
        "digest": manifest["counts_sha256"],
        "platform": dataset_config["platform"],
    }
    base_in = float(baseline["models"]["logistic_regression"]["held_in"][PRIMARY])
    base_ho = float(baseline["models"]["logistic_regression"]["held_out"][PRIMARY])
    reports: list[dict[str, Any]] = []

    os.environ["MLFLOW_TRACKING_URI"] = (ROOT / "mlruns").resolve().as_uri()
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
    with tracking.pipeline_run(
        f"{config['project']}-round3",
        experiment=config["experiment"],
        tags={"baseline_model": "logistic_regression", "candidate_count": len(CANDIDATES)},
    ):
        with tracking.pipeline_stage("tune"):
            for candidate in CANDIDATES:
                params = {"selector_k": 50, "regularization_c": 1.0}
                params.update(candidate["change"])
                with tracking.evaluation_run(
                    candidate["id"],
                    description=candidate["mechanism"],
                ):
                    mlflow.log_params(params)
                    outcome = evaluate_model(
                        build_logistic_model(seed=seed, **params),
                        X_train,
                        y_train,
                        X_holdout,
                        y_holdout,
                        cv_folds=int(config["evaluation"]["cv_folds"]),
                        seed=seed,
                        n_resamples=int(config["evaluation"]["bootstrap_resamples"]),
                        confidence=float(config["evaluation"]["confidence"]),
                        dataset=dataset_meta,
                        model_name=candidate["id"],
                    )
                    tracking.log_evaluation(outcome.held_in, prefix="held_in")
                    tracking.log_evaluation(outcome.held_out, prefix="held_out")

                    candidate_in = float(outcome.held_in.value(PRIMARY))
                    candidate_ho = float(outcome.held_out.value(PRIMARY))
                    delta_in = candidate_in - base_in
                    delta_ho = candidate_ho - base_ho
                    accepted = _accept(delta_in, delta_ho)
                    mlflow.log_metrics(
                        {
                            "delta_in": delta_in,
                            "delta_ho": delta_ho,
                            "non_regression_pass": float(accepted),
                        }
                    )
                    record = {
                        **candidate,
                        "params": params,
                        "baseline": {
                            "held_in_roc_auc": base_in,
                            "held_out_roc_auc": base_ho,
                        },
                        "result": {
                            "held_in": _metrics(outcome.held_in),
                            "held_out": _metrics(outcome.held_out),
                            "delta_in": delta_in,
                            "delta_ho": delta_ho,
                        },
                        "decision": "accept" if accepted else "reject",
                        "decision_rule": (
                            "delta_in >= 0 and delta_ho >= 0 and max(delta) > 0"
                        ),
                        "clinical_status": (
                            "research-only; not validated for patient-level use"
                        ),
                    }
                    reports.append(record)
                    (ROOT / "audit" / f"{candidate['id']}.json").write_text(
                        json.dumps(record, indent=2) + "\n"
                    )

    accepted = [record for record in reports if record["decision"] == "accept"]
    winner = (
        max(
            accepted,
            key=lambda record: min(
                record["result"]["held_in"][PRIMARY],
                record["result"]["held_out"][PRIMARY],
            ),
        )
        if accepted
        else None
    )
    summary = {
        "baseline": {"held_in_roc_auc": base_in, "held_out_roc_auc": base_ho},
        "candidates": reports,
        "winner": winner["id"] if winner else None,
        "stopped_reason": "round_complete" if winner else "no_non_regressing_candidate",
    }
    (ROOT / "reports" / "round3_external_candidates.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
