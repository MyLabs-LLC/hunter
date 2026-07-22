# Improvement log

## Round 0 — setup

- Approved scope: local CPU only; local MLflow; no cloud, GPU, or deployment.
- Candidate families: XGBoost, random forest, regularized logistic regression.
- Initial cohort: GSE15258 anti-TNF response (`RESPONSE` vs `NORESPONSE`).
- Primary metric: ROC-AUC.
- Budget: 30 trials or 3600 seconds; target threshold 0.90.
- Status: first run invalidated before tuning because it included `MEDIUM` labels
  outside the publication's 24-vs-22 binary experiment; MLflow history retained.

## Round 0 — valid baseline

- Labeled cohort: 46 (24 response, 22 no-response).
- Held-in/sealed sizes: 36/10, stratified with seed 42.
- Champion: CPU XGBoost.
- ROC-AUC: 0.551 held-in, 0.640 sealed.
- Interpretation: confidence intervals overlap chance; candidate tuning may
  improve point estimates but cannot establish clinical utility.
- Next: test three one-parameter challengers derived from the failure bundle.

## Round 1 — all challengers rejected

- Selected probes 200 -> 40: held-in AUC 0.520, sealed AUC 0.720.
- XGBoost depth 3 -> 2: held-in AUC 0.588, sealed AUC 0.560.
- XGBoost L2 2 -> 10: held-in AUC 0.607, sealed AUC 0.560.
- Decision: reject all; no model/config edit committed.
- Stopped reason: `no_non_regressing_candidate` for this evidence bundle.
- Next evidence target: a larger independent anti-TNF response cohort to resolve
  whether any observed signal generalizes beyond the ten-person sealed split.

## Round 2 — independent-cohort baseline

- Dataset: GSE129705 baseline whole-blood RNA-seq, per-sample log2(CPM + 1).
- Task: EULAR `Good` versus `None` response to infliximab or adalimumab.
- Fixed populations: Cohort 1 held-in (34); Cohort 2 sealed external (29).
- Provisional champion: logistic regression with 50 train-fold-selected genes.
- ROC-AUC: 0.708 held-in, 0.662 external.
- Interpretation: this is directionally stronger than the small random-holdout
  task, but both intervals overlap chance and calibration is poor externally.
- Next: fixed one-parameter logistic challengers for feature count and L2
  regularization; accept only under the two-split non-regression rule.

## Round 3 — all external-cohort challengers rejected

- Selected genes 50 -> 20: held-in AUC 0.646, external AUC 0.636.
- Selected genes 50 -> 100: held-in AUC 0.705, external AUC 0.646.
- Logistic C 1.0 -> 0.1: held-in AUC 0.698, external AUC 0.636.
- Decision: reject all; the 50-gene logistic baseline remains champion.
- Stopped reason: `no_non_regressing_candidate`.
- Next evidence target: pre-registered cell-composition features or a third
  untouched cohort; do not continue generic tuning against Cohort 2.
