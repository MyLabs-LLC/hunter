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

## Independent-cohort baseline — GSE129705

The stronger follow-up task uses only pretreatment whole-blood RNA-seq and the
publication's EULAR `Good` versus `None` response labels. Cohort 1 is the fixed
held-in development population; Cohort 2 is the sealed external population.
There are 34/29 patients and 25,370 genes in the two splits, respectively.

| Model | Held-in ROC-AUC | External ROC-AUC |
| --- | ---: | ---: |
| Logistic regression | 0.708 | 0.662 |
| Random forest | 0.691 | 0.606 |
| XGBoost | 0.667 | 0.636 |

Logistic regression is the provisional champion because it has the highest
ROC-AUC on both fixed cohorts. Its 95% bootstrap intervals are 0.512–0.879
held-in and 0.443–0.851 external, both overlapping chance. The external result
therefore supports continued research only and does not pass a clinical gate.

The first addressable hypothesis is regularization/feature-count stability in
the linear model. Any challenger must improve or preserve both fixed-cohort
ROC-AUC values; Cohort 2 and the evaluator remain sealed and unchanged.

## Independent-cohort challenger outcome

| Candidate | Delta held-in AUC | Delta external AUC | Decision |
| --- | ---: | ---: | --- |
| 20 selected genes | -0.062 | -0.025 | Reject |
| 100 selected genes | -0.003 | -0.015 | Reject |
| logistic C 0.1 | -0.010 | -0.025 | Reject |

None of the three one-parameter logistic challengers satisfied two-split
non-regression. The 50-gene logistic baseline remains unchanged. This round
also exhausts the directly supported generic hyperparameter hypotheses: the
source study reports that baseline genome-wide good/non-response differences
did not concord significantly between cohorts, while cell-type composition did.

Stop reason: `no_non_regressing_candidate`. Continuing to choose generic
hyperparameters against Cohort 2 would increasingly tune to the external set.
A new loop should first pre-register either a cell-composition feature contract
or an additional untouched cohort, then reseal evaluation before compute.

## Round-4 evidence acquisition — arXiv treatment research

The broad arXiv query returned 87 unique rheumatoid-arthritis papers, fewer
than the approved 1,000-document cap. The local loop read every accessible full
text and screened treatment relevance from title/abstract only, so incidental
reference-list mentions could not make a paper a treatment candidate.

The actionable failure signature is **no compatible public response-data
contract**. Nine papers named a data resource or accession. Official GEO
metadata checks covered 14 unique GEO series: none supplied a baseline RA
treatment exposure plus response outcome suitable for the fixed evaluator.
The one direct anti-TNF response-model paper named the CORRONA/CERTAIN registry
but supplied no downloadable accession.

This cluster is not addressable by changing model hyperparameters or the
evaluator. The correct candidate set is empty. Reusing the sealed GSE129705
external labels to choose an unrelated paper's hypothesis would be leakage, so
the loop records a negative result and stops.

## Round-5 web clinical-evidence acquisition

The follow-up web review read current treatment guidance, a D2T-specific
framework, randomized and synthesized switch-versus-cycle evidence, regulator
safety guidance, and a trial registry record. The evidence identifies a
conditional sequence-level hypothesis: after a *first* TNFi failure in studied
patients with objectively active RA, changing to a different mechanism has
stronger comparative support than automatically cycling to another TNFi.

It does not provide a valid individual-treatment label. The case lacks an
objective activity assessment, a complete exposure/response/discontinuation
history, relevant infection/malignancy/cardiovascular/thrombotic screening, and
coordinated overlap-disease assessment. The JAK-specific trial signal cannot
cross the FDA risk-assessment gate from the currently available case record.

No public baseline treatment-response dataset was found in this evidence
tranche. Therefore the editable model surface remains empty and the fixed
GSE129705 external evaluator remains unaccessed. See
`reports/web_evidence_review.md` and `audit/round5_web_evidence_loop.json`.
