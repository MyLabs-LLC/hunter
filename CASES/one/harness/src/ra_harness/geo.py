from __future__ import annotations

import csv
import gzip
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class GeoSeries:
    expression: pd.DataFrame
    metadata: pd.DataFrame


def _clean(value: str) -> str:
    return value.strip().strip('"')


def load_geo_series_matrix(path: str | Path) -> GeoSeries:
    """Load expression and sample metadata from a GEO series-matrix file.

    Expression is returned sample-by-probe. Repeated GEO characteristic rows are
    expanded into one metadata column per characteristic key.
    """

    path = Path(path)
    opener = gzip.open if path.suffix == ".gz" else open
    sample_rows: dict[str, list[str]] = {}
    characteristic_rows: list[list[str]] = []

    with opener(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("!series_matrix_table_begin"):
                break
            if not line.startswith("!Sample_"):
                continue
            row = next(csv.reader([line], delimiter="\t"))
            key, values = row[0], [_clean(value) for value in row[1:]]
            if key == "!Sample_characteristics_ch1":
                characteristic_rows.append(values)
            else:
                sample_rows[key.removeprefix("!Sample_")] = values

    accessions = sample_rows.get("geo_accession")
    if not accessions:
        raise ValueError("GEO matrix is missing !Sample_geo_accession")

    metadata = pd.DataFrame(index=pd.Index(accessions, name="sample_id"))
    for key, values in sample_rows.items():
        if len(values) == len(accessions):
            metadata[key] = values

    for values in characteristic_rows:
        if len(values) != len(accessions):
            raise ValueError("GEO characteristic row does not match sample count")
        parsed: dict[str, list[str]] = {}
        for value in values:
            key, separator, item = value.partition(":")
            parsed.setdefault(key.strip().lower().replace(" ", "_"), []).append(
                item.strip() if separator else value.strip()
            )
        if len(parsed) != 1:
            raise ValueError("GEO characteristic row contains inconsistent keys")
        key, items = next(iter(parsed.items()))
        metadata[key] = items

    expression = pd.read_csv(
        path,
        sep="\t",
        compression="infer",
        comment="!",
        index_col=0,
    ).T
    expression.index = expression.index.str.strip('"')
    expression.index.name = "sample_id"
    expression.columns = expression.columns.str.strip('"')
    expression = expression.apply(pd.to_numeric, errors="raise")
    expression = expression.loc[metadata.index]

    if expression.index.has_duplicates or expression.columns.has_duplicates:
        raise ValueError("GEO expression matrix contains duplicate samples or probes")
    if expression.isna().any().any():
        raise ValueError("GEO expression matrix contains missing numeric values")

    return GeoSeries(expression=expression, metadata=metadata)
