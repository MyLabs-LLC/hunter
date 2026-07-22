#!/usr/bin/env python3
"""Build the clinician-facing CASE-RA-D2T-A research brief as a styled PDF."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


NAVY = HexColor("#102A43")
INK = HexColor("#243B53")
TEAL = HexColor("#087F8C")
TEAL_DARK = HexColor("#06636D")
MINT = HexColor("#DFF4F1")
SKY = HexColor("#E8F1FA")
CORAL = HexColor("#E76F51")
GOLD = HexColor("#E9B949")
PALE_GOLD = HexColor("#FFF4D6")
LIGHT = HexColor("#F5F8FA")
MID = HexColor("#829AB1")
LINE = HexColor("#D9E2EC")
WHITE = colors.white


def register_fonts() -> None:
    font_paths = {
        "Space": "/usr/share/fonts/truetype/space-grotesk/SpaceGrotesk-Regular.ttf",
        "SpaceBold": "/usr/share/fonts/truetype/space-grotesk/SpaceGrotesk-Bold.ttf",
        "Body": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "BodyBold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "BodyItalic": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
    }
    for name, path in font_paths.items():
        if Path(path).exists():
            pdfmetrics.registerFont(TTFont(name, path))


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="SpaceBold",
            fontSize=27,
            leading=30,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Heading2"],
            fontName="Space",
            fontSize=15,
            leading=19,
            textColor=TEAL_DARK,
            spaceAfter=12,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="SpaceBold",
            fontSize=17,
            leading=21,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=base["Heading3"],
            fontName="SpaceBold",
            fontSize=11.5,
            leading=15,
            textColor=TEAL_DARK,
            spaceBefore=10,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Body",
            fontSize=8.6,
            leading=12.3,
            textColor=INK,
            spaceAfter=6,
            allowWidows=0,
            allowOrphans=0,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Body",
            fontSize=7,
            leading=9.2,
            textColor=INK,
            spaceAfter=3,
        ),
        "tiny": ParagraphStyle(
            "Tiny",
            parent=base["BodyText"],
            fontName="Body",
            fontSize=6.25,
            leading=8.2,
            textColor=INK,
            spaceAfter=2,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["BodyText"],
            fontName="Body",
            fontSize=7.4,
            leading=10.2,
            textColor=HexColor("#486581"),
            spaceAfter=2,
        ),
        "callout": ParagraphStyle(
            "Callout",
            parent=base["BodyText"],
            fontName="BodyBold",
            fontSize=8.2,
            leading=11.4,
            textColor=NAVY,
        ),
        "table": ParagraphStyle(
            "Table",
            parent=base["BodyText"],
            fontName="Body",
            fontSize=6.8,
            leading=9.1,
            textColor=INK,
        ),
        "table_head": ParagraphStyle(
            "TableHead",
            parent=base["BodyText"],
            fontName="BodyBold",
            fontSize=6.7,
            leading=8.6,
            textColor=WHITE,
        ),
        "appendix_title": ParagraphStyle(
            "AppendixTitle",
            parent=base["Heading1"],
            fontName="SpaceBold",
            fontSize=22,
            leading=26,
            textColor=NAVY,
            spaceAfter=8,
        ),
        "source_title": ParagraphStyle(
            "SourceTitle",
            parent=base["BodyText"],
            fontName="BodyBold",
            fontSize=7.1,
            leading=9.3,
            textColor=NAVY,
            spaceAfter=2,
        ),
    }


def inline_markup(value: str) -> str:
    value = html.unescape(value.strip())
    safe = escape(value)
    safe = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<link href="\2" color="#087F8C"><u>\1</u></link>',
        safe,
    )
    safe = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", safe)
    safe = re.sub(r"`([^`]+)`", r'<font name="BodyBold" color="#486581">\1</font>', safe)
    safe = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", safe)
    return safe


def evidence_map(width: float) -> Drawing:
    height = 86
    drawing = Drawing(width, height)
    cards = [
        ("100", "PubMed", TEAL),
        ("87", "arXiv", HexColor("#3E7CB1")),
        ("14", "GEO checks", HexColor("#6956A5")),
        ("2", "response cohorts", CORAL),
        ("3", "model families", GOLD),
    ]
    gap = 8
    card_w = (width - gap * (len(cards) - 1)) / len(cards)
    for index, (number, label, color) in enumerate(cards):
        x = index * (card_w + gap)
        drawing.add(Rect(x, 10, card_w, 62, 7, 7, fillColor=LIGHT, strokeColor=color, strokeWidth=1.2))
        drawing.add(String(x + card_w / 2, 45, number, textAnchor="middle", fontName="SpaceBold", fontSize=18, fillColor=color))
        drawing.add(String(x + card_w / 2, 27, label, textAnchor="middle", fontName="Body", fontSize=6.8, fillColor=INK))
    return drawing


def confidence_badge(text: str, style: ParagraphStyle) -> Paragraph:
    lowered = text.lower()
    color = TEAL_DARK if "very" in lowered else (HexColor("#2F6B3C") if "high" in lowered else HexColor("#8A5A00"))
    return Paragraph(f'<font color="{color.hexval()}"><b>{inline_markup(text)}</b></font>', style)


def callout(text: str, style: ParagraphStyle, background=MINT, accent=TEAL) -> Table:
    table = Table([[Paragraph(inline_markup(text), style)]], colWidths=[7.08 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("BOX", (0, 0), (-1, -1), 0.6, accent),
                ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    return table


def parse_table(lines: list[str], index: int, st: dict[str, ParagraphStyle]) -> tuple[Table, int]:
    raw_rows = []
    while index < len(lines) and lines[index].strip().startswith("|"):
        raw_rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
        index += 1
    if len(raw_rows) > 1 and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in raw_rows[1]):
        raw_rows.pop(1)

    col_count = len(raw_rows[0])
    is_action_table = col_count == 4 and raw_rows[0][0].lower() == "rank"
    if is_action_table:
        widths = [0.42 * inch, 1.53 * inch, 0.86 * inch, 4.27 * inch]
    elif col_count == 4:
        widths = [1.40 * inch, 1.62 * inch, 1.72 * inch, 2.34 * inch]
    elif col_count == 3:
        widths = [2.0 * inch, 2.45 * inch, 2.63 * inch]
    else:
        widths = [7.08 * inch / col_count] * col_count

    data = []
    for row_index, row in enumerate(raw_rows):
        cells = []
        for col_index, cell in enumerate(row):
            if row_index == 0:
                cells.append(Paragraph(inline_markup(cell), st["table_head"]))
            elif is_action_table and col_index == 2:
                cells.append(confidence_badge(cell, st["table"]))
            else:
                cells.append(Paragraph(inline_markup(cell), st["table"]))
        data.append(cells)

    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for row_index in range(1, len(data)):
        commands.append(("BACKGROUND", (0, row_index), (-1, row_index), WHITE if row_index % 2 else LIGHT))
    if is_action_table:
        commands.extend(
            [
                ("ALIGN", (0, 1), (0, -1), "CENTER"),
                ("FONTNAME", (0, 1), (0, -1), "SpaceBold"),
                ("FONTSIZE", (0, 1), (0, -1), 11),
                ("TEXTCOLOR", (0, 1), (0, -1), TEAL_DARK),
            ]
        )
    table.setStyle(TableStyle(commands))
    return table, index


def parse_markdown(path: Path, st: dict[str, ParagraphStyle]) -> list:
    lines = path.read_text(encoding="utf-8").splitlines()
    story = []
    index = 0
    title_seen = False
    subtitle_seen = False
    pagebreak_sections = {
        "What the local experiments taught us",
        "What the research documents collectively taught us",
        "Research opportunities for an RA investigator",
        "Key references",
    }
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("# ") and not title_seen:
            story.append(Spacer(1, 7))
            story.append(Paragraph(inline_markup(line[2:]), st["title"]))
            title_seen = True
            index += 1
            continue
        if line.startswith("## ") and not subtitle_seen:
            story.append(Paragraph(inline_markup(line[3:]), st["subtitle"]))
            story.append(evidence_map(7.08 * inch))
            story.append(Spacer(1, 5))
            subtitle_seen = True
            index += 1
            continue
        if line.startswith("## "):
            heading = line[3:].strip()
            if heading in pagebreak_sections:
                story.append(PageBreak())
            story.append(Paragraph(inline_markup(heading), st["h2"]))
            story.append(HRFlowable(width="100%", thickness=1.1, color=TEAL, spaceAfter=7))
            index += 1
            continue
        if line.startswith("### "):
            story.append(Paragraph(inline_markup(line[4:]), st["h3"]))
            index += 1
            continue
        if line.startswith("> "):
            story.append(callout(line[2:], st["callout"], PALE_GOLD, GOLD))
            story.append(Spacer(1, 7))
            index += 1
            continue
        if line.startswith("|"):
            table, index = parse_table(lines, index, st)
            story.append(table)
            story.append(Spacer(1, 8))
            continue
        if line.startswith("**Prepared:"):
            meta_lines = []
            while index < len(lines) and lines[index].strip().startswith(
                ("**Prepared:", "**Case:", "**Evidence reviewed:")
            ):
                meta_lines.append(Paragraph(inline_markup(lines[index].strip()), st["meta"]))
                index += 1
            meta_table = Table([[item] for item in meta_lines], colWidths=[7.08 * inch])
            meta_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                        ("BOX", (0, 0), (-1, -1), 0.4, LINE),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ]
                )
            )
            story.append(meta_table)
            story.append(Spacer(1, 7))
            continue
        if re.match(r"^\d+\.\s", line):
            items = []
            while index < len(lines) and re.match(r"^\d+\.\s", lines[index].strip()):
                item = re.sub(r"^\d+\.\s+", "", lines[index].strip())
                items.append(ListItem(Paragraph(inline_markup(item), st["body"]), leftIndent=12))
                index += 1
            story.append(ListFlowable(items, bulletType="1", start="1", leftIndent=18, bulletFontName="SpaceBold", bulletColor=TEAL_DARK))
            story.append(Spacer(1, 4))
            continue
        if line.startswith("- "):
            items = []
            while index < len(lines) and lines[index].strip().startswith("- "):
                item = lines[index].strip()[2:]
                items.append(ListItem(Paragraph(inline_markup(item), st["body"]), leftIndent=11))
                index += 1
            story.append(ListFlowable(items, bulletType="bullet", start="circle", leftIndent=18, bulletFontName="Body", bulletColor=TEAL))
            story.append(Spacer(1, 4))
            continue

        paragraph_lines = [line]
        index += 1
        while index < len(lines):
            candidate = lines[index].strip()
            if not candidate or candidate.startswith(("#", ">", "|", "- ")) or re.match(r"^\d+\.\s", candidate):
                break
            paragraph_lines.append(candidate)
            index += 1
        paragraph = " ".join(paragraph_lines)
        style = st["meta"] if paragraph.startswith("**Prepared:") or paragraph.startswith("**Case:") or paragraph.startswith("**Evidence reviewed:") else st["body"]
        story.append(Paragraph(inline_markup(paragraph), style))
    return story


def source_contribution(record: dict) -> str:
    topic = record.get("source_topic", "")
    design = record.get("evidence_design", "research").replace("_", " ")
    topic_text = {
        "remission_and_treat_to_target": "remission definitions, D2T framing, or treat-to-target implementation",
        "treatment_sequence_and_precision": "mechanism sequencing, treatment response, biomarkers, or precision medicine",
        "ibd_overlap_and_safety": "comorbidity, IBD overlap, cardiovascular risk, infection, or treatment safety",
        "diet_and_nutrition": "diet, nutrition, supplements, or microbiome evidence",
        "lifestyle_and_function": "exercise, function, smoking, sleep, weight, or stress evidence",
    }.get(topic, "RA context")
    lead = {
        "guideline": "Formal guidance informing",
        "systematic_review_or_meta_analysis": "Evidence synthesis informing",
        "randomized_trial": "Controlled trial evidence informing",
        "clinical_trial": "Clinical trial evidence informing",
        "observational_or_registry": "Population/registry evidence informing",
        "review": "Review used to map",
    }.get(record.get("evidence_design"), "Peer-reviewed evidence informing")
    return f"{lead} {topic_text}. Routed as {design}; applicability was limited to the population and design reported."


def add_pubmed_appendix(story: list, report_path: Path, st: dict[str, ParagraphStyle]) -> None:
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    story.append(PageBreak())
    story.append(Paragraph("Appendix A", st["appendix_title"]))
    story.append(Paragraph("Complete 100-document PubMed review catalogue", st["subtitle"]))
    story.append(
        callout(
            "All entries are distinct by PMID and normalized title. The catalogue records what each document contributed to the review; it does not convert every paper into a treatment recommendation.",
            st["callout"],
            SKY,
            HexColor("#3E7CB1"),
        )
    )
    story.append(Spacer(1, 9))
    for record in payload["records"]:
        number = record["iteration"]
        title = inline_markup(record["title"])
        url = f"https://pubmed.ncbi.nlm.nih.gov/{record['pmid']}/"
        meta = (
            f"PMID {record['pmid']}  •  {record.get('year') or 'year n/a'}  •  "
            f"{record.get('evidence_design', '').replace('_', ' ')}  •  "
            f"{record.get('source_topic', '').replace('_', ' ')}"
        )
        block = Table(
            [
                [
                    Paragraph(f'<font color="#087F8C"><b>{number:03d}</b></font>', st["source_title"]),
                    Paragraph(f'<link href="{url}" color="#102A43"><b>{title}</b></link>', st["source_title"]),
                ],
                ["", Paragraph(inline_markup(meta), st["tiny"])],
                ["", Paragraph(inline_markup(source_contribution(record)), st["tiny"])],
            ],
            colWidths=[0.42 * inch, 6.66 * inch],
        )
        block.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE if number % 2 else LIGHT),
                    ("LINEBELOW", (0, -1), (-1, -1), 0.35, LINE),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ("SPAN", (0, 0), (0, 2)),
                ]
            )
        )
        story.append(KeepTogether([block, Spacer(1, 2)]))


def arxiv_contribution(record: dict) -> str:
    status = record.get("experiment_status", "")
    screen = record.get("screen_status", "")
    if status == "named_registry_not_runnable_locally":
        return "Direct response-research lead, but the named registry was not supplied as a reproducible public patient-level dataset."
    if "geo" in status:
        return "Dataset accession(s) were checked; the identified series did not meet the public baseline RA treatment-response contract."
    if "dataset_contract_required" in status or "named_source_requires" in status:
        return "Potential data lead retained for audit; population, exposure, baseline, outcome, or access requirements were incomplete."
    if screen == "candidate_ra_treatment_research":
        return "Treatment-relevant paper read for hypothesis generation; no compatible public response dataset or patient-level treatment proof was established."
    return "Read and excluded from direct treatment-response evidence because RA treatment was background, incidental, preclinical, diagnostic, or otherwise out of scope."


def add_arxiv_appendix(story: list, report_path: Path, st: dict[str, ParagraphStyle]) -> None:
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    story.append(PageBreak())
    story.append(Spacer(1, 24))
    story.append(Paragraph("Appendix B", st["appendix_title"]))
    story.append(Paragraph("Complete 87-paper arXiv review catalogue", st["subtitle"]))
    story.append(
        callout(
            "The broad arXiv source was exhausted at 87 unique results. Thirty-three papers met the transparent treatment screen; no new compatible public baseline treatment-response cohort was identified.",
            st["callout"],
            MINT,
            TEAL,
        )
    )
    story.append(Spacer(1, 9))
    for number, record in enumerate(payload["findings"], start=1):
        title = inline_markup(record["title"])
        url = record.get("source_url", "")
        submitted = record.get("submitted", "")[:10]
        status = record.get("screen_status", "").replace("_", " ")
        meta = f"arXiv {record.get('arxiv_id', '')}  •  {submitted}  •  {status}"
        block = Table(
            [
                [
                    Paragraph(f'<font color="#6956A5"><b>{number:03d}</b></font>', st["source_title"]),
                    Paragraph(f'<link href="{url}" color="#102A43"><b>{title}</b></link>', st["source_title"]),
                ],
                ["", Paragraph(inline_markup(meta), st["tiny"])],
                ["", Paragraph(inline_markup(arxiv_contribution(record)), st["tiny"])],
            ],
            colWidths=[0.42 * inch, 6.66 * inch],
        )
        block.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE if number % 2 else HexColor("#F8F6FC")),
                    ("LINEBELOW", (0, -1), (-1, -1), 0.35, LINE),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ("SPAN", (0, 0), (0, 2)),
                ]
            )
        )
        story.append(KeepTogether([block, Spacer(1, 2)]))
    story.append(Spacer(1, 16))
    story.append(
        callout(
            "Closing research message: the most useful idea to spread is a better evidence contract—objective inflammation, explicit treatment-failure labels, coordinated RA–IBD outcomes, complete safety variables, and independent validation. That foundation is more likely to improve remission research than another unvalidated small-cohort model or cure claim.",
            st["callout"],
            PALE_GOLD,
            GOLD,
        )
    )
    story.append(Spacer(1, 10))
    story.append(evidence_map(7.08 * inch))


def page_decor(canvas, doc, first: bool = False) -> None:
    canvas.saveState()
    width, height = letter
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 18, width, 18, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, height - 22, width, 4, fill=1, stroke=0)
    if not first:
        canvas.setFont("Space", 7)
        canvas.setFillColor(HexColor("#486581"))
        canvas.drawString(0.55 * inch, height - 0.42 * inch, "CASE-RA-D2T-A  /  CLINICIAN & RESEARCHER BRIEF")
    canvas.setStrokeColor(LINE)
    canvas.line(0.55 * inch, 0.45 * inch, width - 0.55 * inch, 0.45 * inch)
    canvas.setFont("Body", 6.5)
    canvas.setFillColor(HexColor("#627D98"))
    canvas.drawString(0.55 * inch, 0.27 * inch, "De-identified research aid • Not medical advice or a prescription")
    canvas.drawRightString(width - 0.55 * inch, 0.27 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build(source: Path, pubmed: Path, arxiv: Path, output: Path) -> None:
    register_fonts()
    st = styles()
    story = parse_markdown(source, st)
    add_pubmed_appendix(story, pubmed, st)
    add_arxiv_appendix(story, arxiv, st)
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output),
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.58 * inch,
        bottomMargin=0.58 * inch,
        title="CASE-RA-D2T-A: Clinician & Researcher Brief",
        author="MyLabs research harness",
        subject="De-identified rheumatoid arthritis remission research briefing",
        creator="Local CASE-RA-D2T-A evidence harness",
    )
    doc.build(
        story,
        onFirstPage=lambda canvas, current_doc: page_decor(canvas, current_doc, first=True),
        onLaterPages=lambda canvas, current_doc: page_decor(canvas, current_doc, first=False),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--pubmed", type=Path, required=True)
    parser.add_argument("--arxiv", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.source, args.pubmed, args.arxiv, args.output)


if __name__ == "__main__":
    main()
