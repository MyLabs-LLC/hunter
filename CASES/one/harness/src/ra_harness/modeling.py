from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, VarianceThreshold, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from model_pipeline import evaluate


@dataclass(frozen=True)
class ModelEvaluation:
    held_in: Any
    held_out: Any
    estimator: Pipeline


def _steps(selector_k: int, estimator: Any, *, scale: bool) -> list[tuple[str, Any]]:
    steps: list[tuple[str, Any]] = [
        ("variance", VarianceThreshold()),
        ("select", SelectKBest(score_func=f_classif, k=selector_k)),
    ]
    if scale:
        steps.append(("scale", StandardScaler()))
    steps.append(("model", estimator))
    return steps


def build_models(*, seed: int, threads: int) -> dict[str, Pipeline]:
    """Return conservative CPU baselines suitable for small p>>n cohorts."""

    return {
        "logistic_regression": Pipeline(
            _steps(
                50,
                LogisticRegression(
                    C=1.0,
                    class_weight="balanced",
                    max_iter=2000,
                    random_state=seed,
                ),
                scale=True,
            )
        ),
        "random_forest": Pipeline(
            _steps(
                200,
                RandomForestClassifier(
                    n_estimators=500,
                    max_depth=5,
                    min_samples_leaf=2,
                    max_features="sqrt",
                    class_weight="balanced_subsample",
                    n_jobs=threads,
                    random_state=seed,
                ),
                scale=False,
            )
        ),
        "xgboost": build_xgboost_model(seed=seed, threads=threads),
    }


def build_xgboost_model(
    *,
    seed: int,
    threads: int,
    selector_k: int = 200,
    max_depth: int = 3,
    reg_lambda: float = 2.0,
) -> Pipeline:
    return Pipeline(
        _steps(
            selector_k,
            XGBClassifier(
                n_estimators=300,
                max_depth=max_depth,
                learning_rate=0.05,
                min_child_weight=2,
                subsample=0.8,
                colsample_bytree=0.5,
                reg_lambda=reg_lambda,
                eval_metric="logloss",
                tree_method="hist",
                device="cpu",
                n_jobs=threads,
                random_state=seed,
            ),
            scale=False,
        )
    )


def evaluate_model(
    estimator: Pipeline,
    X_train: Any,
    y_train: Any,
    X_holdout: Any,
    y_holdout: Any,
    *,
    cv_folds: int,
    seed: int,
    n_resamples: int,
    confidence: float,
    dataset: dict[str, Any],
    model_name: str,
) -> ModelEvaluation:
    """Evaluate one estimator using train OOF and fixed holdout predictions."""

    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=seed)
    oof_score = cross_val_predict(
        estimator,
        X_train,
        y_train,
        cv=cv,
        method="predict_proba",
        n_jobs=1,
    )[:, 1]
    oof_pred = (oof_score >= 0.5).astype(int)
    held_in = evaluate(
        "classification",
        y_true=np.asarray(y_train),
        y_pred=oof_pred,
        y_score=oof_score,
        bootstrap=True,
        n_resamples=n_resamples,
        confidence=confidence,
        seed=seed,
        dataset=dataset,
        params={"model": model_name, "split": "held_in_oof"},
    )

    estimator.fit(X_train, y_train)
    holdout_score = estimator.predict_proba(X_holdout)[:, 1]
    holdout_pred = (holdout_score >= 0.5).astype(int)
    held_out = evaluate(
        "classification",
        y_true=np.asarray(y_holdout),
        y_pred=holdout_pred,
        y_score=holdout_score,
        bootstrap=True,
        n_resamples=n_resamples,
        confidence=confidence,
        seed=seed,
        dataset=dataset,
        params={"model": model_name, "split": "sealed_holdout"},
    )
    return ModelEvaluation(held_in=held_in, held_out=held_out, estimator=estimator)
