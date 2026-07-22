from __future__ import annotations

import gzip
import tempfile
import unittest
from pathlib import Path

from ra_harness.geo import (
    load_geo_metadata,
    load_geo_series_matrix,
    load_geo_supplementary_counts,
)


class GeoSeriesTest(unittest.TestCase):
    def _write_matrix(self, path: Path, *, include_expression: bool) -> None:
        content = """!Sample_geo_accession\t\"GSM1\"\t\"GSM2\"
!Sample_title\t\"one\"\t\"two\"
!Sample_characteristics_ch1\t\"response: RESPONSE\"\t\"response: NORESPONSE\"
!series_matrix_table_begin
"""
        if include_expression:
            content += """\"ID_REF\"\t\"GSM1\"\t\"GSM2\"
\"probe1\"\t1.0\t2.0
\"probe2\"\t3.0\t4.0
"""
        content += "!series_matrix_table_end\n"
        with gzip.open(path, "wt", encoding="utf-8") as handle:
            handle.write(content)

    def test_load_geo_series_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "tiny.txt.gz"
            self._write_matrix(matrix, include_expression=True)

            series = load_geo_series_matrix(matrix)

            self.assertEqual(series.expression.shape, (2, 2))
            self.assertEqual(series.expression.loc["GSM2", "probe1"], 2.0)
            self.assertEqual(series.metadata.loc["GSM1", "response"], "RESPONSE")

    def test_load_metadata_without_embedded_expression(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "metadata.txt.gz"
            self._write_matrix(matrix, include_expression=False)

            metadata = load_geo_metadata(matrix)

            self.assertEqual(metadata.loc["GSM2", "title"], "two")
            self.assertEqual(metadata.loc["GSM1", "response"], "RESPONSE")

    def test_load_supplementary_counts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            matrix = root / "metadata.txt.gz"
            counts = root / "counts.txt.gz"
            self._write_matrix(matrix, include_expression=False)
            count_content = """Geneid\tChr\tStart\tEnd\tStrand\tLength\tone\ttwo
gene1\t1\t1\t2\t+\t2\t10\t20
gene2\t1\t3\t4\t-\t2\t30\t40
"""
            with gzip.open(counts, "wt", encoding="utf-8") as handle:
                handle.write(count_content)

            series = load_geo_supplementary_counts(matrix, counts)

            self.assertEqual(series.expression.shape, (2, 2))
            self.assertEqual(series.expression.loc["GSM2", "gene1"], 20)
            self.assertEqual(series.metadata.loc["GSM1", "title"], "one")


if __name__ == "__main__":
    unittest.main()
