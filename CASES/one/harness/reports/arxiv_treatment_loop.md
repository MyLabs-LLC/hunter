# arXiv rheumatoid-arthritis treatment research loop

## Scope and stop condition

- Source: [arXiv API](https://export.arxiv.org/api/query?search_query=all%3A%22rheumatoid%20arthritis%22&sortBy=submittedDate&sortOrder=descending), queried in descending submission date order. The broad source query is retained for audit; the treatment screen uses each paper's title and abstract, not incidental mentions in references.
- Source results: 87; hard iteration cap: 1000; completed: 87; stop: `source_exhausted`.
- Each iteration downloads the public paper PDF locally, extracts text, records explicit public-data identifiers, and updates this report.
- An identifier alone is not a valid treatment-response dataset contract. The loop does not run models or infer a treatment plan unless population, baseline time point, exposure, outcome, preprocessing, and split are verified.
- This report is research triage, not medical advice or an individual treatment recommendation.

## Aggregate readout

- Candidate RA-treatment papers by transparent term screen: 33.
- Papers with an explicit identifier or named data source: 9.
- GEO series metadata checked: 14; candidate RA treatment-response series requiring a contract: 0.
- Papers pointing to an already audited local response cohort: 0.

## Existing fixed response benchmark

- The loop did not re-score a sealed cohort while triaging papers. The existing, fixed `GSE129705` anti-TNF response benchmark remains the only locally reproducible external-cohort experiment.
- Regularized logistic regression: held-in ROC-AUC 0.708; sealed external ROC-AUC 0.662 (95% bootstrap interval 0.443–0.851). See [the fixed evaluation](gse129705_baseline.md).
- This level of uncertainty cannot establish that any treatment will work for an individual. None of the arXiv papers above supplied a new compatible, public response dataset contract that could be evaluated without changing those rules.

## Per-paper findings

| # | arXiv paper | Submitted | Term screen | Dataset/data-source leads | Experiment decision |
| ---: | --- | --- | --- | --- | --- |
| 1 | [MechAInistic: An LLM-guided Multi-Agent System for Reasoning over Genome-Scale Constraint-Based Metabolic Models](https://arxiv.org/abs/2607.18249v1) | 2026-05-08T16:24:41Z | candidate_ra_treatment_research | NCBI GEO repository (accession not explicit) | named_source_requires_dataset_contract |
| 2 | [RAM-H1200: A Unified Evaluation and Dataset on Hand Radiographs for Rheumatoid Arthritis](https://arxiv.org/abs/2605.05616v1) | 2026-05-07T03:12:10Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 3 | [Chronological Contrastive Learning: Few-Shot Progression Assessment in Irreversible Diseases](https://arxiv.org/abs/2603.21935v2) | 2026-03-23T12:53:04Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 4 | [Image-based Joint-level Detection for Inflammation in Rheumatoid Arthritis from Small and Imbalanced Data](https://arxiv.org/abs/2602.14365v1) | 2026-02-16T00:33:52Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 5 | [Network-based prediction of drug combinations with quantum annealing](https://arxiv.org/abs/2512.20199v1) | 2025-12-23T09:47:00Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 6 | [Automated Radiographic Total Sharp Score (ARTSS) in Rheumatoid Arthritis: A Solution to Reduce Inter-Intra Reader Variation and Enhancing Clinical Practice](https://arxiv.org/abs/2509.06854v1) | 2025-09-08T16:21:45Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 7 | [Network Community Detection and Novelty Scoring Reveal Underexplored Hub Genes in Rheumatoid Arthritis](https://arxiv.org/abs/2509.00897v1) | 2025-08-31T15:22:19Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 8 | [Interpretable Rheumatoid Arthritis Scoring via Anatomy-aware Multiple Instance Learning](https://arxiv.org/abs/2508.06218v1) | 2025-08-08T10:56:14Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 9 | [Pragmatic Policy Development via Interpretable Behavior Cloning](https://arxiv.org/abs/2507.17056v1) | 2025-07-22T22:34:35Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 10 | [Challenging Disability and Interaction Norms in XR: Cooling Down the Empathy Machine in Waiting for Hands](https://arxiv.org/abs/2507.15481v1) | 2025-07-21T10:36:15Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 11 | [Using off-treatment sequential multiple imputation for binary outcomes to address intercurrent events handled by a treatment policy strategy](https://arxiv.org/abs/2507.14006v1) | 2025-07-18T15:18:36Z | candidate_ra_treatment_research | ClinicalTrials.gov: NCT03970837, NCT03980483 | dataset_contract_required_before_experiment |
| 12 | [RAM-W600: A Multi-Task Wrist Dataset and Benchmark for Rheumatoid Arthritis](https://arxiv.org/abs/2507.05193v4) | 2025-07-07T16:53:22Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 13 | [Classification of autoimmune diseases from Peripheral blood TCR repertoires by multimodal multi-instance learning](https://arxiv.org/abs/2507.04981v4) | 2025-07-07T13:24:41Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 14 | [Evaluation of clinical utility in emulated clinical trials](https://arxiv.org/abs/2506.03991v2) | 2025-06-04T14:18:04Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 15 | [Right Prediction, Wrong Reasoning: Uncovering LLM Misalignment in RA Disease Diagnosis](https://arxiv.org/abs/2504.06581v1) | 2025-04-09T05:04:01Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 16 | [BioX-CPath: Biologically-driven Explainable Diagnostics for Multistain IHC Computational Pathology](https://arxiv.org/abs/2503.20880v2) | 2025-03-26T18:00:22Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 17 | [Layer Separation: Adjustable Joint Space Width Images Synthesis in Conventional Radiography](https://arxiv.org/abs/2502.01972v1) | 2025-02-04T03:33:52Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 18 | [Effect of a new type of healthy and live food supplement on osteoporosis blood parameters and induced rheumatoid arthritis in Wistar rats](https://arxiv.org/abs/2501.19343v1) | 2025-01-31T17:43:38Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 19 | [Hengqin-RA-v1: Advanced Large Language Model for Diagnosis and Treatment of Rheumatoid Arthritis with Dataset based Traditional Chinese Medicine](https://arxiv.org/abs/2501.02471v2) | 2025-01-05T07:46:51Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 20 | [Going Beyond H&E and Oncology: How Do Histopathology Foundation Models Perform for Multi-stain IHC and Immunology?](https://arxiv.org/abs/2410.21560v1) | 2024-10-28T21:48:39Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 21 | [A Comparative Study of Multiple Deep Learning Algorithms for Efficient Localization of Bone Joints in the Upper Limbs of Human Body](https://arxiv.org/abs/2410.20639v1) | 2024-10-28T00:05:38Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 22 | [Dynamic borrowing from historical controls via the synthetic prior with covariates in randomized clinical trials](https://arxiv.org/abs/2410.07242v2) | 2024-10-07T22:35:55Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 23 | [Group lasso based selection for high-dimensional mediation analysis](https://arxiv.org/abs/2409.20036v2) | 2024-09-30T07:41:50Z | out_of_scope_or_background_only | GEO: GSE42861; GSE42861 (ra_case_control_or_mechanistic_not_treatment_response); NCBI GEO repository (accession not explicit) | not_evaluated_out_of_scope |
| 24 | [Incremental Causal Effect for Time to Treatment Initialization](https://arxiv.org/abs/2409.13097v2) | 2024-09-19T21:40:59Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 25 | [Federated One-Shot Ensemble Clustering](https://arxiv.org/abs/2409.08396v1) | 2024-09-12T20:55:21Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 26 | [Associations between exposure to OPEs and rheumatoid arthritis risk among adults in NHANES, 2011-2018](https://arxiv.org/abs/2409.00745v1) | 2024-09-01T15:15:41Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 27 | [Deep Learning Models to Automate the Scoring of Hand Radiographs for Rheumatoid Arthritis](https://arxiv.org/abs/2406.09980v1) | 2024-06-14T12:43:16Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 28 | [An adaptive enrichment design using Bayesian model averaging for selection and threshold-identification of tailoring variables](https://arxiv.org/abs/2405.08180v1) | 2024-05-13T20:58:13Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 29 | [How to develop, externally validate, and update multinomial prediction models](https://arxiv.org/abs/2312.12008v2) | 2023-12-19T09:57:33Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 30 | [Automated segmentation of rheumatoid arthritis immunohistochemistry stained synovial tissue](https://arxiv.org/abs/2309.07255v1) | 2023-09-13T18:43:14Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 31 | [Microbiome-derived bile acids contribute to elevated antigenic response and bone erosion in rheumatoid arthritis](https://arxiv.org/abs/2307.08848v1) | 2023-07-14T04:03:37Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 32 | [MIRACLE: Multi-task Learning based Interpretable Regulation of Autoimmune Diseases through Common Latent Epigenetics](https://arxiv.org/abs/2306.13866v2) | 2023-06-24T05:10:43Z | candidate_ra_treatment_research | GEO: GSE106648, GSE142512, GSE42861, GSE59250, GSE73894, GSE87648; GSE106648 (not_ra_treatment_response_dataset); GSE142512 (not_ra_treatment_response_dataset); GSE42861 (ra_case_control_or_mechanistic_not_treatment_response); GSE59250 (not_ra_treatment_response_dataset); GSE73894 (not_ra_treatment_response_dataset); GSE87648 (not_ra_treatment_response_dataset) | identified_geo_not_treatment_response |
| 33 | [A Deep Registration Method for Accurate Quantification of Joint Space Narrowing Progression in Rheumatoid Arthritis](https://arxiv.org/abs/2304.13938v1) | 2023-04-27T03:08:34Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 34 | [Estimation of age-specific excess mortality of men and women with rheumatoid arthritis (RA) in Germany](https://arxiv.org/abs/2302.11576v1) | 2023-02-22T17:11:50Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 35 | [multi-GPA-Tree: Statistical Approach for Pleiotropy Informed and Functional Annotation Tree Guided Prioritization of GWAS Results](https://arxiv.org/abs/2302.01982v1) | 2023-02-03T20:06:22Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 36 | [Nanoparticles Passive Targeting Allows Optical Imaging of Bone Diseases](https://arxiv.org/abs/2301.01896v1) | 2023-01-05T03:48:20Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 37 | [Prediction of drug effectiveness in rheumatoid arthritis patients based on machine learning algorithms](https://arxiv.org/abs/2210.08016v3) | 2022-10-14T15:15:37Z | candidate_ra_treatment_research | CORRONA/CERTAIN registry, DREAM RA Responder Challenge | named_registry_not_runnable_locally |
| 38 | [Clinical Utility Gains from Incorporating Comorbidity and Geographic Location Information into Risk Estimation Equations for Atherosclerotic Cardiovascular Disease](https://arxiv.org/abs/2209.06985v2) | 2022-09-15T00:22:03Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 39 | [Semi-supervised Transfer Learning for Evaluation of Model Classification Performance](https://arxiv.org/abs/2208.07927v2) | 2022-08-16T19:56:14Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 40 | [Employing Feature Selection Algorithms to Determine the Immune State of a Mouse Model of Rheumatoid Arthritis](https://arxiv.org/abs/2207.05882v2) | 2022-07-12T23:08:47Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 41 | [CNN-based fully automatic wrist cartilage volume quantification in MR Image](https://arxiv.org/abs/2206.11127v1) | 2022-06-22T14:19:06Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 42 | [A Sub-pixel Accurate Quantification of Joint Space Narrowing Progression in Rheumatoid Arthritis](https://arxiv.org/abs/2205.09315v2) | 2022-05-19T04:04:45Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 43 | [A robust Bayesian bias-adjusted random effects model for consideration of uncertainty about bias terms in evidence synthesis](https://arxiv.org/abs/2204.10645v1) | 2022-04-22T11:29:38Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 44 | [Bridging disconnected networks of first and second lines of biologic therapies in rheumatoid arthritis with registry data: Bayesian evidence synthesis with target trial emulation](https://arxiv.org/abs/2201.01720v1) | 2022-01-05T17:22:35Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 45 | [Towards Super-Resolution CEST MRI for Visualization of Small Structures](https://arxiv.org/abs/2112.01905v1) | 2021-12-03T13:41:57Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 46 | [Rheumatoid Arthritis: Automated Scoring of Radiographic Joint Damage](https://arxiv.org/abs/2110.08812v1) | 2021-10-17T12:45:47Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 47 | [Deep Learning for Rheumatoid Arthritis: Joint Detection and Damage Scoring in X-rays](https://arxiv.org/abs/2104.13915v2) | 2021-04-28T17:53:19Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 48 | [DeepRA: Predicting Joint Damage From Radiographs Using CNN with Attention](https://arxiv.org/abs/2102.06982v2) | 2021-02-13T18:48:01Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 49 | [Topological data analysis distinguishes parameter regimes in the Anderson-Chaplain model of angiogenesis](https://arxiv.org/abs/2101.00523v2) | 2021-01-02T22:20:53Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 50 | [MixTwice: large-scale hypothesis testing for peptide arrays by variance mixing](https://arxiv.org/abs/2011.07420v1) | 2020-11-15T00:18:13Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 51 | [COMO: A Pipeline for Multi-Omics Data Integration in Metabolic Modeling and Drug Discovery](https://arxiv.org/abs/2011.02103v2) | 2020-11-04T02:54:09Z | candidate_ra_treatment_research | GEO: GSE107011, GSE110999, GSE118165, GSE92387; GSE107011 (not_ra_treatment_response_dataset); GSE110999 (ra_case_control_or_mechanistic_not_treatment_response); GSE118165 (not_ra_treatment_response_dataset); GSE92387 (not_ra_treatment_response_dataset); NCBI GEO repository (accession not explicit) | identified_geo_not_treatment_response |
| 52 | [Automatic Chronic Degenerative Diseases Identification Using Enteric Nervous System Images](https://arxiv.org/abs/2011.00160v1) | 2020-10-31T01:04:46Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 53 | [Augmented Transfer Regression Learning with Semi-non-parametric Nuisance Models](https://arxiv.org/abs/2010.02521v3) | 2020-10-06T06:50:27Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 54 | [A Dynamic Deep Neural Network For Multimodal Clinical Data Analysis](https://arxiv.org/abs/2008.06294v1) | 2020-08-14T11:19:32Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 55 | [An one-factor copula mixed model for joint meta-analysis of multiple diagnostic tests](https://arxiv.org/abs/2006.09278v2) | 2020-06-16T16:17:08Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 56 | [Blocking of the CD80/86 axis as a therapeutic approach to prevent progression to more severe forms of COVID-19](https://arxiv.org/abs/2005.10055v1) | 2020-05-20T14:05:06Z | candidate_ra_treatment_research | GEO: GSE145926; ClinicalTrials.gov: NCT02090556; GSE145926 (not_ra_treatment_response_dataset); NCBI GEO repository (accession not explicit) | identified_geo_not_treatment_response |
| 57 | [Prior Adaptive Semi-supervised Learning with Application to EHR Phenotyping](https://arxiv.org/abs/2003.11744v2) | 2020-03-26T04:50:28Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 58 | [Quantitative predictive modelling approaches to understanding rheumatoid arthritis: A brief review](https://arxiv.org/abs/1911.09035v4) | 2019-11-20T17:04:28Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 59 | [Cartilage-binding antibodies induce pain through immune complex-mediated activation of neurons](https://arxiv.org/abs/1908.05298v1) | 2019-08-08T13:10:21Z | candidate_ra_treatment_research | ArrayExpress: E-MTAB-7853 | dataset_contract_required_before_experiment |
| 60 | [An Evaluation Toolkit to Guide Model Selection and Cohort Definition in Causal Inference](https://arxiv.org/abs/1906.00442v1) | 2019-06-02T16:36:45Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 61 | [Optimal Statistical Inference for Individualized Treatment Effects in High-dimensional Models](https://arxiv.org/abs/1904.12891v2) | 2019-04-29T18:20:15Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 62 | [Hand range of motion evaluation for Rheumatoid Arthritis patients](https://arxiv.org/abs/1903.06949v1) | 2019-03-16T15:51:23Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 63 | [Pain pathogenesis in rheumatoid arthritis -- what have we learned from animal models](https://arxiv.org/abs/1903.04987v1) | 2019-03-12T15:20:01Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 64 | [Empowering individual trait prediction using interactions](https://arxiv.org/abs/1901.08814v1) | 2019-01-25T10:23:30Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 65 | [Interpretable Graph Convolutional Neural Networks for Inference on Noisy Knowledge Graphs](https://arxiv.org/abs/1812.00279v1) | 2018-12-01T23:04:30Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 66 | [JS-MA: A Jensen-Shannon Divergence Based Method for Mapping Genome-wide Associations on Multiple Diseases](https://arxiv.org/abs/1811.07099v1) | 2018-11-17T04:27:34Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 67 | [Unsupervised Ensemble Learning via Ising Model Approximation with Application to Phenotyping Prediction](https://arxiv.org/abs/1810.06376v1) | 2018-10-15T14:27:38Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 68 | [Using routinely collected patient data to support clinical trials research in accountable care organizations](https://arxiv.org/abs/1807.00668v1) | 2018-06-25T22:13:30Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 69 | [Variable domain N-linked glycosylation and negative surface charge are key features of monoclonal ACPA: implications for B-cell selection](https://arxiv.org/abs/1802.10401v1) | 2018-02-28T13:33:25Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 70 | [A Bayesian Joint model for Longitudinal DAS28 Scores and Competing Risk Informative Drop Out in a Rheumatoid Arthritis Clinical Trial](https://arxiv.org/abs/1801.08628v1) | 2018-01-25T23:07:30Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 71 | [Semi-Supervised Approaches to Efficient Evaluation of Model Prediction Performance](https://arxiv.org/abs/1711.05663v1) | 2017-11-15T16:50:43Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 72 | [Autoreactivity to malondialdehyde-modifications in rheumatoid arthritis is linked to disease activity and synovial pathogenesis](https://arxiv.org/abs/1710.10861v1) | 2017-10-30T10:50:19Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 73 | [LPG: a four-groups probabilistic approach to leveraging pleiotropy in genome-wide association studies](https://arxiv.org/abs/1710.09551v1) | 2017-10-26T06:02:43Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 74 | [Good Arm Identification via Bandit Feedback](https://arxiv.org/abs/1710.06360v2) | 2017-10-17T16:08:16Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 75 | [Development of a passive Rehabilitation Robot for the wrist joint through the implementation of an Arduino UNO microcontroller](https://arxiv.org/abs/1706.05076v1) | 2017-06-07T14:39:20Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 76 | [Vulnerability of geriatric patients to biomaterial associated infections: in vitro study of biofilm formation by Pseudomonas aeruginosa on orthopedic implants](https://arxiv.org/abs/1511.06969v1) | 2015-11-22T06:08:03Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 77 | [A method for delineation of bone surfaces in photoacoustic computed tomography of the finger](https://arxiv.org/abs/1506.02165v1) | 2015-06-06T15:51:24Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 78 | [Initial results of finger imaging using Photoacoustic Computed Tomography](https://arxiv.org/abs/1406.5500v1) | 2014-06-20T19:49:56Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 79 | [Implementing Evidential Reasoning in Expert Systems](https://arxiv.org/abs/1304.2731v1) | 2013-03-27T19:47:55Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 80 | [Finding the basic neighborhood in variable range Markov random fields: application in SNP association studies](https://arxiv.org/abs/1302.5589v1) | 2013-02-22T13:45:49Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 81 | [Attribute Exploration of Gene Regulatory Processes](https://arxiv.org/abs/1204.1995v1) | 2012-04-09T21:23:04Z | out_of_scope_or_background_only | GEO: GSE13837, GSE1742, GSE2624; GSE13837 (ra_case_control_or_mechanistic_not_treatment_response); GSE1742 (not_ra_treatment_response_dataset); GSE2624 (not_ra_treatment_response_dataset); NCBI GEO repository (accession not explicit) | not_evaluated_out_of_scope |
| 82 | [Detection of treatment effects by covariate-adjusted expected shortfall](https://arxiv.org/abs/1101.1407v1) | 2011-01-07T11:23:52Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 83 | [BOOST: A fast approach to detecting gene-gene interactions in genome-wide case-control studies](https://arxiv.org/abs/1001.5130v1) | 2010-01-28T09:01:37Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 84 | [Peptide strings clues to the genesis and treatment of rheumatoid arthritis: rebuilding self-protective immunity amid fungal ruins](https://arxiv.org/abs/0808.1283v1) | 2008-08-10T23:03:29Z | candidate_ra_treatment_research | none detected | no_public_labeled_response_dataset_detected |
| 85 | [Across and beyond the cell are peptide strings](https://arxiv.org/abs/0711.0202v1) | 2007-11-01T19:43:21Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 86 | [Effective Sample Size: Quick Estimation of the Effect of Related Samples in Genetic Case-Control Association Analyses](https://arxiv.org/abs/q-bio/0611093v3) | 2006-11-28T18:22:02Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |
| 87 | [LASSO-Patternsearch algorithm with application to ophthalmology and genomic data](https://arxiv.org/abs/math/0610916v2) | 2006-10-30T19:59:38Z | out_of_scope_or_background_only | none detected | not_evaluated_out_of_scope |

### 1. MechAInistic: An LLM-guided Multi-Agent System for Reasoning over Genome-Scale Constraint-Based Metabolic Models

- arXiv: [2607.18249v1](https://arxiv.org/abs/2607.18249v1); submitted 2026-05-08T16:24:41Z; categories: q-bio.QM, cs.AI.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=therapeutic, drug, biologic; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: NCBI GEO repository (accession not explicit)
- Experiment decision: `named_source_requires_dataset_contract`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 2. RAM-H1200: A Unified Evaluation and Dataset on Hand Radiographs for Rheumatoid Arthritis

- arXiv: [2605.05616v1](https://arxiv.org/abs/2605.05616v1); submitted 2026-05-07T03:12:10Z; categories: cs.CV, cs.LG.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 3. Chronological Contrastive Learning: Few-Shot Progression Assessment in Irreversible Diseases

- arXiv: [2603.21935v2](https://arxiv.org/abs/2603.21935v2); submitted 2026-03-23T12:53:04Z; categories: cs.CV, cs.AI.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 4. Image-based Joint-level Detection for Inflammation in Rheumatoid Arthritis from Small and Imbalanced Data

- arXiv: [2602.14365v1](https://arxiv.org/abs/2602.14365v1); submitted 2026-02-16T00:33:52Z; categories: cs.CV, cs.AI.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 5. Network-based prediction of drug combinations with quantum annealing

- arXiv: [2512.20199v1](https://arxiv.org/abs/2512.20199v1); submitted 2025-12-23T09:47:00Z; categories: quant-ph.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=therapeutic, drug, biologic; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 6. Automated Radiographic Total Sharp Score (ARTSS) in Rheumatoid Arthritis: A Solution to Reduce Inter-Intra Reader Variation and Enhancing Clinical Practice

- arXiv: [2509.06854v1](https://arxiv.org/abs/2509.06854v1); submitted 2025-09-08T16:21:45Z; categories: cs.CV, cs.AI.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 7. Network Community Detection and Novelty Scoring Reveal Underexplored Hub Genes in Rheumatoid Arthritis

- arXiv: [2509.00897v1](https://arxiv.org/abs/2509.00897v1); submitted 2025-08-31T15:22:19Z; categories: q-bio.MN, cs.SI, q-bio.GN.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=biologic; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 8. Interpretable Rheumatoid Arthritis Scoring via Anatomy-aware Multiple Instance Learning

- arXiv: [2508.06218v1](https://arxiv.org/abs/2508.06218v1); submitted 2025-08-08T10:56:14Z; categories: cs.CV.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 9. Pragmatic Policy Development via Interpretable Behavior Cloning

- arXiv: [2507.17056v1](https://arxiv.org/abs/2507.17056v1); submitted 2025-07-22T22:34:35Z; categories: cs.LG, cs.AI.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 10. Challenging Disability and Interaction Norms in XR: Cooling Down the Empathy Machine in Waiting for Hands

- arXiv: [2507.15481v1](https://arxiv.org/abs/2507.15481v1); submitted 2025-07-21T10:36:15Z; categories: cs.HC.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 11. Using off-treatment sequential multiple imputation for binary outcomes to address intercurrent events handled by a treatment policy strategy

- arXiv: [2507.14006v1](https://arxiv.org/abs/2507.14006v1); submitted 2025-07-18T15:18:36Z; categories: stat.ME, stat.AP.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment; status=`candidate_ra_treatment_research`.
- Dataset readout: ClinicalTrials.gov: NCT03970837, NCT03980483
- Named data-source context: No named source detected.
- Experiment decision: `dataset_contract_required_before_experiment`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 12. RAM-W600: A Multi-Task Wrist Dataset and Benchmark for Rheumatoid Arthritis

- arXiv: [2507.05193v4](https://arxiv.org/abs/2507.05193v4); submitted 2025-07-07T16:53:22Z; categories: eess.IV, cs.CV.
- Acquisition: PDF `failed`, text `not_available`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.
- Acquisition error: `refusing download larger than 41943040 bytes`

### 13. Classification of autoimmune diseases from Peripheral blood TCR repertoires by multimodal multi-instance learning

- arXiv: [2507.04981v4](https://arxiv.org/abs/2507.04981v4); submitted 2025-07-07T13:24:41Z; categories: cs.LG, cs.AI, q-bio.GN.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 14. Evaluation of clinical utility in emulated clinical trials

- arXiv: [2506.03991v2](https://arxiv.org/abs/2506.03991v2); submitted 2025-06-04T14:18:04Z; categories: stat.AP.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 15. Right Prediction, Wrong Reasoning: Uncovering LLM Misalignment in RA Disease Diagnosis

- arXiv: [2504.06581v1](https://arxiv.org/abs/2504.06581v1); submitted 2025-04-09T05:04:01Z; categories: cs.AI.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 16. BioX-CPath: Biologically-driven Explainable Diagnostics for Multistain IHC Computational Pathology

- arXiv: [2503.20880v2](https://arxiv.org/abs/2503.20880v2); submitted 2025-03-26T18:00:22Z; categories: cs.CV, q-bio.CB, q-bio.QM, q-bio.TO.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=biologic; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 17. Layer Separation: Adjustable Joint Space Width Images Synthesis in Conventional Radiography

- arXiv: [2502.01972v1](https://arxiv.org/abs/2502.01972v1); submitted 2025-02-04T03:33:52Z; categories: eess.IV, cs.AI, cs.CV, cs.LG.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 18. Effect of a new type of healthy and live food supplement on osteoporosis blood parameters and induced rheumatoid arthritis in Wistar rats

- arXiv: [2501.19343v1](https://arxiv.org/abs/2501.19343v1); submitted 2025-01-31T17:43:38Z; categories: q-bio.TO.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment, therapeutic; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 19. Hengqin-RA-v1: Advanced Large Language Model for Diagnosis and Treatment of Rheumatoid Arthritis with Dataset based Traditional Chinese Medicine

- arXiv: [2501.02471v2](https://arxiv.org/abs/2501.02471v2); submitted 2025-01-05T07:46:51Z; categories: cs.CL.
- Acquisition: PDF `failed`, text `not_available`.
- Transparent screen: RA phrase=True; treatment terms=treatment; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.
- Acquisition error: `HTTP Error 404: Not Found`

### 20. Going Beyond H&E and Oncology: How Do Histopathology Foundation Models Perform for Multi-stain IHC and Immunology?

- arXiv: [2410.21560v1](https://arxiv.org/abs/2410.21560v1); submitted 2024-10-28T21:48:39Z; categories: cs.CV, cs.AI, q-bio.QM, q-bio.TO.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 21. A Comparative Study of Multiple Deep Learning Algorithms for Efficient Localization of Bone Joints in the Upper Limbs of Human Body

- arXiv: [2410.20639v1](https://arxiv.org/abs/2410.20639v1); submitted 2024-10-28T00:05:38Z; categories: cs.CV.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 22. Dynamic borrowing from historical controls via the synthetic prior with covariates in randomized clinical trials

- arXiv: [2410.07242v2](https://arxiv.org/abs/2410.07242v2); submitted 2024-10-07T22:35:55Z; categories: stat.ME.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 23. Group lasso based selection for high-dimensional mediation analysis

- arXiv: [2409.20036v2](https://arxiv.org/abs/2409.20036v2); submitted 2024-09-30T07:41:50Z; categories: q-bio.QM, math.ST.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: GEO: GSE42861
- Named data-source context: NCBI GEO repository (accession not explicit)
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.
- GEO validation: [GSE42861](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE42861&targ=self&form=text&view=quick) — `ra_case_control_or_mechanistic_not_treatment_response`; title: Differential DNA methylation in Rheumatoid arthritis.

### 24. Incremental Causal Effect for Time to Treatment Initialization

- arXiv: [2409.13097v2](https://arxiv.org/abs/2409.13097v2); submitted 2024-09-19T21:40:59Z; categories: stat.ME.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 25. Federated One-Shot Ensemble Clustering

- arXiv: [2409.08396v1](https://arxiv.org/abs/2409.08396v1); submitted 2024-09-12T20:55:21Z; categories: stat.ML, cs.LG, stat.AP.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 26. Associations between exposure to OPEs and rheumatoid arthritis risk among adults in NHANES, 2011-2018

- arXiv: [2409.00745v1](https://arxiv.org/abs/2409.00745v1); submitted 2024-09-01T15:15:41Z; categories: q-bio.QM.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 27. Deep Learning Models to Automate the Scoring of Hand Radiographs for Rheumatoid Arthritis

- arXiv: [2406.09980v1](https://arxiv.org/abs/2406.09980v1); submitted 2024-06-14T12:43:16Z; categories: eess.IV, cs.CV.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 28. An adaptive enrichment design using Bayesian model averaging for selection and threshold-identification of tailoring variables

- arXiv: [2405.08180v1](https://arxiv.org/abs/2405.08180v1); submitted 2024-05-13T20:58:13Z; categories: stat.ME.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 29. How to develop, externally validate, and update multinomial prediction models

- arXiv: [2312.12008v2](https://arxiv.org/abs/2312.12008v2); submitted 2023-12-19T09:57:33Z; categories: stat.ME, stat.AP.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 30. Automated segmentation of rheumatoid arthritis immunohistochemistry stained synovial tissue

- arXiv: [2309.07255v1](https://arxiv.org/abs/2309.07255v1); submitted 2023-09-13T18:43:14Z; categories: eess.IV, cs.CV, q-bio.QM.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 31. Microbiome-derived bile acids contribute to elevated antigenic response and bone erosion in rheumatoid arthritis

- arXiv: [2307.08848v1](https://arxiv.org/abs/2307.08848v1); submitted 2023-07-14T04:03:37Z; categories: physics.bio-ph, q-bio.QM.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 32. MIRACLE: Multi-task Learning based Interpretable Regulation of Autoimmune Diseases through Common Latent Epigenetics

- arXiv: [2306.13866v2](https://arxiv.org/abs/2306.13866v2); submitted 2023-06-24T05:10:43Z; categories: cs.LG.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=biologic; status=`candidate_ra_treatment_research`.
- Dataset readout: GEO: GSE106648, GSE142512, GSE42861, GSE59250, GSE73894, GSE87648
- Named data-source context: No named source detected.
- Experiment decision: `identified_geo_not_treatment_response`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.
- GEO validation: [GSE106648](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE106648&targ=self&form=text&view=quick) — `not_ra_treatment_response_dataset`; title: Differential DNA methylation in Multiple Sclerosis.
- GEO validation: [GSE142512](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE142512&targ=self&form=text&view=quick) — `not_ra_treatment_response_dataset`; title: Longitudinal DNA methylation differences precede type 1 diabetes.
- GEO validation: [GSE42861](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE42861&targ=self&form=text&view=quick) — `ra_case_control_or_mechanistic_not_treatment_response`; title: Differential DNA methylation in Rheumatoid arthritis.
- GEO validation: [GSE59250](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE59250&targ=self&form=text&view=quick) — `not_ra_treatment_response_dataset`; title: DNA Methylation Analysis of Systemic Lupus Erythematosus.
- GEO validation: [GSE73894](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE73894&targ=self&form=text&view=quick) — `not_ra_treatment_response_dataset`; title: Genome-wide DNA methylation analysis of psoriatic and normal skin tissues.
- GEO validation: [GSE87648](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE87648&targ=self&form=text&view=quick) — `not_ra_treatment_response_dataset`; title: Integrative Epigenome-Wide Analysis Shows That DNA Methylation May Mediate Genetic Risk In Inflammatory Bowel Disease [Whole blood, Methylation profiling].

### 33. A Deep Registration Method for Accurate Quantification of Joint Space Narrowing Progression in Rheumatoid Arthritis

- arXiv: [2304.13938v1](https://arxiv.org/abs/2304.13938v1); submitted 2023-04-27T03:08:34Z; categories: eess.IV, cs.CV, cs.LG.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 34. Estimation of age-specific excess mortality of men and women with rheumatoid arthritis (RA) in Germany

- arXiv: [2302.11576v1](https://arxiv.org/abs/2302.11576v1); submitted 2023-02-22T17:11:50Z; categories: q-bio.OT.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 35. multi-GPA-Tree: Statistical Approach for Pleiotropy Informed and Functional Annotation Tree Guided Prioritization of GWAS Results

- arXiv: [2302.01982v1](https://arxiv.org/abs/2302.01982v1); submitted 2023-02-03T20:06:22Z; categories: stat.ME, stat.AP, stat.CO.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 36. Nanoparticles Passive Targeting Allows Optical Imaging of Bone Diseases

- arXiv: [2301.01896v1](https://arxiv.org/abs/2301.01896v1); submitted 2023-01-05T03:48:20Z; categories: physics.bio-ph, physics.med-ph, physics.optics.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 37. Prediction of drug effectiveness in rheumatoid arthritis patients based on machine learning algorithms

- arXiv: [2210.08016v3](https://arxiv.org/abs/2210.08016v3); submitted 2022-10-14T15:15:37Z; categories: q-bio.QM, cs.LG, q-bio.BM.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment, drug, anti-tnf; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: CORRONA/CERTAIN registry, DREAM RA Responder Challenge
- Experiment decision: `named_registry_not_runnable_locally`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 38. Clinical Utility Gains from Incorporating Comorbidity and Geographic Location Information into Risk Estimation Equations for Atherosclerotic Cardiovascular Disease

- arXiv: [2209.06985v2](https://arxiv.org/abs/2209.06985v2); submitted 2022-09-15T00:22:03Z; categories: stat.AP.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 39. Semi-supervised Transfer Learning for Evaluation of Model Classification Performance

- arXiv: [2208.07927v2](https://arxiv.org/abs/2208.07927v2); submitted 2022-08-16T19:56:14Z; categories: stat.ME.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 40. Employing Feature Selection Algorithms to Determine the Immune State of a Mouse Model of Rheumatoid Arthritis

- arXiv: [2207.05882v2](https://arxiv.org/abs/2207.05882v2); submitted 2022-07-12T23:08:47Z; categories: stat.ML, cs.LG.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment, therapy; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 41. CNN-based fully automatic wrist cartilage volume quantification in MR Image

- arXiv: [2206.11127v1](https://arxiv.org/abs/2206.11127v1); submitted 2022-06-22T14:19:06Z; categories: eess.IV, cs.CV, physics.med-ph.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 42. A Sub-pixel Accurate Quantification of Joint Space Narrowing Progression in Rheumatoid Arthritis

- arXiv: [2205.09315v2](https://arxiv.org/abs/2205.09315v2); submitted 2022-05-19T04:04:45Z; categories: eess.IV, cs.CV.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 43. A robust Bayesian bias-adjusted random effects model for consideration of uncertainty about bias terms in evidence synthesis

- arXiv: [2204.10645v1](https://arxiv.org/abs/2204.10645v1); submitted 2022-04-22T11:29:38Z; categories: stat.ME, stat.AP.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=rituximab; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 44. Bridging disconnected networks of first and second lines of biologic therapies in rheumatoid arthritis with registry data: Bayesian evidence synthesis with target trial emulation

- arXiv: [2201.01720v1](https://arxiv.org/abs/2201.01720v1); submitted 2022-01-05T17:22:35Z; categories: stat.AP, stat.ME.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment, therapy, biologic; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 45. Towards Super-Resolution CEST MRI for Visualization of Small Structures

- arXiv: [2112.01905v1](https://arxiv.org/abs/2112.01905v1); submitted 2021-12-03T13:41:57Z; categories: eess.IV, cs.AI, cs.CV, physics.med-ph.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 46. Rheumatoid Arthritis: Automated Scoring of Radiographic Joint Damage

- arXiv: [2110.08812v1](https://arxiv.org/abs/2110.08812v1); submitted 2021-10-17T12:45:47Z; categories: eess.IV, cs.CV, cs.LG.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 47. Deep Learning for Rheumatoid Arthritis: Joint Detection and Damage Scoring in X-rays

- arXiv: [2104.13915v2](https://arxiv.org/abs/2104.13915v2); submitted 2021-04-28T17:53:19Z; categories: cs.CV, cs.LG.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 48. DeepRA: Predicting Joint Damage From Radiographs Using CNN with Attention

- arXiv: [2102.06982v2](https://arxiv.org/abs/2102.06982v2); submitted 2021-02-13T18:48:01Z; categories: cs.CV, cs.AI, cs.LG.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 49. Topological data analysis distinguishes parameter regimes in the Anderson-Chaplain model of angiogenesis

- arXiv: [2101.00523v2](https://arxiv.org/abs/2101.00523v2); submitted 2021-01-02T22:20:53Z; categories: q-bio.QM.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=biologic; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 50. MixTwice: large-scale hypothesis testing for peptide arrays by variance mixing

- arXiv: [2011.07420v1](https://arxiv.org/abs/2011.07420v1); submitted 2020-11-15T00:18:13Z; categories: stat.ME.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 51. COMO: A Pipeline for Multi-Omics Data Integration in Metabolic Modeling and Drug Discovery

- arXiv: [2011.02103v2](https://arxiv.org/abs/2011.02103v2); submitted 2020-11-04T02:54:09Z; categories: q-bio.MN.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment, drug, biologic; status=`candidate_ra_treatment_research`.
- Dataset readout: GEO: GSE107011, GSE110999, GSE118165, GSE92387
- Named data-source context: NCBI GEO repository (accession not explicit)
- Experiment decision: `identified_geo_not_treatment_response`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.
- GEO validation: [GSE107011](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE107011&targ=self&form=text&view=quick) — `not_ra_treatment_response_dataset`; title: RNA-Seq profiling of 29 immune cell types and peripheral blood mononuclear cells.
- GEO validation: [GSE110999](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110999&targ=self&form=text&view=quick) — `ra_case_control_or_mechanistic_not_treatment_response`; title: RNA sequencing of B cell subsets (CD11c hi IgD+ B cells, CD11c hi IgD- B cells, Memory B cells and Naïve B cells) from healthy subjects and subjects with Systemic lupus erythematosus (SLE) or Rheumatoid arthritis (RA).
- GEO validation: [GSE118165](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE118165&targ=self&form=text&view=quick) — `not_ra_treatment_response_dataset`; title: RNA-seq data.
- GEO validation: [GSE92387](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE92387&targ=self&form=text&view=quick) — `not_ra_treatment_response_dataset`; title: Gene expresison studies of lupus and healthy B cell subsets through RNA sequencing.

### 52. Automatic Chronic Degenerative Diseases Identification Using Enteric Nervous System Images

- arXiv: [2011.00160v1](https://arxiv.org/abs/2011.00160v1); submitted 2020-10-31T01:04:46Z; categories: cs.CV, cs.AI, cs.LG.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 53. Augmented Transfer Regression Learning with Semi-non-parametric Nuisance Models

- arXiv: [2010.02521v3](https://arxiv.org/abs/2010.02521v3); submitted 2020-10-06T06:50:27Z; categories: stat.ME.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 54. A Dynamic Deep Neural Network For Multimodal Clinical Data Analysis

- arXiv: [2008.06294v1](https://arxiv.org/abs/2008.06294v1); submitted 2020-08-14T11:19:32Z; categories: cs.LG, stat.ML.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 55. An one-factor copula mixed model for joint meta-analysis of multiple diagnostic tests

- arXiv: [2006.09278v2](https://arxiv.org/abs/2006.09278v2); submitted 2020-06-16T16:17:08Z; categories: stat.ME, stat.AP.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 56. Blocking of the CD80/86 axis as a therapeutic approach to prevent progression to more severe forms of COVID-19

- arXiv: [2005.10055v1](https://arxiv.org/abs/2005.10055v1); submitted 2020-05-20T14:05:06Z; categories: q-bio.TO, q-bio.GN.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=therapeutic, biologic, abatacept; status=`candidate_ra_treatment_research`.
- Dataset readout: GEO: GSE145926; ClinicalTrials.gov: NCT02090556
- Named data-source context: NCBI GEO repository (accession not explicit)
- Experiment decision: `identified_geo_not_treatment_response`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.
- GEO validation: [GSE145926](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE145926&targ=self&form=text&view=quick) — `not_ra_treatment_response_dataset`; title: Single-cell landscape of bronchoalveolar immune cells in COVID-19 patients.

### 57. Prior Adaptive Semi-supervised Learning with Application to EHR Phenotyping

- arXiv: [2003.11744v2](https://arxiv.org/abs/2003.11744v2); submitted 2020-03-26T04:50:28Z; categories: stat.ME.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 58. Quantitative predictive modelling approaches to understanding rheumatoid arthritis: A brief review

- arXiv: [1911.09035v4](https://arxiv.org/abs/1911.09035v4); submitted 2019-11-20T17:04:28Z; categories: q-bio.QM, q-bio.TO.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment, therapeutic, drug, biologic; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 59. Cartilage-binding antibodies induce pain through immune complex-mediated activation of neurons

- arXiv: [1908.05298v1](https://arxiv.org/abs/1908.05298v1); submitted 2019-08-08T13:10:21Z; categories: q-bio.NC, q-bio.TO.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=therapeutic; status=`candidate_ra_treatment_research`.
- Dataset readout: ArrayExpress: E-MTAB-7853
- Named data-source context: No named source detected.
- Experiment decision: `dataset_contract_required_before_experiment`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 60. An Evaluation Toolkit to Guide Model Selection and Cohort Definition in Causal Inference

- arXiv: [1906.00442v1](https://arxiv.org/abs/1906.00442v1); submitted 2019-06-02T16:36:45Z; categories: stat.ML, cs.LG.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 61. Optimal Statistical Inference for Individualized Treatment Effects in High-dimensional Models

- arXiv: [1904.12891v2](https://arxiv.org/abs/1904.12891v2); submitted 2019-04-29T18:20:15Z; categories: stat.ME, math.ST.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 62. Hand range of motion evaluation for Rheumatoid Arthritis patients

- arXiv: [1903.06949v1](https://arxiv.org/abs/1903.06949v1); submitted 2019-03-16T15:51:23Z; categories: cs.CV.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 63. Pain pathogenesis in rheumatoid arthritis -- what have we learned from animal models

- arXiv: [1903.04987v1](https://arxiv.org/abs/1903.04987v1); submitted 2019-03-12T15:20:01Z; categories: q-bio.TO.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 64. Empowering individual trait prediction using interactions

- arXiv: [1901.08814v1](https://arxiv.org/abs/1901.08814v1); submitted 2019-01-25T10:23:30Z; categories: stat.ML, cs.LG.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=biologic; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 65. Interpretable Graph Convolutional Neural Networks for Inference on Noisy Knowledge Graphs

- arXiv: [1812.00279v1](https://arxiv.org/abs/1812.00279v1); submitted 2018-12-01T23:04:30Z; categories: cs.LG, stat.ML.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=therapeutic; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 66. JS-MA: A Jensen-Shannon Divergence Based Method for Mapping Genome-wide Associations on Multiple Diseases

- arXiv: [1811.07099v1](https://arxiv.org/abs/1811.07099v1); submitted 2018-11-17T04:27:34Z; categories: q-bio.GN.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=biologic; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 67. Unsupervised Ensemble Learning via Ising Model Approximation with Application to Phenotyping Prediction

- arXiv: [1810.06376v1](https://arxiv.org/abs/1810.06376v1); submitted 2018-10-15T14:27:38Z; categories: stat.ML, cs.LG.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 68. Using routinely collected patient data to support clinical trials research in accountable care organizations

- arXiv: [1807.00668v1](https://arxiv.org/abs/1807.00668v1); submitted 2018-06-25T22:13:30Z; categories: q-bio.QM, cs.CY, cs.IR.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 69. Variable domain N-linked glycosylation and negative surface charge are key features of monoclonal ACPA: implications for B-cell selection

- arXiv: [1802.10401v1](https://arxiv.org/abs/1802.10401v1); submitted 2018-02-28T13:33:25Z; categories: q-bio.BM, q-bio.CB.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 70. A Bayesian Joint model for Longitudinal DAS28 Scores and Competing Risk Informative Drop Out in a Rheumatoid Arthritis Clinical Trial

- arXiv: [1801.08628v1](https://arxiv.org/abs/1801.08628v1); submitted 2018-01-25T23:07:30Z; categories: stat.AP.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 71. Semi-Supervised Approaches to Efficient Evaluation of Model Prediction Performance

- arXiv: [1711.05663v1](https://arxiv.org/abs/1711.05663v1); submitted 2017-11-15T16:50:43Z; categories: stat.ME.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 72. Autoreactivity to malondialdehyde-modifications in rheumatoid arthritis is linked to disease activity and synovial pathogenesis

- arXiv: [1710.10861v1](https://arxiv.org/abs/1710.10861v1); submitted 2017-10-30T10:50:19Z; categories: q-bio.BM, q-bio.TO.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 73. LPG: a four-groups probabilistic approach to leveraging pleiotropy in genome-wide association studies

- arXiv: [1710.09551v1](https://arxiv.org/abs/1710.09551v1); submitted 2017-10-26T06:02:43Z; categories: stat.ME.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 74. Good Arm Identification via Bandit Feedback

- arXiv: [1710.06360v2](https://arxiv.org/abs/1710.06360v2); submitted 2017-10-17T16:08:16Z; categories: stat.ML.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 75. Development of a passive Rehabilitation Robot for the wrist joint through the implementation of an Arduino UNO microcontroller

- arXiv: [1706.05076v1](https://arxiv.org/abs/1706.05076v1); submitted 2017-06-07T14:39:20Z; categories: cs.RO, physics.med-ph.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=therapy; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 76. Vulnerability of geriatric patients to biomaterial associated infections: in vitro study of biofilm formation by Pseudomonas aeruginosa on orthopedic implants

- arXiv: [1511.06969v1](https://arxiv.org/abs/1511.06969v1); submitted 2015-11-22T06:08:03Z; categories: q-bio.TO.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 77. A method for delineation of bone surfaces in photoacoustic computed tomography of the finger

- arXiv: [1506.02165v1](https://arxiv.org/abs/1506.02165v1); submitted 2015-06-06T15:51:24Z; categories: physics.med-ph.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 78. Initial results of finger imaging using Photoacoustic Computed Tomography

- arXiv: [1406.5500v1](https://arxiv.org/abs/1406.5500v1); submitted 2014-06-20T19:49:56Z; categories: physics.med-ph.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 79. Implementing Evidential Reasoning in Expert Systems

- arXiv: [1304.2731v1](https://arxiv.org/abs/1304.2731v1); submitted 2013-03-27T19:47:55Z; categories: cs.AI.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 80. Finding the basic neighborhood in variable range Markov random fields: application in SNP association studies

- arXiv: [1302.5589v1](https://arxiv.org/abs/1302.5589v1); submitted 2013-02-22T13:45:49Z; categories: stat.ME.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 81. Attribute Exploration of Gene Regulatory Processes

- arXiv: [1204.1995v1](https://arxiv.org/abs/1204.1995v1); submitted 2012-04-09T21:23:04Z; categories: q-bio.MN, cs.CE, cs.LO, math.LO.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: GEO: GSE13837, GSE1742, GSE2624
- Named data-source context: NCBI GEO repository (accession not explicit)
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.
- GEO validation: [GSE13837](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE13837&targ=self&form=text&view=quick) — `ra_case_control_or_mechanistic_not_treatment_response`; title: Adapted Boolean Network Models for Extracellular Matrix Formation.
- GEO validation: [GSE1742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE1742&targ=self&form=text&view=quick) — `not_ra_treatment_response_dataset`; title: TGFbeta signalling in fibroblasts..
- GEO validation: [GSE2624](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE2624&targ=self&form=text&view=quick) — `not_ra_treatment_response_dataset`; title: TNF time course study.

### 82. Detection of treatment effects by covariate-adjusted expected shortfall

- arXiv: [1101.1407v1](https://arxiv.org/abs/1101.1407v1); submitted 2011-01-07T11:23:52Z; categories: stat.AP.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 83. BOOST: A fast approach to detecting gene-gene interactions in genome-wide case-control studies

- arXiv: [1001.5130v1](https://arxiv.org/abs/1001.5130v1); submitted 2010-01-28T09:01:37Z; categories: q-bio.GN, cs.CE, q-bio.QM.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 84. Peptide strings clues to the genesis and treatment of rheumatoid arthritis: rebuilding self-protective immunity amid fungal ruins

- arXiv: [0808.1283v1](https://arxiv.org/abs/0808.1283v1); submitted 2008-08-10T23:03:29Z; categories: q-bio.SC, q-bio.BM.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=treatment, therapeutic; status=`candidate_ra_treatment_research`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `no_public_labeled_response_dataset_detected`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 85. Across and beyond the cell are peptide strings

- arXiv: [0711.0202v1](https://arxiv.org/abs/0711.0202v1); submitted 2007-11-01T19:43:21Z; categories: q-bio.SC, q-bio.BM.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 86. Effective Sample Size: Quick Estimation of the Effect of Related Samples in Genetic Case-Control Association Analyses

- arXiv: [0611093v3](https://arxiv.org/abs/q-bio/0611093v3); submitted 2006-11-28T18:22:02Z; categories: q-bio.QM.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.

### 87. LASSO-Patternsearch algorithm with application to ophthalmology and genomic data

- arXiv: [0610916v2](https://arxiv.org/abs/math/0610916v2); submitted 2006-10-30T19:59:38Z; categories: math.ST.
- Acquisition: PDF `cached`, text `cached`.
- Transparent screen: RA phrase=True; treatment terms=none; status=`out_of_scope_or_background_only`.
- Dataset readout: No explicit public accession detected in the extracted text.
- Named data-source context: No named source detected.
- Experiment decision: `not_evaluated_out_of_scope`.
- Boundary: This is research triage only. It does not establish an effective treatment for a person or replace clinician-led care.
