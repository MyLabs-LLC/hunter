from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import mlflow
import numpy as np

from model_pipeline import tracking
from ra_harness import build_xgboost_model, evaluate_model, load_geo_series_matrix


ROOT = Path(__file__).resolve().parent
PRIMARY = "roc_auc"

CANDIDATES = [
    {
        "id": "round1_a_selector_40",
        "change": {"selector_k": 40},
        "mechanism": "reduce high-dimensional expression noise",
        "surface": "train-fold feature count",
        "expected_effect": "improve cross-fold stability by retaining fewer probes",
        "regression_risk": "discard weak complementary signal",
    },
    {
        "id": "round1_b_depth_2",
        "change": {"max_depth": 2},
        "mechanism": "reduce boosted-tree interaction variance",
        "surface": "XGBoost tree depth",
        "expected_effect": "reduce overfit interactions in the 36-person held-in set",
        "regression_risk": "underfit a real nonlinear interaction",
    },
    {
        "id": "round1_c_l2_10",
        "change": {"reg_lambda": 10.0},
        "mechanism": "shrink unstable boosted-tree leaf weights",
        "surface": "XGBoost L2 regularization",
        "expected_effect": "reduce variance while preserving ranking signal",
        "regression_risk": "overshrink the already weak response signal",
    },
]


def _metrics(result: Any) -> dict[str, float]:
    return {key: float(value) for key, value in result.scalar_metrics().items()}


def _accept(delta_in: float, delta_ho: float) -> bool:
    return delta_in >= 0.0 and delta_ho >= 0.0 and max(delta_in, delta_ho) > 0.0


def main() -> None:
    config = json.loads((ROOT / "config.json").read_text())
    manifest = json.loads((ROOT / "data" / "manifest.json").read_text())
    baseline = json.loads((ROOT / "reports" / "baseline.json").read_text())
    series = load_geo_series_matrix(ROOT / config["dataset"]["matrix_path"])

    label_col = "response_to_anti-tnf_therapy"
    labels = series.metadata[label_col].str.upper()
    positive = set(config["dataset"]["positive_labels"])
    negative = set(config["dataset"]["negative_labels"])
    selected = labels.isin(positive | negative)
    X = series.expression.loc[selected]
    y = labels.loc[selected].isin(positive).astype(int)

    train_ids = manifest["held_in_sample_ids"]
    holdout_ids = manifest["sealed_holdout_sample_ids"]
    X_train, y_train = X.loc[train_ids], y.loc[train_ids]
    X_holdout, y_holdout = X.loc[holdout_ids], y.loc[holdout_ids]
    seed = int(config["evaluation"]["split_seed"])
    threads = int(config["compute"]["threads"])
    dataset_meta = {
        "name": config["dataset"]["accession"],
        "digest": manifest["sha256"],
        "platform": config["dataset"]["platform"],
    }

    base_in = float(baseline["models"]["xgboost"]["held_in"][PRIMARY])
    base_ho = float(baseline["models"]["xgboost"]["held_out"][PRIMARY])
    reports: list[dict[str, Any]] = []

    os.environ["MLFLOW_TRACKING_URI"] = (ROOT / "mlruns").resolve().as_uri()
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
    with tracking.pipeline_run(
        f"{config['project']}-round1",
        experiment=config["experiment"],
        tags={"baseline_model": "xgboost", "candidate_count": len(CANDIDATES)},
    ):
        with tracking.pipeline_stage("tune"):
            for candidate in CANDIDATES:
                params = {"selector_k": 200, "max_depth": 3, "reg_lambda": 2.0}
                params.update(candidate["change"])
                with tracking.evaluation_run(
                    candidate["id"],
                    description=candidate["mechanism"],
                ):
                    mlflow.log_params(params)
                    outcome = evaluate_model(
                        build_xgboost_model(seed=seed, threads=threads, **params),
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
                        "baseline": {"held_in_roc_auc": base_in, "held_out_roc_auc": base_ho},
                        "result": {
                            "held_in": _metrics(outcome.held_in),
                            "held_out": _metrics(outcome.held_out),
                            "delta_in": delta_in,
                            "delta_ho": delta_ho,
                        },
                        "decision": "accept" if accepted else "reject",
                        "decision_rule": "delta_in >= 0 and delta_ho >= 0 and max(delta) > 0",
                        "clinical_status": "research-only; not validated for patient-level use",
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
    (ROOT / "reports" / "round1_candidates.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
