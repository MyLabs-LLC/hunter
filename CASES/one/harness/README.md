# CASE-RA-D2T-A local model harness

This project is the CPU-only measurement and tuning harness for the de-identified
research case in the parent directory. It predicts public-cohort treatment
response; it does **not** diagnose the case or recommend treatment.

## First task

- Dataset: NCBI GEO `GSE15258` (processed series matrix, GPL570).
- Population: rheumatoid arthritis patients sampled before anti-TNF therapy.
- Label: the publication's binary task, `RESPONSE` versus `NORESPONSE`;
  `MEDIUM` and missing outcomes are excluded.
- Primary metric: ROC-AUC. Secondary metrics include PR-AUC, F1, log loss,
  Brier score, and MCC.
- Held-in score: five-fold out-of-fold predictions on the training partition.
- Sealed score: fixed 20% stratified holdout, seed 42.
- Baselines: regularized logistic regression, random forest, and CPU XGBoost.
- Tracking: local MLflow file store at `harness/mlruns/`.

The public cohort is training/evaluation data. The single de-identified case is
never inserted into training and cannot be scored until compatible patient-level
features are available.

## Fixed surfaces

- `RA_deidentified_case.json` and the case PDF.
- The label mapping and split seed in `config.json` after baseline measurement.
- Evaluation code and the sealed sample assignment after baseline measurement.
- Downloaded source records and checksums.

## Editable surfaces

- Model family and hyperparameters within the approved CPU families.
- Number of training-fold-selected expression probes.
- Train-fold-only preprocessing and feature selection.

Every challenger is evaluated on the same held-in and sealed partitions. It is
accepted only when `delta_in >= 0`, `delta_ho >= 0`, and at least one delta is
strictly positive. A passing research metric is not evidence that a therapy is
appropriate for an individual.

## Run

Use the interpreter printed by the SDLC skill bootstrap:

```bash
PYTHONPATH=src /path/to/bootstrap-python run_baseline.py
```

Large matrices, MLflow state, run outputs, and model binaries are ignored by Git.
Small configs, checksums, audit records, and reports remain trackable.

De-identified research aid only. Not medical advice, diagnosis, or treatment.
All hypotheses require review and decision by the licensed care team.
