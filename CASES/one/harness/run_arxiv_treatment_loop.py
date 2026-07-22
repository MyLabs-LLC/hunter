"""Acquire and triage arXiv RA-treatment research without treatment recommendations.

Each iteration downloads one public arXiv paper, extracts its text locally,
looks only for explicit public-data identifiers, and appends a finding to the
tracked report.  A treatment-response model is never started from an accession
alone: a pre-registered dataset contract (population, baseline time point,
outcome, treatment, split, and preprocessing) is required first.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
RESEARCH_ROOT = ROOT / "research"
PAPERS_DIR = RESEARCH_ROOT / "papers"
TEXT_DIR = RESEARCH_ROOT / "text"
GEO_DIR = RESEARCH_ROOT / "geo"
REPORTS_DIR = ROOT / "reports"
JSON_REPORT = REPORTS_DIR / "arxiv_treatment_loop.json"
MARKDOWN_REPORT = REPORTS_DIR / "arxiv_treatment_loop.md"
FIXED_BENCHMARK_REPORT = REPORTS_DIR / "gse129705_baseline.json"

ATOM = "{http://www.w3.org/2005/Atom}"
OPENSEARCH = "{http://a9.com/-/spec/opensearch/1.1/}"
ARXIV_QUERY = 'all:"rheumatoid arthritis"'
USER_AGENT = "hunter-ra-research-loop/1.0 (local reproducibility research)"
MAX_PDF_BYTES = 40 * 1024 * 1024

DATASET_PATTERNS = {
    "GEO": re.compile(r"\bGSE\d{3,}\b", flags=re.IGNORECASE),
    "ArrayExpress": re.compile(r"\bE-MTAB-\d+\b", flags=re.IGNORECASE),
    "dbGaP": re.compile(r"\bphs\d{6,}\b", flags=re.IGNORECASE),
    "EGA": re.compile(r"\bEGAS\d+\b", flags=re.IGNORECASE),
    "ClinicalTrials.gov": re.compile(r"\bNCT\d{8}\b", flags=re.IGNORECASE),
}
NAMED_DATA_SOURCE_PATTERNS = {
    "CORRONA/CERTAIN registry": re.compile(
        r"\b(?:CORRONA|CorEvitas)\b.{0,120}\bCERTAIN\b",
        flags=re.IGNORECASE | re.DOTALL,
    ),
    "DREAM RA Responder Challenge": re.compile(
        r"\bDREAM\b.{0,120}\b(?:rheumatoid arthritis|RA)\b.{0,120}\bresponder\b",
        flags=re.IGNORECASE | re.DOTALL,
    ),
    "NCBI GEO repository (accession not explicit)": re.compile(
        r"(?:Gene Expression Omnibus|\bNCBI GEO\b)", flags=re.IGNORECASE
    ),
}
TREATMENT_TERMS = (
    "treatment",
    "therapy",
    "therapeutic",
    "drug",
    "anti-tnf",
    "biologic",
    "dmard",
    "jak inhibitor",
    "abatacept",
    "rituximab",
    "tocilizumab",
)


@dataclass(frozen=True)
class Paper:
    arxiv_id: str
    title: str
    submitted: str
    updated: str
    categories: list[str]
    source_url: str
    pdf_url: str
    abstract: str


def _collapse(text: str | None) -> str:
    return " ".join((text or "").split())


def _request(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        size = response.headers.get("Content-Length")
        if size is not None and int(size) > MAX_PDF_BYTES:
            raise ValueError(f"refusing download larger than {MAX_PDF_BYTES} bytes")
        chunks: list[bytes] = []
        seen = 0
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            seen += len(chunk)
            if seen > MAX_PDF_BYTES:
                raise ValueError(f"refusing download larger than {MAX_PDF_BYTES} bytes")
            chunks.append(chunk)
        return b"".join(chunks)


def fetch_papers(limit: int, request_delay_s: float) -> tuple[int, list[Paper]]:
    """Fetch at most ``limit`` papers, obeying arXiv's paced API use."""

    papers: list[Paper] = []
    total_results: int | None = None
    page_size = 100
    for start in range(0, limit, page_size):
        encoded = urllib.parse.urlencode(
            {
                "search_query": ARXIV_QUERY,
                "start": start,
                "max_results": min(page_size, limit - start),
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }
        )
        root = ET.fromstring(_request(f"https://export.arxiv.org/api/query?{encoded}"))
        if total_results is None:
            total_results = int(root.findtext(f"{OPENSEARCH}totalResults", default="0"))
        entries = root.findall(f"{ATOM}entry")
        if not entries:
            break
        for entry in entries:
            arxiv_id = _collapse(entry.findtext(f"{ATOM}id")).rsplit("/", 1)[-1]
            pdf_url = ""
            source_url = f"https://arxiv.org/abs/{arxiv_id}"
            for link in entry.findall(f"{ATOM}link"):
                href = link.attrib.get("href", "")
                if link.attrib.get("rel") == "alternate":
                    source_url = href
                if link.attrib.get("title") == "pdf":
                    pdf_url = href
            papers.append(
                Paper(
                    arxiv_id=arxiv_id,
                    title=_collapse(entry.findtext(f"{ATOM}title")),
                    submitted=_collapse(entry.findtext(f"{ATOM}published")),
                    updated=_collapse(entry.findtext(f"{ATOM}updated")),
                    categories=[category.attrib["term"] for category in entry.findall(f"{ATOM}category")],
                    source_url=source_url,
                    pdf_url=pdf_url or f"https://arxiv.org/pdf/{arxiv_id}",
                    abstract=_collapse(entry.findtext(f"{ATOM}summary")),
                )
            )
        if len(papers) >= min(limit, total_results):
            break
        time.sleep(request_delay_s)
    return total_results or 0, papers[:limit]


def safe_stem(arxiv_id: str) -> str:
    return arxiv_id.replace("/", "_")


def download_and_extract(paper: Paper) -> tuple[str, str, str | None]:
    """Return PDF/text status, extracted text, and an error if one occurred."""

    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    stem = safe_stem(paper.arxiv_id)
    pdf_path = PAPERS_DIR / f"{stem}.pdf"
    text_path = TEXT_DIR / f"{stem}.txt"
    try:
        pdf_status = "cached"
        if not pdf_path.exists():
            temporary = pdf_path.with_suffix(".download")
            temporary.write_bytes(_request(paper.pdf_url))
            temporary.replace(pdf_path)
            pdf_status = "downloaded"
        text_status = "cached"
        if not text_path.exists():
            subprocess.run(
                ["pdftotext", "-layout", str(pdf_path), str(text_path)],
                check=True,
                timeout=120,
                capture_output=True,
                text=True,
            )
            text_status = "extracted"
        return pdf_status, text_status, None
    except (OSError, ValueError, subprocess.SubprocessError, urllib.error.URLError) as exc:
        return "failed", "not_available", str(exc)


def dataset_ids(text: str) -> dict[str, list[str]]:
    return {
        source: sorted({match.upper() for match in pattern.findall(text)})
        for source, pattern in DATASET_PATTERNS.items()
        if pattern.findall(text)
    }


def named_data_sources(text: str) -> list[str]:
    return [name for name, pattern in NAMED_DATA_SOURCE_PATTERNS.items() if pattern.search(text)]


def geo_dataset_status(accession: str, metadata: str) -> str:
    """Classify a GEO lead without treating mechanistic studies as response data."""

    if accession in {"GSE15258", "GSE129705"}:
        return "existing_audited_ra_treatment_response_cohort"
    text = metadata.lower()
    if "rheumatoid arthritis" not in text:
        return "not_ra_treatment_response_dataset"
    response_terms = (
        "treatment response",
        "drug response",
        "anti-tnf",
        "tnf inhibitor",
        "eular response",
        "therapy response",
    )
    if any(term in text for term in response_terms):
        return "candidate_ra_treatment_response_contract_required"
    return "ra_case_control_or_mechanistic_not_treatment_response"


def _geo_series_fields(text: str) -> dict[str, object]:
    fields: dict[str, list[str]] = {"title": [], "summary": [], "overall_design": [], "type": []}
    for line in text.splitlines():
        for field in fields:
            prefix = f"!Series_{field} = "
            if line.startswith(prefix):
                fields[field].append(_collapse(line.removeprefix(prefix)))
    return {
        "title": fields["title"][0] if fields["title"] else "",
        "summary": fields["summary"],
        "overall_design": fields["overall_design"],
        "type": fields["type"],
    }


def validate_geo_series(accession: str) -> dict[str, object]:
    """Fetch small GEO metadata, cache it locally, and classify the source role."""

    GEO_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = GEO_DIR / f"{accession}.txt"
    source_url = (
        "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?"
        + urllib.parse.urlencode({"acc": accession, "targ": "self", "form": "text", "view": "quick"})
    )
    try:
        if cache_path.exists():
            raw = cache_path.read_text(errors="replace")
            acquisition = "cached"
        else:
            raw = _request(source_url).decode("utf-8", errors="replace")
            cache_path.write_text(raw)
            acquisition = "downloaded"
            time.sleep(0.35)
        fields = _geo_series_fields(raw)
        status = geo_dataset_status(accession, raw)
        return {
            "accession": accession,
            "source_url": source_url,
            "acquisition": acquisition,
            "status": status,
            **fields,
            "error": None,
        }
    except (OSError, ValueError, urllib.error.URLError) as exc:
        return {
            "accession": accession,
            "source_url": source_url,
            "acquisition": "failed",
            "status": "metadata_unavailable",
            "title": "",
            "summary": [],
            "overall_design": [],
            "type": [],
            "error": str(exc),
        }


def matched_terms(text: str) -> list[str]:
    text = text.lower()
    return [term for term in TREATMENT_TERMS if term in text]


def experiment_decision(
    identifiers: dict[str, list[str]],
    named_sources: list[str],
    geo_validation: list[dict[str, object]],
    *,
    is_treatment_candidate: bool,
) -> tuple[str, list[str]]:
    """Route only source contracts already fixed in the audited harness."""

    if not is_treatment_candidate:
        return ("not_evaluated_out_of_scope", [])
    compatible = sorted(
        str(record["accession"])
        for record in geo_validation
        if record["status"] == "existing_audited_ra_treatment_response_cohort"
    )
    if compatible:
        return (
            "existing_audited_experiment_available",
            compatible,
        )
    if any(record["status"] == "candidate_ra_treatment_response_contract_required" for record in geo_validation):
        return ("dataset_contract_required_before_experiment", [])
    if geo_validation:
        return ("identified_geo_not_treatment_response", [])
    if identifiers:
        return (
            "dataset_contract_required_before_experiment",
            [],
        )
    if "CORRONA/CERTAIN registry" in named_sources:
        return ("named_registry_not_runnable_locally", [])
    if named_sources:
        return ("named_source_requires_dataset_contract", [])
    return ("no_public_labeled_response_dataset_detected", [])


def record_finding(paper: Paper, full_text: str, pdf_status: str, text_status: str, error: str | None) -> dict[str, object]:
    searchable = f"{paper.title}\n{paper.abstract}\n{full_text}"
    screen_text = f"{paper.title}\n{paper.abstract}"
    identifiers = dataset_ids(searchable)
    named_sources = named_data_sources(searchable)
    geo_validation = [validate_geo_series(accession) for accession in identifiers.get("GEO", [])]
    terms = matched_terms(screen_text)
    ra_mentioned = "rheumatoid arthritis" in screen_text.lower()
    is_treatment_candidate = ra_mentioned and bool(terms)
    decision, existing = experiment_decision(
        identifiers,
        named_sources,
        geo_validation,
        is_treatment_candidate=is_treatment_candidate,
    )
    return {
        **asdict(paper),
        "ra_mentioned": ra_mentioned,
        "treatment_terms_matched": terms,
        "screen_status": "candidate_ra_treatment_research" if is_treatment_candidate else "out_of_scope_or_background_only",
        "pdf_status": pdf_status,
        "text_status": text_status,
        "dataset_identifiers": identifiers,
        "named_data_sources": named_sources,
        "geo_series_validation": geo_validation,
        "experiment_status": decision,
        "existing_audited_datasets": existing,
        "error": error,
        "clinical_boundary": (
            "This is research triage only. It does not establish an effective treatment "
            "for a person or replace clinician-led care."
        ),
    }


def _cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def fixed_response_benchmark() -> dict[str, float] | None:
    """Read the already-sealed external response evaluation without re-scoring it."""

    if not FIXED_BENCHMARK_REPORT.exists():
        return None
    report = json.loads(FIXED_BENCHMARK_REPORT.read_text())
    result = report["models"]["logistic_regression"]
    return {
        "held_in_roc_auc": float(result["held_in"]["roc_auc"]),
        "external_roc_auc": float(result["held_out"]["roc_auc"]),
        "external_roc_auc_ci_low": float(result["held_out"]["roc_auc_ci_low"]),
        "external_roc_auc_ci_high": float(result["held_out"]["roc_auc_ci_high"]),
    }


def write_reports(total_results: int, limit: int, findings: list[dict[str, object]]) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    stopped_reason = "source_exhausted" if total_results <= limit else "max_iterations_reached"
    benchmark = fixed_response_benchmark()
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "arXiv API",
        "query": ARXIV_QUERY,
        "source_results": total_results,
        "iteration_cap": limit,
        "iterations_completed": len(findings),
        "stopped_reason": stopped_reason,
        "findings": findings,
        "fixed_existing_response_benchmark": benchmark,
        "experiment_policy": (
            "An accession alone does not authorize a model run. A reproducible RA treatment-response "
            "dataset contract and a fixed evaluator are required before any experiment."
        ),
    }
    JSON_REPORT.write_text(json.dumps(payload, indent=2) + "\n")

    candidate_count = sum(finding["screen_status"] == "candidate_ra_treatment_research" for finding in findings)
    dataset_count = sum(
        bool(finding["dataset_identifiers"] or finding["named_data_sources"])
        for finding in findings
    )
    experiment_count = sum(bool(finding["existing_audited_datasets"]) for finding in findings)
    geo_checked = len(
        {
            record["accession"]
            for finding in findings
            for record in finding["geo_series_validation"]
        }
    )
    geo_response_candidates = sum(
        record["status"] == "candidate_ra_treatment_response_contract_required"
        for finding in findings
        for record in finding["geo_series_validation"]
    )
    lines = [
        "# arXiv rheumatoid-arthritis treatment research loop",
        "",
        "## Scope and stop condition",
        "",
        f"- Source: [arXiv API](https://export.arxiv.org/api/query?search_query=all%3A%22rheumatoid%20arthritis%22&sortBy=submittedDate&sortOrder=descending), queried in descending submission date order. The broad source query is retained for audit; the treatment screen uses each paper's title and abstract, not incidental mentions in references.",
        f"- Source results: {total_results}; hard iteration cap: {limit}; completed: {len(findings)}; stop: `{stopped_reason}`.",
        "- Each iteration downloads the public paper PDF locally, extracts text, records explicit public-data identifiers, and updates this report.",
        "- An identifier alone is not a valid treatment-response dataset contract. The loop does not run models or infer a treatment plan unless population, baseline time point, exposure, outcome, preprocessing, and split are verified.",
        "- This report is research triage, not medical advice or an individual treatment recommendation.",
        "",
        "## Aggregate readout",
        "",
        f"- Candidate RA-treatment papers by transparent term screen: {candidate_count}.",
        f"- Papers with an explicit identifier or named data source: {dataset_count}.",
        f"- GEO series metadata checked: {geo_checked}; candidate RA treatment-response series requiring a contract: {geo_response_candidates}.",
        f"- Papers pointing to an already audited local response cohort: {experiment_count}.",
        "",
        "## Existing fixed response benchmark",
        "",
    ]
    if benchmark:
        lines.extend(
            [
                "- The loop did not re-score a sealed cohort while triaging papers. The existing, fixed `GSE129705` anti-TNF response benchmark remains the only locally reproducible external-cohort experiment.",
                f"- Regularized logistic regression: held-in ROC-AUC {benchmark['held_in_roc_auc']:.3f}; sealed external ROC-AUC {benchmark['external_roc_auc']:.3f} (95% bootstrap interval {benchmark['external_roc_auc_ci_low']:.3f}–{benchmark['external_roc_auc_ci_high']:.3f}). See [the fixed evaluation](gse129705_baseline.md).",
                "- This level of uncertainty cannot establish that any treatment will work for an individual. None of the arXiv papers above supplied a new compatible, public response dataset contract that could be evaluated without changing those rules.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "- No existing fixed response benchmark was available locally.",
                "",
            ]
        )
    lines.extend(
        [
        "## Per-paper findings",
        "",
        "| # | arXiv paper | Submitted | Term screen | Dataset/data-source leads | Experiment decision |",
        "| ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for number, finding in enumerate(findings, start=1):
        ids = finding["dataset_identifiers"]
        named_sources = finding["named_data_sources"]
        identifiers_text = "; ".join(f"{source}: {', '.join(values)}" for source, values in ids.items())
        geo_status_text = "; ".join(
            f"{record['accession']} ({record['status']})"
            for record in finding["geo_series_validation"]
        )
        identifier_text = "; ".join(
            filter(None, [identifiers_text, geo_status_text, ", ".join(named_sources)])
        ) or "none detected"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(number),
                    f"[{_cell(finding['title'])}]({_cell(finding['source_url'])})",
                    _cell(finding["submitted"]),
                    _cell(finding["screen_status"]),
                    _cell(identifier_text),
                    _cell(finding["experiment_status"]),
                ]
            )
            + " |"
        )
    for number, finding in enumerate(findings, start=1):
        ids = finding["dataset_identifiers"]
        terms = ", ".join(finding["treatment_terms_matched"]) or "none"
        identifiers_text = "; ".join(f"{source}: {', '.join(values)}" for source, values in ids.items())
        identifier_text = identifiers_text or "No explicit public accession detected in the extracted text."
        named_source_text = ", ".join(finding["named_data_sources"]) or "No named source detected."
        lines.extend(
            [
                "",
                f"### {number}. {finding['title']}",
                "",
                f"- arXiv: [{finding['arxiv_id']}]({finding['source_url']}); submitted {finding['submitted']}; categories: {', '.join(finding['categories']) or 'not listed'}.",
                f"- Acquisition: PDF `{finding['pdf_status']}`, text `{finding['text_status']}`.",
                f"- Transparent screen: RA phrase={finding['ra_mentioned']}; treatment terms={terms}; status=`{finding['screen_status']}`.",
                f"- Dataset readout: {identifier_text}",
                f"- Named data-source context: {named_source_text}",
                f"- Experiment decision: `{finding['experiment_status']}`.",
                f"- Boundary: {finding['clinical_boundary']}",
            ]
        )
        for record in finding["geo_series_validation"]:
            title = record["title"] or "No title extracted"
            lines.append(
                f"- GEO validation: [{record['accession']}]({record['source_url']}) — `{record['status']}`; title: {title}."
            )
            if record["error"]:
                lines.append(f"- GEO metadata error: `{record['error']}`")
        if finding["error"]:
            lines.append(f"- Acquisition error: `{finding['error']}`")
    MARKDOWN_REPORT.write_text("\n".join(lines) + "\n")


def run_loop(limit: int, request_delay_s: float) -> int:
    total_results, papers = fetch_papers(limit=limit, request_delay_s=request_delay_s)
    findings: list[dict[str, object]] = []
    for number, paper in enumerate(papers, start=1):
        pdf_status, text_status, error = download_and_extract(paper)
        text_path = TEXT_DIR / f"{safe_stem(paper.arxiv_id)}.txt"
        full_text = text_path.read_text(errors="replace") if text_path.exists() else ""
        findings.append(record_finding(paper, full_text, pdf_status, text_status, error))
        write_reports(total_results, limit, findings)
        print(f"[{number}/{len(papers)}] {paper.arxiv_id}: {findings[-1]['experiment_status']}", flush=True)
    write_reports(total_results, limit, findings)
    print(json.dumps({"source_results": total_results, "completed": len(findings), "report": str(MARKDOWN_REPORT)}))
    return 0


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=1000, help="Maximum number of unique arXiv papers to process.")
    parser.add_argument("--request-delay-s", type=float, default=3.0, help="Delay between arXiv API pages.")
    args = parser.parse_args(argv)
    if not 1 <= args.limit <= 1000:
        parser.error("--limit must be between 1 and 1000")
    if args.request_delay_s < 0:
        parser.error("--request-delay-s must be non-negative")
    return args


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(run_loop(arguments.limit, arguments.request_delay_s))
