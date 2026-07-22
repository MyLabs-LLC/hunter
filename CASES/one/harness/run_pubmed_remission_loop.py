#!/usr/bin/env python3
"""Run a fixed 100-source PubMed evidence-acquisition loop for CASE-RA-D2T-A.

The loop reads unique abstracts, caches available PubMed Central full text, and
emits an auditable source manifest. It does not infer or prescribe treatment.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import date
from pathlib import Path


BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
USER_AGENT = "CASE-RA-D2T-A-research-harness/1.0 (local research audit)"
PREVIOUSLY_REVIEWED_PMIDS = {"27654603", "33854570", "39288740", "41826212"}

TOPIC_QUERIES = [
    (
        "remission_and_treat_to_target",
        25,
        'RA_FILTER AND '
        '(remission[Title] OR "treat to target"[Title] OR '
        '"difficult to treat"[Title])',
    ),
    (
        "treatment_sequence_and_precision",
        25,
        'RA_FILTER AND '
        '(biologic*[Title] OR DMARD*[Title] OR '
        '"treatment response"[Title] OR "precision medicine"[Title] '
        'OR "mechanism of action"[Title])',
    ),
    (
        "ibd_overlap_and_safety",
        20,
        'RA_FILTER AND '
        '("inflammatory bowel disease"[Title] OR Crohn*[Title] '
        'OR "ulcerative colitis"[Title] OR cardiovascular[Title] '
        'OR infection*[Title] OR safety[Title])',
    ),
    (
        "diet_and_nutrition",
        15,
        'RA_FILTER AND '
        '(diet*[Title] OR nutrition*[Title] OR '
        'Mediterranean[Title] OR "omega-3"[Title] OR '
        'supplement*[Title] OR microbiome[Title])',
    ),
    (
        "lifestyle_and_function",
        15,
        'RA_FILTER AND '
        '(exercise[Title] OR "physical activity"[Title] OR '
        'smoking[Title] OR sleep[Title] OR obesity[Title] '
        'OR weight[Title] OR stress[Title])',
    ),
]

RA_FILTER = '("Arthritis, Rheumatoid"[MeSH Terms] OR "rheumatoid arthritis"[Title])'
DATE_FILTER = '("2010/01/01"[Date - Publication] : "3000"[Date - Publication])'
HUMAN_EVIDENCE_FILTER = (
    '(Humans[MeSH Terms] OR Review[Publication Type] OR Meta-Analysis[Publication Type] '
    'OR Systematic Review[Publication Type] OR Guideline[Publication Type] '
    'OR Clinical Trial[Publication Type]) NOT (Animals[MeSH Terms] NOT Humans[MeSH Terms])'
)

QUALIFY_TERMS = {
    "remission_and_treat_to_target": ("remission", "treat-to-target", "treat to target", "difficult-to-treat", "difficult to treat"),
    "treatment_sequence_and_precision": ("biologic", "dmard", "treatment response", "precision medicine", "mechanism of action", "switch", "refractory"),
    "ibd_overlap_and_safety": ("inflammatory bowel", "crohn", "ulcerative colitis", "cardiovascular", "infection", "safety"),
    "diet_and_nutrition": ("diet", "nutrition", "mediterranean", "omega-3", "supplement", "microbiome"),
    "lifestyle_and_function": ("exercise", "physical activity", "smoking", "sleep", "obesity", "weight", "stress"),
}

TOPIC_TERMS = {
    "remission": ("remission", "low disease activity", "treat-to-target", "treat to target"),
    "difficult_to_treat": ("difficult-to-treat", "difficult to treat", "refractory"),
    "treatment_response": ("response", "dmard", "biologic", "inhibitor", "therapy", "treatment"),
    "precision_or_biomarker": ("biomarker", "precision", "predict", "pathotype", "synovial"),
    "ibd_overlap": ("inflammatory bowel", "crohn", "ulcerative colitis"),
    "safety": ("safety", "infection", "cardiovascular", "malignancy", "thromb", "adverse"),
    "diet_or_nutrition": ("diet", "nutrition", "mediterranean", "omega-3", "supplement", "microbiome"),
    "exercise_or_activity": ("exercise", "physical activity", "aerobic", "resistance training"),
    "weight_or_obesity": ("obesity", "overweight", "body mass index", "weight loss"),
    "smoking": ("smoking", "smoker", "tobacco"),
    "sleep_or_stress": ("sleep", "stress", "mindfulness", "fatigue"),
}


def request_bytes(url: str, max_bytes: int | None = None) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read((max_bytes + 1) if max_bytes else None)
    if max_bytes and len(data) > max_bytes:
        raise ValueError(f"response exceeded {max_bytes} bytes")
    return data


def search(query: str, retmax: int = 250) -> list[str]:
    query = query.replace("RA_FILTER", RA_FILTER)
    params = urllib.parse.urlencode(
        {
            "db": "pubmed",
            "term": f"({query}) AND {DATE_FILTER} AND {HUMAN_EVIDENCE_FILTER}",
            "retmax": str(retmax),
            "sort": "relevance",
            "retmode": "json",
        }
    )
    payload = json.loads(request_bytes(f"{BASE}/esearch.fcgi?{params}"))
    return payload["esearchresult"]["idlist"]


def fetch_records(pmids: list[str]) -> dict[str, dict]:
    if not pmids:
        return {}
    params = urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"}
    )
    root = ET.fromstring(request_bytes(f"{BASE}/efetch.fcgi?{params}"))
    records: dict[str, dict] = {}
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//MedlineCitation/PMID", default="").strip()
        title_node = article.find(".//ArticleTitle")
        title = "" if title_node is None else "".join(title_node.itertext())
        abstract_parts = []
        for node in article.findall(".//Abstract/AbstractText"):
            label = node.attrib.get("Label", "").strip()
            text = "".join(node.itertext()).strip()
            abstract_parts.append(f"{label}: {text}" if label else text)
        abstract = " ".join(abstract_parts)
        journal = article.findtext(".//Article/Journal/Title", default="").strip()
        year = (
            article.findtext(".//Article/Journal/JournalIssue/PubDate/Year", default="").strip()
            or article.findtext(".//ArticleDate/Year", default="").strip()
            or article.findtext(".//DateCompleted/Year", default="").strip()
        )
        publication_types = [
            "".join(node.itertext()).strip()
            for node in article.findall(".//PublicationTypeList/PublicationType")
        ]
        ids = {
            node.attrib.get("IdType", ""): (node.text or "").strip()
            for node in article.findall(".//PubmedData/ArticleIdList/ArticleId")
        }
        records[pmid] = {
            "pmid": pmid,
            "title": html.unescape(re.sub(r"\s+", " ", title)).strip(),
            "abstract": html.unescape(re.sub(r"\s+", " ", abstract)).strip(),
            "journal": journal,
            "year": year,
            "publication_types": publication_types,
            "doi": ids.get("doi", ""),
            "pmcid": ids.get("pmc", ""),
        }
    return records


def evidence_design(publication_types: list[str], title: str) -> str:
    values = " ".join(publication_types).lower() + " " + title.lower()
    if "practice guideline" in values or "guideline" in values:
        return "guideline"
    if "meta-analysis" in values or "systematic review" in values:
        return "systematic_review_or_meta_analysis"
    if "randomized controlled trial" in values or "randomised" in values or "randomized" in values:
        return "randomized_trial"
    if "clinical trial" in values:
        return "clinical_trial"
    if "review" in values:
        return "review"
    if "observational" in values or "cohort" in values or "registry" in values:
        return "observational_or_registry"
    return "other_peer_reviewed_research"


def detected_topics(title: str, abstract: str) -> list[str]:
    text = f"{title} {abstract}".lower()
    return [name for name, terms in TOPIC_TERMS.items() if any(term in text for term in terms)]


def cache_full_text(record: dict, fulltext_dir: Path) -> tuple[str, int]:
    pmcid = record["pmcid"]
    if not pmcid:
        return "not_in_pubmed_central", 0
    path = fulltext_dir / f"{pmcid}.xml"
    if path.exists():
        return "cached", path.stat().st_size
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    try:
        data = request_bytes(url, max_bytes=15 * 1024 * 1024)
        ET.fromstring(data)
        path.write_bytes(data)
        return "downloaded", len(data)
    except Exception as exc:  # acquisition failures belong in the audit
        return f"failed:{type(exc).__name__}", 0


def choose_sources() -> list[dict]:
    chosen: list[dict] = []
    used = set(PREVIOUSLY_REVIEWED_PMIDS)
    used_titles: set[str] = set()
    for topic, quota, query in TOPIC_QUERIES:
        candidate_ids = [pmid for pmid in search(query, retmax=350) if pmid not in used]
        records = fetch_records(candidate_ids)
        topic_count = 0
        for pmid in candidate_ids:
            record = records.get(pmid)
            if not record or not record["abstract"] or pmid in used:
                continue
            normalized_title = re.sub(r"\W+", " ", record["title"].lower()).strip()
            if not normalized_title or normalized_title in used_titles:
                continue
            searchable = f"{record['title']} {record['abstract']}".lower()
            if "rheumatoid arthritis" not in searchable:
                continue
            if not any(term in searchable for term in QUALIFY_TERMS[topic]):
                continue
            record["source_topic"] = topic
            record["source_query"] = query
            chosen.append(record)
            used.add(pmid)
            used_titles.add(normalized_title)
            topic_count += 1
            if topic_count == quota:
                break
        if topic_count != quota:
            raise RuntimeError(f"topic {topic} supplied {topic_count}/{quota} readable unique abstracts")
        time.sleep(0.35)
    if len(chosen) != 100:
        raise RuntimeError(f"expected exactly 100 sources, got {len(chosen)}")
    return chosen


def write_outputs(records: list[dict], report_dir: Path, research_dir: Path) -> None:
    fulltext_dir = research_dir / "fulltext"
    fulltext_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    for index, record in enumerate(records, start=1):
        record["iteration"] = index
        record["evidence_design"] = evidence_design(record["publication_types"], record["title"])
        record["detected_topics"] = detected_topics(record["title"], record["abstract"])
        record["abstract_characters_read"] = len(record["abstract"])
        status, byte_count = cache_full_text(record, fulltext_dir)
        record["full_text_status"] = status
        record["full_text_bytes_cached"] = byte_count
        print(f"iteration {index:03d}/100 PMID {record['pmid']} {status}", flush=True)
        time.sleep(0.34)

    raw_xml_note = research_dir / "README.md"
    raw_xml_note.write_text(
        "Locally cached PubMed Central full text for the 100-source evidence loop.\n"
        "This directory is intentionally ignored by Git.\n",
        encoding="utf-8",
    )
    (research_dir / "abstract_records.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    manifest_records = []
    for record in records:
        manifest_records.append({key: value for key, value in record.items() if key != "abstract"})

    payload = {
        "case": "CASE-RA-D2T-A",
        "run_date": date.today().isoformat(),
        "iteration_budget": 100,
        "completed_iterations": len(records),
        "unique_pmids": len({record["pmid"] for record in records}),
        "unique_normalized_titles": len(
            {re.sub(r"\W+", " ", record["title"].lower()).strip() for record in records}
        ),
        "previously_reviewed_pmids_excluded": sorted(PREVIOUSLY_REVIEWED_PMIDS),
        "date_filter": DATE_FILTER,
        "topic_targets": {topic: quota for topic, quota, _ in TOPIC_QUERIES},
        "evidence_design_counts": dict(Counter(record["evidence_design"] for record in records)),
        "full_text_status_counts": dict(Counter(record["full_text_status"] for record in records)),
        "total_abstract_characters_read": sum(record["abstract_characters_read"] for record in records),
        "records": manifest_records,
        "clinical_status": "research evidence triage only; no treatment prescription or cure claim",
    }
    (report_dir / "pubmed_100_loop.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    lines = [
        "# PubMed 100-source RA remission evidence loop",
        "",
        f"**Run date:** {payload['run_date']}  ",
        "**Case:** `CASE-RA-D2T-A`  ",
        f"**Budget/completed:** 100/{len(records)} unique PubMed sources  ",
        "**Boundary:** source-acquisition audit only; not medical advice, treatment selection, or proof of cure.",
        "",
        "## Acquisition contract",
        "",
        "The loop selected unique, RA-indexed human clinical sources or evidence reviews with readable abstracts from five predeclared query families, ranked by PubMed relevance. Previously reviewed PMIDs were excluded. PubMed Central full text was also read and cached locally when available; raw full text is ignored by Git.",
        "",
        "| Query family | Target | Completed |",
        "| --- | ---: | ---: |",
    ]
    actual_topics = Counter(record["source_topic"] for record in records)
    for topic, quota, _ in TOPIC_QUERIES:
        lines.append(f"| `{topic}` | {quota} | {actual_topics[topic]} |")
    lines.extend(
        [
            "",
            f"Total abstract text read: {payload['total_abstract_characters_read']:,} characters. Evidence-design counts: "
            + ", ".join(f"{key}={value}" for key, value in sorted(payload["evidence_design_counts"].items()))
            + ".",
            "",
            "## Per-iteration source record",
            "",
            "| # | Query family | Source | Year | Design | Full text | Detected relevance |",
            "| ---: | --- | --- | ---: | --- | --- | --- |",
        ]
    )
    for record in records:
        title = record["title"].replace("|", "\\|")
        link = f"https://pubmed.ncbi.nlm.nih.gov/{record['pmid']}/"
        relevance = ", ".join(record["detected_topics"]) or "general_ra_context"
        lines.append(
            f"| {record['iteration']} | `{record['source_topic']}` | "
            f"[{title}]({link}) (PMID {record['pmid']}) | {record['year'] or 'n/a'} | "
            f"`{record['evidence_design']}` | `{record['full_text_status']}` | {relevance} |"
        )
    lines.extend(
        [
            "",
            "## Stop condition",
            "",
            "The loop stopped at the hard budget after 100 unique additional sources. This manifest records acquisition and coarse routing; claim-level interpretation, applicability, contradictions, and the case-specific remission discussion are kept in `case_remission_report.md`.",
            "",
        ]
    )
    (report_dir / "pubmed_100_loop.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-dir", type=Path, required=True)
    parser.add_argument("--research-dir", type=Path, required=True)
    args = parser.parse_args()
    records = choose_sources()
    write_outputs(records, args.report_dir, args.research_dir)


if __name__ == "__main__":
    main()
