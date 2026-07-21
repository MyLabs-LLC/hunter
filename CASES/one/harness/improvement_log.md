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
