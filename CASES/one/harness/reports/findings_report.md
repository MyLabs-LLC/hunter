# CASE-RA-D2T-A findings report

**Date:** 2026-07-21  
**Scope:** local CPU-only research model harness  
**Status:** exploratory evidence complete; no treatment or model recommendation

## Executive finding

The available evidence does not identify a treatment that can be expected to
work for this individual case. The strongest reproducible result was a small
logistic-regression model trained on baseline whole-blood RNA-seq: ROC-AUC 0.708
in the development cohort and 0.662 in an independent cohort. Its bootstrap
intervals included chance, and all tested challengers failed the prespecified
two-split non-regression gate.

This is weak, unstable population-level ranking signal—not proof of individual
treatment benefit. The correct conclusion is **no treatment was validated for
this case**.

## 1. Case facts and evidence gaps

The case is a fully de-identified synthetic research input describing an adult
woman with approximately ten years of severe, incompletely controlled,
multi-system autoimmune disease and a difficult-to-treat RA candidate phenotype.
Documented facts include IBD/autoimmune overlap, prior certolizumab exposure,
and an approximately six-month DMARD gap.

Treatment-critical variables that are unknown or incomplete include:

- RF and anti-CCP/ACPA status and titers.
- DAS28/CDAI/SDAI trajectory, joint counts, CRP/ESR, and radiographic status.
- Complete csDMARD, biologic, and targeted-synthetic DMARD sequence, dose,
  duration, adherence, response, adverse events, and discontinuation reasons.
- Drug levels and anti-drug antibodies for prior biologic failures.
- Exposure to IL-6R, JAK, CD20/B-cell, and T-cell co-stimulation therapies.
- Extra-articular disease, lung disease, vasculitis, overlap serologies, and
  inflammatory bowel disease phenotype/current therapy.
- Fibromyalgia or central-sensitization overlap, which can mimic active RA.

Without these facts, treatment matching is underdetermined. A transcriptomic
classifier cannot recover missing clinical history, distinguish active synovitis
from non-inflammatory pain, or establish contraindication safety.

## 2. Data and evaluation design

### GSE15258 baseline

The first task used public pretreatment anti-TNF microarray data from
[GSE15258](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE15258). The
publication's binary task was respected: 24 `RESPONSE` versus 22 `NORESPONSE`;
`MEDIUM` and missing outcomes were excluded. A fixed seed-42 stratified split
provided 36 held-in samples and 10 sealed holdout samples.

Models were regularized logistic regression, random forest, and CPU XGBoost.
Feature selection occurred inside training folds. Held-in performance was
five-fold out-of-fold ROC-AUC; holdout performance was measured on the fixed
sealed set with 1,000 bootstrap resamples.

### GSE129705 independent cohorts

The follow-up task used [GSE129705](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE129705),
a biologic-naive RA anti-TNF RNA-seq study with baseline and month-three samples.
Only baseline samples were used, with EULAR `Good` versus `None` labels.

- Cohort 1: 34 patients, development/held-in population.
- Cohort 2: 29 patients, sealed external population.
- Features: 25,370 genes.
- Normalization: per-sample log2(CPM + 1).
- No subjects overlapped between cohorts.

The source study reports that baseline genome-wide good-response versus
non-response differences did not show statistically significant concordance
between cohorts; its more consistent observation involved innate/adaptive cell
composition. That argues against interpreting a generic gene-ranking model as a
treatment selector.

## 3. Model results

### GSE15258

| Model | Held-in ROC-AUC | Sealed ROC-AUC | Decision |
| --- | ---: | ---: | --- |
| Logistic regression | 0.526 | 0.600 | Baseline |
| Random forest | 0.539 | 0.560 | Baseline |
| XGBoost | 0.551 | 0.640 | Initial champion |

Three one-parameter XGBoost challengers were tested: 40 selected genes, depth 2,
and stronger L2 regularization. Each improved one partition while regressing the
other, so all were rejected.

### GSE129705

| Model | Held-in ROC-AUC | External ROC-AUC | 95% external ROC-AUC interval |
| --- | ---: | ---: | ---: |
| Logistic regression | **0.708** | **0.662** | 0.443–0.851 |
| Random forest | 0.691 | 0.606 | 0.374–0.818 |
| XGBoost | 0.667 | 0.636 | 0.406–0.841 |

Logistic regression was provisionally best on both cohorts. Its held-in interval
was 0.512–0.879. The external cohort is small, intervals are broad, and chance
remains plausible.

Three one-parameter logistic challengers were then tested:

| Candidate | Held-in AUC delta | External AUC delta | Decision |
| --- | ---: | ---: | --- |
| 20 selected genes | -0.062 | -0.025 | Reject |
| 100 selected genes | -0.003 | -0.015 | Reject |
| L2 C = 0.1 | -0.010 | -0.025 | Reject |

The 50-gene logistic baseline remains unchanged. The loop stopped with
`no_non_regressing_candidate`.

## 4. What the results do and do not show

### Supported findings

1. Anti-TNF response prediction from small public blood-expression cohorts is
   feasible as exploratory ranking, but the signal is weak and unstable.
2. Independent validation is essential: the apparent ranking advantage changed
   materially across cohorts and did not support a robust treatment selector.
3. Generic feature-count and regularization changes did not produce a
   non-regressing improvement.
4. The public evidence points more toward immune-cell composition and disease
   endotype than toward a universal whole-blood gene signature.

### Unsupported claims

- No result establishes that certolizumab, another anti-TNF, or any other drug
  will work for this patient.
- No result establishes that an anti-TNF class should be continued, stopped, or
  switched.
- No model has been calibrated for individual risk, safety, contraindications,
  or treatment selection.
- No model score should be used to start, stop, or change medication.

## 5. Clinical interpretation boundary

The [American College of Rheumatology RA guideline](https://rheumatology.org/rheumatoid-arthritis-guideline)
provides evidence-based treatment guidance, but applying it requires the
clinician to account for the individual patient's disease state, comorbidities,
prior therapy, risks, and preferences. The case's IBD and unresolved cardiac and
neurologic workups make that individualized review especially important.

The appropriate next clinical step is a rheumatology-led difficult-to-treat RA
review that verifies diagnosis and inflammatory activity, reconstructs the full
DMARD history, assesses adherence and drug-level/anti-drug-antibody data where
relevant, and coordinates IBD and other specialty input. This report is a
research evidence summary only.

## 6. Valid next research step

Do not continue generic hyperparameter tuning against Cohort 2. A defensible
next loop would first define and reseal a new evaluator for one of these:

1. Prespecified immune-cell-composition features replicated in a third untouched
   cohort.
2. A tissue/endotype feature contract that distinguishes mechanism-specific
   response in a trial or prospective cohort.
3. A larger harmonized cohort containing treatment history, disease activity,
   comorbidities, and safety exclusions alongside expression data.

Until one of those steps yields prospective or adequately validated evidence,
the status remains **research hypothesis, not treatment proof**.

## 7. Reproducibility and artifact inventory

- [Harness README](../README.md)
- [Evidence bundle](../audit/evidence_bundle.md)
- [Improvement log](../improvement_log.md)
- [GSE129705 baseline report](gse129705_baseline.md)
- [Round-three challenger audit](round3_external_candidates.json)
- Local MLflow store: `../mlruns/` (ignored by Git)
- Raw cohort matrices: `../data/raw/` (ignored by Git)

All evaluator changes and retained negative results are Git-committed. Tests
pass, and large raw data, model artifacts, caches, and MLflow state are excluded
from version control.

## 8. arXiv treatment-research supplement

The local evidence-acquisition loop queried the current arXiv rheumatoid-
arthritis corpus in descending submission-date order with a 1,000-paper cap. It
found 87 unique papers and stopped `source_exhausted`, rather than reusing
documents. Each accessible PDF was downloaded and read locally; the complete
per-paper record is in [the arXiv loop report](arxiv_treatment_loop.md).

Thirty-three papers met the deliberately simple RA-treatment screen. Nine named
an accession or data source. Official metadata checks of 14 unique GEO series
showed no compatible public baseline treatment-response cohort: the RA records
were case/control or mechanistic studies, and other series were not RA response
studies. The direct anti-TNF response-model preprint
[arXiv:2210.08016](https://arxiv.org/abs/2210.08016) identifies the
CORRONA/CERTAIN registry but supplies no public data accession, so it cannot be
reproduced locally from the paper.

Accordingly, no new experiment was valid and the sealed external GSE129705
cohort was not re-scored. This reinforces, rather than changes, the central
finding: there is no research basis here for a patient-specific treatment plan.
