# Evidence bundle — baseline round

Status: valid baseline measured.

Failure clusters will be ordered by support and addressability after all three
CPU baselines have been scored on the fixed held-in and sealed partitions.
Neither the evaluator nor the sealed sample assignment is an editable surface.

## Setup finding: label contract mismatch

The first instrumented run grouped `MEDIUM` with `RESPONSE`. The primary
publication (PMID 19699293, DOI 10.1016/j.ygeno.2009.08.008) describes the
modeled data as 24 responders and 22 non-responders. Those counts match the GEO
`RESPONSE` and `NORESPONSE` fields exactly and exclude the 29 `MEDIUM` records.

Decision: mark the first run invalid for promotion, retain its MLflow history,
correct the task contract once, and create a new fixed split before candidate
tuning. This is a scientific task-definition correction, not an accepted model
edit.

## Valid baseline

| Model | Held-in ROC-AUC | Sealed ROC-AUC |
| --- | ---: | ---: |
| Logistic regression | 0.526 | 0.600 |
| Random forest | 0.539 | 0.560 |
| XGBoost | 0.551 | 0.640 |

XGBoost is the initial champion because it has the highest point estimate on
both fixed partitions. All confidence intervals overlap 0.5, so the result is a
lineage baseline and not a reliable treatment-response biomarker.

## Failure signatures

1. **High-dimensional instability** — 54,675 probes for 36 held-in samples;
   baseline feature selection retains 200 probes per fold. The publication
   explicitly describes accumulated noise from redundant genes and reduces a
   convergent 40-transcript set to 8 predictors. Support: all three model
   families remain near chance; addressable by a single feature-count change.
2. **Tree interaction variance** — XGBoost wins both point estimates but its
   intervals are extremely wide. Support: only 10 sealed samples; addressable
   by shallower trees, but final resolution requires more independent data.
3. **Weight variance** — the small cohort may permit large boosted-tree leaf
   weights. Addressable by stronger L2 regularization.

## Round-1 candidates

- A: change XGBoost selected probes from 200 to 40.
- B: change XGBoost maximum depth from 3 to 2.
- C: change XGBoost L2 regularization from 2 to 10.

Each candidate changes one declared parameter. The scorer, labels, splits, and
source matrix remain fixed.

## Round-1 outcome

| Candidate | Delta held-in AUC | Delta sealed AUC | Decision |
| --- | ---: | ---: | --- |
| 40 selected probes | -0.031 | +0.080 | Reject |
| maximum depth 2 | +0.037 | -0.080 | Reject |
| L2 regularization 10 | +0.056 | -0.080 | Reject |

All candidates traded performance between partitions. None satisfied the fixed
non-regression rule. The recurring mechanism is now **validation instability**:
the sealed set has only ten people, and model/config changes do not generalize
consistently across the split. The next addressable surface is independent cohort
validation, not another same-cohort hyperparameter edit.
