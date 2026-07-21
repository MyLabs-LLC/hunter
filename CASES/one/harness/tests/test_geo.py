from __future__ import annotations

import gzip
import tempfile
import unittest
from pathlib import Path

from ra_harness.geo import load_geo_series_matrix


class GeoSeriesTest(unittest.TestCase):
    def test_load_geo_series_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "tiny.txt.gz"
            content = """!Sample_geo_accession\t\"GSM1\"\t\"GSM2\"
!Sample_title\t\"one\"\t\"two\"
!Sample_characteristics_ch1\t\"response: RESPONSE\"\t\"response: NORESPONSE\"
!series_matrix_table_begin
\"ID_REF\"\t\"GSM1\"\t\"GSM2\"
\"probe1\"\t1.0\t2.0
\"probe2\"\t3.0\t4.0
!series_matrix_table_end
"""
            with gzip.open(matrix, "wt", encoding="utf-8") as handle:
                handle.write(content)

            series = load_geo_series_matrix(matrix)

            self.assertEqual(series.expression.shape, (2, 2))
            self.assertEqual(series.expression.loc["GSM2", "probe1"], 2.0)
            self.assertEqual(series.metadata.loc["GSM1", "response"], "RESPONSE")


if __name__ == "__main__":
    unittest.main()
