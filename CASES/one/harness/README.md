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

## Independent-cohort task

`config_gse129705.json` defines a second, stronger anti-TNF response test using
baseline whole-blood RNA-seq from `GSE129705`. It predicts EULAR `Good` versus
`None`, trains with five-fold out-of-fold predictions on Cohort 1, and reserves
Cohort 2 as the sealed external cohort. Counts receive per-sample
`log2(CPM + 1)` normalization; variance filtering and supervised feature
selection remain inside each training fold.

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
PYTHONPATH=src /path/to/bootstrap-python run_external_baseline.py
PYTHONPATH=src /path/to/bootstrap-python run_external_candidates.py
```

## arXiv RA-treatment research loop

`run_arxiv_treatment_loop.py` retrieves the current arXiv corpus returned for
`"rheumatoid arthritis"`, newest first, with a hard cap of 1,000 unique papers.
For each paper it downloads the public PDF, extracts local text, records explicit
data identifiers (for example, GEO accessions), and updates
`reports/arxiv_treatment_loop.md` immediately. PDFs and extraction caches stay
local and are ignored by Git; the source URLs and per-paper findings are tracked.

```bash
/path/to/bootstrap-python run_arxiv_treatment_loop.py --limit 1000
```

It is deliberately conservative: mentioning an accession is not enough to run a
response model. A dataset must first have a documented baseline time point,
treatment exposure, response outcome, preprocessing, and fixed split. Until
then, the loop reports the candidate rather than fabricating a result. It never
selects a treatment plan for the de-identified case.

Large matrices, MLflow state, run outputs, and model binaries are ignored by Git.
Small configs, checksums, audit records, and reports remain trackable.

De-identified research aid only. Not medical advice, diagnosis, or treatment.
All hypotheses require review and decision by the licensed care team.
