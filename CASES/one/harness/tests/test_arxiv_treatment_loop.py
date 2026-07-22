from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from run_arxiv_treatment_loop import (
    dataset_ids,
    experiment_decision,
    geo_dataset_status,
    matched_terms,
    named_data_sources,
)


class ArxivTreatmentLoopTests(unittest.TestCase):
    def test_extracts_explicit_public_dataset_identifiers(self) -> None:
        found = dataset_ids("Data came from GSE129705, E-MTAB-123, and NCT01234567.")
        self.assertEqual(found["GEO"], ["GSE129705"])
        self.assertEqual(found["ArrayExpress"], ["E-MTAB-123"])
        self.assertEqual(found["ClinicalTrials.gov"], ["NCT01234567"])

    def test_only_pre_registered_response_cohorts_are_routable(self) -> None:
        decision, cohort = experiment_decision(
            {"GEO": ["GSE129705", "GSE999999"]},
            [],
            [{"accession": "GSE129705", "status": "existing_audited_ra_treatment_response_cohort"}],
            is_treatment_candidate=True,
        )
        self.assertEqual(decision, "existing_audited_experiment_available")
        self.assertEqual(cohort, ["GSE129705"])
        self.assertEqual(
            experiment_decision(
                {"GEO": ["GSE999999"]},
                [],
                [{"accession": "GSE999999", "status": "ra_case_control_or_mechanistic_not_treatment_response"}],
                is_treatment_candidate=True,
            )[0],
            "identified_geo_not_treatment_response",
        )

    def test_treatment_screen_is_transparent(self) -> None:
        self.assertEqual(matched_terms("Anti-TNF therapy is a treatment."), ["treatment", "therapy", "anti-tnf"])

    def test_named_registry_is_recorded_but_not_treated_as_public_data(self) -> None:
        sources = named_data_sources("The CORRONA registry provided the CERTAIN cohort.")
        self.assertEqual(sources, ["CORRONA/CERTAIN registry"])
        self.assertEqual(
            experiment_decision({}, sources, [], is_treatment_candidate=True)[0],
            "named_registry_not_runnable_locally",
        )

    def test_geo_status_requires_an_explicit_response_signal(self) -> None:
        self.assertEqual(
            geo_dataset_status("GSE000001", "Rheumatoid arthritis cases and healthy controls"),
            "ra_case_control_or_mechanistic_not_treatment_response",
        )
        self.assertEqual(
            geo_dataset_status("GSE000002", "Rheumatoid arthritis anti-TNF treatment response"),
            "candidate_ra_treatment_response_contract_required",
        )


if __name__ == "__main__":
    unittest.main()
