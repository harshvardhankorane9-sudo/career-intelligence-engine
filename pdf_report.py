"""
Career Intelligence Engine — PDF Report Generator
Generates a polished, downloadable student analysis PDF.

Usage (from app_final.py):
    from pdf_report import generate_report_pdf
    pdf_bytes = generate_report_pdf(student, asmt_results, sim_results)
    st.download_button("Download PDF", pdf_bytes, "cie_report.pdf", "application/pdf")
"""

import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, HRFlowable, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, KeepTogether,
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.barcharts import HorizontalBarChart

# ─────────────────────────────────────────────────────────────────────────────
# Brand palette
# ─────────────────────────────────────────────────────────────────────────────
INDIGO       = colors.HexColor("#4f46e5")
INDIGO_LIGHT = colors.HexColor("#e0e7ff")
PURPLE       = colors.HexColor("#7c3aed")
SLATE_800    = colors.HexColor("#1e293b")
SLATE_600    = colors.HexColor("#475569")
SLATE_400    = colors.HexColor("#94a3b8")
SLATE_100    = colors.HexColor("#f1f5f9")
WHITE        = colors.white
GREEN        = colors.HexColor("#22c55e")
AMBER        = colors.HexColor("#f59e0b")
RED          = colors.HexColor("#ef4444")

BRANCH_HEX = {
    "CSE": "#4f46e5", "CSE-AIML": "#7c3aed",
    "MECH": "#d97706", "ECE": "#0891b2",
    "CIVIL": "#059669", "CHEM": "#dc2626",
    "BME": "#db2777", "AERO": "#6d28d9",
}
BRANCH_EMOJI_MAP = {
    "CSE": "💻", "CSE-AIML": "🤖", "MECH": "⚙️", "ECE": "🔌",
    "CIVIL": "🏗", "CHEM": "⚗", "BME": "🏥", "AERO": "🚀",
}

# ─────────────────────────────────────────────────────────────────────────────
# Styles
# ─────────────────────────────────────────────────────────────────────────────
def _styles():
    base = getSampleStyleSheet()
    return {
        "h1": ParagraphStyle("h1", fontSize=22, textColor=WHITE,
                             fontName="Helvetica-Bold", leading=28,
                             alignment=TA_CENTER),
        "h2": ParagraphStyle("h2", fontSize=15, textColor=INDIGO,
                             fontName="Helvetica-Bold", leading=20,
                             spaceAfter=4),
        "h3": ParagraphStyle("h3", fontSize=11, textColor=SLATE_800,
                             fontName="Helvetica-Bold", leading=15),
        "body": ParagraphStyle("body", fontSize=9, textColor=SLATE_600,
                               fontName="Helvetica", leading=14),
        "small": ParagraphStyle("small", fontSize=8, textColor=SLATE_400,
                                fontName="Helvetica", leading=11),
        "label": ParagraphStyle("label", fontSize=8, textColor=SLATE_600,
                                fontName="Helvetica-Bold", leading=11,
                                spaceAfter=1),
        "value": ParagraphStyle("value", fontSize=10, textColor=SLATE_800,
                                fontName="Helvetica", leading=14),
        "tag": ParagraphStyle("tag", fontSize=8, textColor=WHITE,
                              fontName="Helvetica-Bold", leading=10,
                              alignment=TA_CENTER),
        "center": ParagraphStyle("center", fontSize=9, textColor=SLATE_600,
                                 fontName="Helvetica", leading=14,
                                 alignment=TA_CENTER),
        "footer": ParagraphStyle("footer", fontSize=7, textColor=SLATE_400,
                                 fontName="Helvetica", leading=9,
                                 alignment=TA_CENTER),
    }

# ─────────────────────────────────────────────────────────────────────────────
# Page template with header/footer
# ─────────────────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm

def _header_footer(canvas, doc):
    canvas.saveState()
    # Top accent bar (skip cover page which draws its own)
    if doc.page > 1:
        canvas.setFillColor(INDIGO)
        canvas.rect(0, PAGE_H - 8 * mm, PAGE_W, 8 * mm, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawString(MARGIN, PAGE_H - 5.5 * mm, "Career Intelligence Engine")
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 5.5 * mm,
                               f"Student Analysis Report")

    # Bottom footer
    canvas.setFillColor(SLATE_100)
    canvas.rect(0, 0, PAGE_W, 10 * mm, fill=1, stroke=0)
    canvas.setFillColor(SLATE_400)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(MARGIN, 3.5 * mm, "Confidential — generated for personal use only")
    canvas.drawRightString(PAGE_W - MARGIN, 3.5 * mm, f"Page {doc.page}")
    canvas.restoreState()

# ─────────────────────────────────────────────────────────────────────────────
# Helper: horizontal progress bar drawing
# ─────────────────────────────────────────────────────────────────────────────
def _bar_drawing(value: float, max_val: float, bar_color: colors.Color,
                 width=380, height=14) -> Drawing:
    pct = min(value / max_val, 1.0) if max_val else 0
    d = Drawing(width, height)
    # Background track
    d.add(Rect(0, 2, width, height - 4, fillColor=SLATE_100, strokeColor=None))
    # Fill
    fill_w = max(pct * width, 4)
    d.add(Rect(0, 2, fill_w, height - 4, fillColor=bar_color, strokeColor=None))
    return d

# ─────────────────────────────────────────────────────────────────────────────
# Helper: skill bars drawing (horizontal bar chart)
# ─────────────────────────────────────────────────────────────────────────────
def _skills_drawing(skill_scores: dict, width=460, row_h=20) -> Drawing:
    items = sorted(skill_scores.items(), key=lambda x: -x[1])
    h = len(items) * row_h + 10
    d = Drawing(width, h)
    label_w = 160
    bar_area = width - label_w - 50  # leave room for value

    for i, (skill, score) in enumerate(items):
        y = h - (i + 1) * row_h + 4
        label = skill.replace("_", " ").title()
        # Label
        d.add(String(0, y + 4, label, fontSize=8,
                     fontName="Helvetica", fillColor=SLATE_600))
        # Track
        d.add(Rect(label_w, y + 2, bar_area, row_h - 8,
                   fillColor=SLATE_100, strokeColor=None))
        # Fill
        fill_w = max((score / 10) * bar_area, 3)
        d.add(Rect(label_w, y + 2, fill_w, row_h - 8,
                   fillColor=INDIGO, strokeColor=None))
        # Score text
        d.add(String(label_w + bar_area + 6, y + 4, f"{score:.1f}/10",
                     fontSize=8, fontName="Helvetica-Bold", fillColor=SLATE_800))
    return d

# ─────────────────────────────────────────────────────────────────────────────
# Helper: colored badge paragraph
# ─────────────────────────────────────────────────────────────────────────────
def _badge_table(text: str, bg_hex: str, styles: dict) -> Table:
    bg = colors.HexColor(bg_hex)
    cell = Paragraph(text, styles["tag"])
    t = Table([[cell]], colWidths=[2.5 * cm], rowHeights=[0.55 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("ROUNDEDCORNERS", [4]),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",   (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 3),
    ]))
    return t

# ─────────────────────────────────────────────────────────────────────────────
# Cover page
# ─────────────────────────────────────────────────────────────────────────────
def _cover_elements(student: dict, asmt_results: dict, styles: dict) -> list:
    elems = []

    # Full-width hero block built as a table
    top_branch = ""
    match_pct  = 0
    if asmt_results:
        branches = asmt_results.get("recommended_branches", [])
        if branches:
            top_branch = branches[0].get("name", "")
            match_pct  = branches[0].get("match_pct", 0)

    name_text  = student.get("name", "Student")
    date_str   = datetime.now().strftime("%d %B %Y")
    asmt_id    = asmt_results.get("assessment_id", "—") if asmt_results else "—"
    conf       = asmt_results.get("confidence", 0) if asmt_results else 0

    # Hero banner
    hero_data = [[
        Paragraph("Career Intelligence Engine", ParagraphStyle(
            "hero_title", fontSize=20, textColor=WHITE,
            fontName="Helvetica-Bold", alignment=TA_CENTER, leading=24)),
    ], [
        Paragraph("Student Analysis Report", ParagraphStyle(
            "hero_sub", fontSize=11, textColor=colors.HexColor("#c7d2fe"),
            fontName="Helvetica", alignment=TA_CENTER, leading=16)),
    ]]
    hero = Table(hero_data, colWidths=[PAGE_W - 2 * MARGIN])
    hero.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), INDIGO),
        ("TOPPADDING",    (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ("LEFTPADDING",   (0, 0), (-1, -1), 20),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 20),
        ("ROWBACKGROUNDS",(0, 0), (-1, -1), [INDIGO]),
    ]))
    elems.append(Spacer(1, 0.5 * cm))
    elems.append(hero)
    elems.append(Spacer(1, 0.8 * cm))

    # Student info card
    info_rows = [
        [Paragraph("Name",    styles["label"]), Paragraph(name_text, styles["h3"])],
        [Paragraph("Email",   styles["label"]), Paragraph(student.get("email", "—"), styles["value"])],
        [Paragraph("College", styles["label"]), Paragraph(student.get("college", "—") or "—", styles["value"])],
        [Paragraph("Year",    styles["label"]), Paragraph(f"Year {student.get('branch_year', '—')}", styles["value"])],
        [Paragraph("Report Date", styles["label"]), Paragraph(date_str, styles["value"])],
        [Paragraph("Assessment ID", styles["label"]), Paragraph(str(asmt_id), styles["value"])],
    ]
    info_t = Table(info_rows, colWidths=[3.5 * cm, PAGE_W - 2 * MARGIN - 3.5 * cm])
    info_t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), SLATE_100),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS",(0, 0), (-1, -1), [WHITE, SLATE_100]),
        ("LINEBELOW",     (0, -1), (-1, -1), 0.5, SLATE_400),
    ]))
    elems.append(info_t)
    elems.append(Spacer(1, 0.8 * cm))

    # Summary banner
    if top_branch:
        summary_rows = [[
            Paragraph("Top Branch Match", styles["label"]),
            Paragraph(f"{top_branch}", styles["h3"]),
            Paragraph(f"{match_pct:.0f}% match", ParagraphStyle(
                "match", fontSize=16, fontName="Helvetica-Bold",
                textColor=GREEN, alignment=TA_RIGHT)),
        ], [
            Paragraph("Confidence Score", styles["label"]),
            Paragraph(f"{conf * 100:.0f}%", ParagraphStyle(
                "conf", fontSize=13, fontName="Helvetica-Bold",
                textColor=INDIGO)),
            Paragraph("", styles["body"]),
        ]]
        summary_t = Table(summary_rows,
                          colWidths=[3.5 * cm, 9 * cm, 4 * cm])
        summary_t.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, -1), INDIGO_LIGHT),
            ("TOPPADDING",   (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 8),
            ("LEFTPADDING",  (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elems.append(summary_t)

    elems.append(Spacer(1, 0.6 * cm))
    elems.append(Paragraph(
        "This report summarises your skill profile, branch compatibility scores, and simulator "
        "performance as assessed by the Career Intelligence Engine. Use it to guide your "
        "engineering branch selection and counselling discussions.",
        styles["body"]))
    elems.append(Spacer(1, 0.4 * cm))
    elems.append(HRFlowable(width="100%", thickness=0.5, color=SLATE_400))
    return elems

# ─────────────────────────────────────────────────────────────────────────────
# Skill profile section
# ─────────────────────────────────────────────────────────────────────────────
def _skills_section(asmt_results: dict, styles: dict) -> list:
    if not asmt_results:
        return []
    skill_scores = {k: v for k, v in asmt_results.get("skill_scores", {}).items() if v > 0}
    if not skill_scores:
        return []

    elems = [
        Spacer(1, 0.5 * cm),
        Paragraph("Skill Profile", styles["h2"]),
        HRFlowable(width="100%", thickness=1, color=INDIGO),
        Spacer(1, 0.3 * cm),
        Paragraph(
            "Your responses across 10 questions have been mapped to 8 engineering skill "
            "dimensions. Each score is out of 10.",
            styles["body"]),
        Spacer(1, 0.4 * cm),
    ]

    drawing = _skills_drawing(skill_scores, width=460)
    elems.append(drawing)
    elems.append(Spacer(1, 0.3 * cm))

    # Confidence callout
    conf = asmt_results.get("confidence", 0)
    conf_color = GREEN if conf >= 0.7 else AMBER if conf >= 0.5 else RED
    conf_label = "High" if conf >= 0.7 else "Moderate" if conf >= 0.5 else "Low"
    callout_data = [[
        Paragraph("Assessment Confidence", styles["label"]),
        Paragraph(f"{conf_label}  ({conf * 100:.0f}%)", ParagraphStyle(
            "cconf", fontSize=11, fontName="Helvetica-Bold",
            textColor=conf_color)),
        Paragraph(
            "Reflects how consistently your answers point to a single branch profile.",
            styles["small"]),
    ]]
    ct = Table(callout_data, colWidths=[3.8 * cm, 3.5 * cm, 9.3 * cm])
    ct.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), SLATE_100),
        ("TOPPADDING",   (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 8),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elems.append(ct)
    return elems

# ─────────────────────────────────────────────────────────────────────────────
# Branch recommendations section
# ─────────────────────────────────────────────────────────────────────────────
def _branches_section(asmt_results: dict, branch_details: dict, styles: dict) -> list:
    if not asmt_results:
        return []
    branches = asmt_results.get("recommended_branches", [])
    if not branches:
        return []

    elems = [
        Spacer(1, 0.5 * cm),
        Paragraph("Branch Recommendations", styles["h2"]),
        HRFlowable(width="100%", thickness=1, color=INDIGO),
        Spacer(1, 0.3 * cm),
        Paragraph(
            "Branches are ranked by how closely your skill profile matches each branch's "
            "requirements. Top 4 results are shown.",
            styles["body"]),
        Spacer(1, 0.4 * cm),
    ]

    medals = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"]
    for i, b in enumerate(branches[:8]):
        code    = b.get("code", "")
        pct     = b.get("match_pct", 0)
        bname   = b.get("name", code)
        expl    = b.get("explanation", "")
        hex_c   = BRANCH_HEX.get(code, "#4f46e5")
        bar_clr = colors.HexColor(hex_c)
        bd      = branch_details.get(code, {})

        # Title row
        rank_lbl = medals[i] if i < len(medals) else f"#{i+1}"
        title_row = [[
            Paragraph(f"<b>{rank_lbl}</b>", ParagraphStyle(
                "rank", fontSize=9, fontName="Helvetica-Bold",
                textColor=colors.HexColor(hex_c))),
            Paragraph(f"<b>{bname}</b>", styles["h3"]),
            Paragraph(f"<b>{pct:.0f}% match</b>", ParagraphStyle(
                "pct", fontSize=12, fontName="Helvetica-Bold",
                textColor=bar_clr, alignment=TA_RIGHT)),
        ]]
        tt = Table(title_row, colWidths=[1.2 * cm, 11 * cm, 4.5 * cm])
        tt.setStyle(TableStyle([
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",   (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 2),
        ]))

        # Progress bar
        bar = _bar_drawing(pct, 100, bar_clr, width=int(PAGE_W - 2 * MARGIN))

        # Salary row
        sal_items = []
        if bd:
            for lbl, key in [("Entry", "entry_salary"), ("Mid-level", "mid_salary"),
                              ("Senior", "senior_salary")]:
                val = bd.get(key, "—")
                sal_items.append(Paragraph(f"<b>{lbl}:</b> {val}", styles["body"]))
        sal_row = [[p] for p in sal_items] if sal_items else []

        card_content = [tt, bar, Spacer(1, 4)]
        if expl:
            card_content.append(Paragraph(expl[:300], styles["body"]))
        if bd.get("future_scope"):
            card_content.append(Spacer(1, 3))
            card_content.append(Paragraph(
                f"<b>Future Scope:</b> {bd['future_scope'][:180]}...",
                styles["small"]))
        if sal_items:
            card_content.append(Spacer(1, 3))
            sal_table = Table([[s for s in sal_items]], colWidths=[5.5 * cm] * 3)
            sal_table.setStyle(TableStyle([
                ("TOPPADDING",   (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING",(0, 0), (-1, -1), 2),
            ]))
            card_content.append(sal_table)

        card_wrapper = Table(
            [[item] for item in card_content],
            colWidths=[PAGE_W - 2 * MARGIN],
        )
        card_wrapper.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, -1), SLATE_100 if i % 2 == 0 else WHITE),
            ("LEFTPADDING",  (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING",   (0, 0), (-1, 0), 8),
            ("BOTTOMPADDING",(0, -1), (-1, -1), 10),
            ("BOX",          (0, 0), (-1, -1), 0.5, SLATE_400),
        ]))

        elems.append(KeepTogether([card_wrapper, Spacer(1, 0.25 * cm)]))

    return elems

# ─────────────────────────────────────────────────────────────────────────────
# Simulator results section
# ─────────────────────────────────────────────────────────────────────────────
def _simulator_section(sim_results: dict, styles: dict) -> list:
    if not sim_results:
        return []

    branch_name = sim_results.get("branch_name", "")
    branch_code = sim_results.get("branch_code", "")
    total       = sim_results.get("total_score", 0)
    max_s       = sim_results.get("max_score", 0)
    pct         = sim_results.get("percentage", 0)
    level       = sim_results.get("level", "")
    message     = sim_results.get("message", "")
    decisions   = sim_results.get("decisions", [])
    hex_c       = BRANCH_HEX.get(branch_code, "#4f46e5")
    bar_clr     = GREEN if pct >= 70 else AMBER if pct >= 50 else RED

    elems = [
        Spacer(1, 0.5 * cm),
        Paragraph("Day-in-the-Life Simulation Results", styles["h2"]),
        HRFlowable(width="100%", thickness=1, color=INDIGO),
        Spacer(1, 0.3 * cm),
    ]

    # Score summary row
    score_data = [[
        Paragraph("Branch Simulated", styles["label"]),
        Paragraph("Score", styles["label"]),
        Paragraph("Percentage", styles["label"]),
        Paragraph("Level", styles["label"]),
    ], [
        Paragraph(f"<b>{branch_name}</b>", styles["h3"]),
        Paragraph(f"<b>{total}/{max_s}</b>", ParagraphStyle(
            "sc", fontSize=13, fontName="Helvetica-Bold", textColor=INDIGO)),
        Paragraph(f"<b>{pct:.0f}%</b>", ParagraphStyle(
            "pctc", fontSize=13, fontName="Helvetica-Bold", textColor=bar_clr)),
        Paragraph(f"<b>{level}</b>", styles["h3"]),
    ]]
    st = Table(score_data, colWidths=[5 * cm, 3.5 * cm, 3.5 * cm, 4.7 * cm])
    st.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), INDIGO),
        ("TEXTCOLOR",    (0, 0), (-1, 0), WHITE),
        ("BACKGROUND",   (0, 1), (-1, 1), INDIGO_LIGHT),
        ("TOPPADDING",   (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 8),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("GRID",         (0, 0), (-1, -1), 0.5, SLATE_400),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elems.append(st)
    elems.append(Spacer(1, 0.3 * cm))

    if message:
        elems.append(Paragraph(f"<i>{message}</i>", styles["body"]))
        elems.append(Spacer(1, 0.3 * cm))

    # Decision breakdown table
    if decisions:
        elems.append(Paragraph("Decision Breakdown", styles["h3"]))
        elems.append(Spacer(1, 0.2 * cm))
        dec_header = [
            Paragraph("Scenario", styles["label"]),
            Paragraph("Choice Made", styles["label"]),
            Paragraph("Score", styles["label"]),
        ]
        dec_rows = [dec_header]
        for d in decisions:
            sc  = d.get("score", 0)
            sc_color = GREEN if sc >= 8 else AMBER if sc >= 5 else RED
            dec_rows.append([
                Paragraph(f"Scenario {d.get('scenario_index', 0) + 1}", styles["body"]),
                Paragraph(f"Option {d.get('choice_id', '—')}", styles["body"]),
                Paragraph(f"<b>{sc}/10</b>", ParagraphStyle(
                    "dscore", fontSize=9, fontName="Helvetica-Bold",
                    textColor=sc_color)),
            ])
        dt = Table(dec_rows, colWidths=[4 * cm, 11 * cm, 2 * cm])
        dt.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0), SLATE_800),
            ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, SLATE_100]),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("GRID",          (0, 0), (-1, -1), 0.5, SLATE_400),
        ]))
        elems.append(dt)

    return elems

# ─────────────────────────────────────────────────────────────────────────────
# Next steps / closing section
# ─────────────────────────────────────────────────────────────────────────────
def _next_steps_section(asmt_results: dict, styles: dict) -> list:
    if not asmt_results:
        return []
    branches = asmt_results.get("recommended_branches", [])
    top = branches[0].get("name", "") if branches else ""

    elems = [
        Spacer(1, 0.5 * cm),
        Paragraph("Recommended Next Steps", styles["h2"]),
        HRFlowable(width="100%", thickness=1, color=INDIGO),
        Spacer(1, 0.3 * cm),
    ]

    steps = [
        ("1. Explore your top match",
         f"Deep-dive into {top or 'your top branch'} — watch YouTube channels, "
         "read about real engineering projects, and speak to final-year students."),
        ("2. Run the Day-in-the-Life Simulator",
         "Use the Career Intelligence Engine simulator to experience a day as an "
         "engineer in your top-matched branches."),
        ("3. Check MHT-CET cutoffs",
         "Visit the Cutoffs page in the app to see which Pune colleges admit students "
         "in your percentile range for each branch."),
        ("4. Speak to a counsellor",
         "Bring this report to your school/college counsellor or an engineering career "
         "advisor for a personalised discussion."),
        ("5. Revisit your assessment",
         "Retake the assessment after 2–3 weeks of exploration to see if your scores "
         "and confidence change."),
    ]
    for title, body in steps:
        elems.append(KeepTogether([
            Paragraph(f"<b>{title}</b>", styles["h3"]),
            Paragraph(body, styles["body"]),
            Spacer(1, 0.25 * cm),
        ]))

    elems.append(Spacer(1, 0.3 * cm))
    elems.append(HRFlowable(width="100%", thickness=0.5, color=SLATE_400))
    elems.append(Spacer(1, 0.2 * cm))
    elems.append(Paragraph(
        "Generated by Career Intelligence Engine · For personal use only · "
        f"Pune & Maharashtra Engineering Counsellor · {datetime.now().strftime('%d %b %Y')}",
        styles["footer"]))
    return elems

# ─────────────────────────────────────────────────────────────────────────────
# Main public function
# ─────────────────────────────────────────────────────────────────────────────
def generate_report_pdf(
    student: dict,
    asmt_results: dict | None,
    sim_results:  dict | None = None,
    branch_details: dict | None = None,
) -> bytes:
    """
    Build and return a PDF report as bytes.

    Args:
        student       : dict with keys: name, email, college, branch_year
        asmt_results  : the dict returned by /api/v1/assessment/submit
        sim_results   : optional dict with keys: branch_name, branch_code,
                        total_score, max_score, percentage, level, message, decisions[]
        branch_details: optional dict mapping branch_code -> branch detail dict
                        (fetched from /api/v1/branches/{code})
    """
    branch_details = branch_details or {}
    buf    = io.BytesIO()
    styles = _styles()

    doc = BaseDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=1.8 * cm,
        bottomMargin=1.5 * cm,
        title="Career Intelligence Engine — Student Report",
        author="Career Intelligence Engine",
    )
    frame = Frame(
        MARGIN, 1.5 * cm,
        PAGE_W - 2 * MARGIN, PAGE_H - 3.3 * cm,
        id="main",
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame],
                                       onPage=_header_footer)])

    story = []
    story += _cover_elements(student, asmt_results, styles)
    story += _skills_section(asmt_results, styles)
    story += _branches_section(asmt_results, branch_details, styles)
    story += _simulator_section(sim_results, styles)
    story += _next_steps_section(asmt_results, styles)

    doc.build(story)
    return buf.getvalue()
