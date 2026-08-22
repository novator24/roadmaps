"""Generate strategy charts and STRAT.pdf from STRAT.md.

The script intentionally uses only matplotlib, Pillow and ReportLab so the
document can be rebuilt on a standard Python workstation without Pandoc.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
SOURCE = ROOT / "STRAT.md"
OUTPUT = ROOT / "STRAT.pdf"

NAVY = "#172A3A"
BLUE = "#276FBF"
TEAL = "#0F8B8D"
GREEN = "#2E7D5B"
RED = "#B54646"
AMBER = "#C27A16"
LIGHT = "#EEF3F7"
GRID = "#D6DEE5"
TEXT = "#1C252C"
MUTED = "#62727E"


def register_fonts() -> tuple[str, str, str]:
    candidates = [
        (
            Path(r"C:\Windows\Fonts\arial.ttf"),
            Path(r"C:\Windows\Fonts\arialbd.ttf"),
            Path(r"C:\Windows\Fonts\ariali.ttf"),
        ),
        (
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"),
        ),
    ]
    for regular, bold, italic in candidates:
        if regular.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont("StrategyRegular", str(regular)))
            pdfmetrics.registerFont(TTFont("StrategyBold", str(bold)))
            pdfmetrics.registerFont(
                TTFont("StrategyItalic", str(italic if italic.exists() else regular))
            )
            font_manager.fontManager.addfont(str(regular))
            matplotlib.rcParams["font.family"] = font_manager.FontProperties(
                fname=str(regular)
            ).get_name()
            return "StrategyRegular", "StrategyBold", "StrategyItalic"
    raise RuntimeError("A Unicode font with Cyrillic support was not found.")


REGULAR, BOLD, ITALIC = register_fonts()


def chart_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": GRID,
            "axes.labelcolor": TEXT,
            "xtick.color": MUTED,
            "ytick.color": TEXT,
            "text.color": TEXT,
            "axes.titleweight": "bold",
            "axes.titlesize": 15,
            "axes.labelsize": 10,
            "font.size": 9,
        }
    )


def save_chart(fig: plt.Figure, filename: str) -> None:
    fig.tight_layout()
    fig.savefig(ASSETS / filename, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def make_swot_chart() -> None:
    data = [
        ("Нет продукта и метрик", -100, "W"),
        ("Legal model до review", -100, "W"),
        ("Риск gambling", -100, "T"),
        ("Риск securities/VA", -100, "T"),
        ("B2B SaaS без денег", 96, "O"),
        ("Banking / sanctions KYC", -96, "T"),
        ("Необоснованные IPO-цели", -90, "W"),
        ("Oracle/security disputes", -84, "T"),
        ("Нет владельцев и бюджета", -80, "W"),
        ("Расфокусировка портфеля", -80, "W"),
        ("AI + provenance", 80, "O"),
        ("Платные B2B-пилоты", 76, "O"),
        ("Dual-tax / PE", -76, "T"),
        ("Audit / antifraud assets", 61, "S"),
        ("Связная product idea", 58, "S"),
        ("API / white-label", 58, "O"),
        ("Слабый moat", -58, "T"),
        ("Международное видение", 43, "S"),
    ]
    data = sorted(data, key=lambda item: abs(item[1]))
    labels = [item[0] for item in data]
    values = [item[1] for item in data]
    bar_colors = [GREEN if value > 0 else RED for value in values]

    fig, ax = plt.subplots(figsize=(11.5, 8))
    bars = ax.barh(labels, values, color=bar_colors, height=0.65)
    ax.axvline(0, color=NAVY, linewidth=0.8)
    ax.set_xlim(-112, 112)
    ax.set_xlabel("Единая signed-метрика приоритета (− риск / + преимущество)")
    ax.set_title("SWOT: управленческие приоритеты NOVATOR24")
    ax.grid(axis="x", color=GRID, linewidth=0.7)
    ax.spines[["top", "right", "left"]].set_visible(False)
    for bar, value in zip(bars, values):
        x = value + (2 if value > 0 else -2)
        ax.text(
            x,
            bar.get_y() + bar.get_height() / 2,
            str(abs(value)),
            va="center",
            ha="left" if value > 0 else "right",
            color=TEXT,
            fontweight="bold",
        )
    fig.text(
        0.01,
        0.005,
        "Источник: анализ novator24/roadmaps, 22.08.2026. Priority = 4 × Impact × Urgency × Confidence.",
        fontsize=7.5,
        color=MUTED,
    )
    save_chart(fig, "swot-priority.png")


def make_gap_chart() -> None:
    capabilities = [
        "Legal / compliance",
        "Product",
        "Market evidence",
        "Banking / finance",
        "Security / privacy",
        "Delivery / team",
        "Data / analytics",
    ]
    current = np.array([0.5, 1.0, 0.5, 0.0, 1.0, 0.5, 1.0])
    target = np.array([3.5, 3.5, 3.0, 3.5, 3.0, 3.0, 3.0])
    y = np.arange(len(capabilities))

    fig, ax = plt.subplots(figsize=(11.5, 5.6))
    ax.barh(y + 0.18, target, height=0.32, color=BLUE, label="Цель через 12 месяцев")
    ax.barh(y - 0.18, current, height=0.32, color=AMBER, label="Текущая оценка")
    ax.set_yticks(y, capabilities)
    ax.invert_yaxis()
    ax.set_xlim(0, 5)
    ax.set_xlabel("Уровень зрелости (0–5)")
    ax.set_title("GAP-анализ: от концепции к банковско- и enterprise-ready бизнесу")
    ax.legend(frameon=False, loc="lower right")
    ax.grid(axis="x", color=GRID, linewidth=0.7)
    ax.spines[["top", "right", "left"]].set_visible(False)
    for row, (now, goal) in enumerate(zip(current, target)):
        ax.text(goal + 0.08, row + 0.18, f"{goal:.1f}", va="center", fontsize=8)
        ax.text(now + 0.08, row - 0.18, f"{now:.1f}", va="center", fontsize=8)
    fig.text(
        0.01,
        0.005,
        "Источник: оценка зрелости по доступным артефактам репозитория; отсутствие файла не доказывает отсутствие работы вне репозитория.",
        fontsize=7.5,
        color=MUTED,
    )
    save_chart(fig, "gap-maturity.png")


def make_roadmap_chart() -> None:
    phases = [
        ("Legal + discovery", 0, 2, NAVY),
        ("Banking readiness", 1, 2, TEAL),
        ("No-money MVP", 2, 2, BLUE),
        ("Paid pilots", 3, 2, GREEN),
        ("Repeatable sales", 5, 5, BLUE),
        ("Security + enterprise", 7, 5, NAVY),
        ("Second geography", 10, 5, TEAL),
        ("Benchmark data moat", 12, 8, GREEN),
        ("Regulated option gate", 16, 4, AMBER),
    ]
    fig, ax = plt.subplots(figsize=(12, 6))
    for row, (name, start, length, color) in enumerate(phases):
        ax.barh(row, length, left=start, height=0.55, color=color)
        ax.text(start + 0.18, row, name, va="center", ha="left", color="white", fontsize=8)
    ax.set_yticks([])
    ax.set_xticks(
        np.arange(0, 21),
        [f"Y{year}Q{quarter}" for year in range(1, 6) for quarter in range(1, 5)]
        + [""],
        rotation=45,
        ha="right",
    )
    ax.set_xlim(0, 20)
    ax.invert_yaxis()
    ax.set_xlabel("Кварталы после утверждения стратегии")
    ax.set_title("NOVATOR24: stage-gated дорожная карта на пять лет")
    ax.grid(axis="x", color=GRID, linewidth=0.7)
    ax.spines[["top", "right", "left"]].set_visible(False)
    for marker, label in [(4, "Gate: paid"), (12, "Gate: scale"), (16, "Gate: license")]:
        ax.axvline(marker, color=RED, linestyle="--", linewidth=0.9)
        ax.text(marker + 0.1, len(phases) - 0.2, label, color=RED, fontsize=7)
    fig.text(
        0.01,
        0.005,
        "Принцип: каждый следующий этап финансируется после прохождения измеримого gate; regulated scope не входит в core roadmap.",
        fontsize=7.5,
        color=MUTED,
    )
    save_chart(fig, "roadmap-5y.png")


def make_scenario_chart() -> None:
    years = np.array([0, 1, 3, 5])
    scenarios = {
        "Base: B2B SaaS": (
            np.array([0, 0.05, 1.0, 6.0]),
            np.array([0, 0.15, 3.0, 12.0]),
            BLUE,
        ),
        "Upside: licensed partner": (
            np.array([0, 0.05, 2.0, 10.0]),
            np.array([0, 0.15, 5.0, 20.0]),
            GREEN,
        ),
        "Downside: friction": (
            np.array([0, 0.02, 0.3, 2.0]),
            np.array([0, 0.08, 1.0, 5.0]),
            AMBER,
        ),
    }
    fig, ax = plt.subplots(figsize=(11.5, 6.2))
    for name, (low, high, color) in scenarios.items():
        mid = (low + high) / 2
        ax.plot(years, mid, marker="o", linewidth=2, color=color, label=name)
        ax.fill_between(years, low, high, color=color, alpha=0.14)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 21)
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_xlabel("Годы после утверждения стратегии")
    ax.set_ylabel("ARR, млн USD")
    ax.set_title("Сценарные диапазоны ARR — цели для решений, не прогноз")
    ax.grid(color=GRID, linewidth=0.7)
    ax.legend(frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(
        0.01,
        0.005,
        "Источник: управленческие допущения стратегии от 22.08.2026; диапазоны требуют пересчёта после первых пяти платных пилотов.",
        fontsize=7.5,
        color=MUTED,
    )
    save_chart(fig, "scenario-arr.png")


def generate_charts() -> None:
    ASSETS.mkdir(exist_ok=True)
    chart_style()
    make_swot_chart()
    make_gap_chart()
    make_roadmap_chart()
    make_scenario_chart()


def inline_markup(text: str) -> str:
    text = html.escape(text, quote=False)
    code_fragments: list[str] = []

    def protect_code(match: re.Match) -> str:
        code_fragments.append(match.group(1))
        return f"@@CODE{len(code_fragments) - 1}@@"

    text = re.sub(r"`([^`]+)`", protect_code, text)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<link href="\2" color="#276FBF">\1</link>',
        text,
    )
    text = re.sub(
        r"(?<!\()(?<!href=&quot;)(https?://\S+)",
        r'<link href="\1" color="#276FBF">\1</link>',
        text,
    )
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    for index, fragment in enumerate(code_fragments):
        text = text.replace(
            f"@@CODE{index}@@", f'<font name="Courier">{fragment}</font>'
        )
    return text


def build_styles() -> dict[str, ParagraphStyle]:
    styles = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName=REGULAR,
            fontSize=9.1,
            leading=12.2,
            textColor=colors.HexColor(TEXT),
            spaceAfter=4.5,
            splitLongWords=True,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=styles["Heading1"],
            fontName=BOLD,
            fontSize=20,
            leading=23,
            textColor=colors.HexColor(NAVY),
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=styles["Heading2"],
            fontName=BOLD,
            fontSize=15,
            leading=18,
            textColor=colors.HexColor(NAVY),
            spaceBefore=2,
            spaceAfter=7,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=styles["Heading3"],
            fontName=BOLD,
            fontSize=11.5,
            leading=14,
            textColor=colors.HexColor(BLUE),
            spaceBefore=7,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "h4": ParagraphStyle(
            "H4",
            parent=styles["Heading4"],
            fontName=BOLD,
            fontSize=9.7,
            leading=12,
            textColor=colors.HexColor(TEAL),
            spaceBefore=5,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "quote": ParagraphStyle(
            "Quote",
            parent=styles["BodyText"],
            fontName=ITALIC,
            fontSize=9.3,
            leading=13,
            textColor=colors.HexColor(NAVY),
            leftIndent=8 * mm,
            rightIndent=4 * mm,
            borderColor=colors.HexColor(BLUE),
            borderWidth=1.5,
            borderPadding=(4, 7, 4, 7),
            backColor=colors.HexColor(LIGHT),
            spaceAfter=8,
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=styles["BodyText"],
            fontName=REGULAR,
            fontSize=7.2,
            leading=9,
            textColor=colors.HexColor(MUTED),
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "table": ParagraphStyle(
            "TableCell",
            parent=styles["BodyText"],
            fontName=REGULAR,
            fontSize=6.7,
            leading=8.3,
            textColor=colors.HexColor(TEXT),
            splitLongWords=True,
        ),
        "table_head": ParagraphStyle(
            "TableHead",
            parent=styles["BodyText"],
            fontName=BOLD,
            fontSize=6.6,
            leading=8,
            textColor=colors.white,
            splitLongWords=True,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=6.8,
            leading=8.2,
            backColor=colors.HexColor(LIGHT),
            borderPadding=5,
            spaceAfter=6,
        ),
    }


STYLES = build_styles()


def fit_image(path: Path, max_width: float, max_height: float) -> Image:
    with PILImage.open(path) as image:
        width, height = image.size
    scale = min(max_width / width, max_height / height)
    return Image(str(path), width=width * scale, height=height * scale)


def make_table(rows: list[list[str]], available_width: float) -> Table:
    ncols = max(len(row) for row in rows)
    padded = [row + [""] * (ncols - len(row)) for row in rows]
    weights = []
    for col in range(ncols):
        longest = max(5, min(34, max(len(row[col]) for row in padded)))
        weights.append(longest)
    total = sum(weights)
    col_widths = [available_width * weight / total for weight in weights]

    parsed = []
    for ridx, row in enumerate(padded):
        style = STYLES["table_head"] if ridx == 0 else STYLES["table"]
        parsed.append([Paragraph(inline_markup(cell.strip()), style) for cell in row])
    table = Table(parsed, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(NAVY)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor(GRID)),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
    ]
    for ridx in range(1, len(parsed)):
        if ridx % 2 == 0:
            commands.append(
                ("BACKGROUND", (0, ridx), (-1, ridx), colors.HexColor("#F7F9FB"))
            )
    table.setStyle(TableStyle(commands))
    return table


def add_cover(story: list, page_width: float) -> None:
    story.append(Spacer(1, 7 * mm))
    story.append(
        Paragraph(
            "NOVATOR24",
            ParagraphStyle(
                "CoverBrand",
                fontName=BOLD,
                fontSize=13,
                leading=16,
                textColor=colors.HexColor(BLUE),
                alignment=TA_CENTER,
                spaceAfter=8,
            ),
        )
    )
    story.append(
        Paragraph(
            "СТРАТЕГИЯ КОМПАНИИ<br/>НА 1, 3 И 5 ЛЕТ",
            ParagraphStyle(
                "CoverTitle",
                fontName=BOLD,
                fontSize=27,
                leading=31,
                textColor=colors.HexColor(NAVY),
                alignment=TA_CENTER,
                spaceAfter=13,
            ),
        )
    )
    story.append(
        fit_image(ASSETS / "hong-kong.jpg", page_width, 82 * mm)
    )
    story.append(Spacer(1, 9 * mm))
    story.append(
        Paragraph(
            "B2B decision intelligence для MENA и APAC:<br/>от концепции рынка предсказаний к легальному, проверяемому SaaS",
            ParagraphStyle(
                "CoverSub",
                fontName=REGULAR,
                fontSize=12,
                leading=17,
                textColor=colors.HexColor(TEXT),
                alignment=TA_CENTER,
                spaceAfter=12,
            ),
        )
    )
    story.append(
        Paragraph(
            "22 августа 2026 года · версия 1.0",
            ParagraphStyle(
                "CoverDate",
                fontName=REGULAR,
                fontSize=9,
                leading=12,
                textColor=colors.HexColor(MUTED),
                alignment=TA_CENTER,
            ),
        )
    )
    story.append(PageBreak())


def markdown_to_story(markdown_text: str, available_width: float) -> list:
    lines = markdown_text.splitlines()
    story: list = []
    paragraph_buffer: list[str] = []
    code_buffer: list[str] = []
    in_code = False
    seen_first_h2 = False
    skipped_title = False
    skipped_cover_photo = False

    def flush_paragraph() -> None:
        if paragraph_buffer:
            text = " ".join(item.strip() for item in paragraph_buffer).strip()
            if text:
                story.append(Paragraph(inline_markup(text), STYLES["body"]))
            paragraph_buffer.clear()

    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            if in_code:
                story.append(Preformatted("\n".join(code_buffer), STYLES["code"]))
                code_buffer.clear()
                in_code = False
            else:
                in_code = True
            idx += 1
            continue
        if in_code:
            code_buffer.append(line)
            idx += 1
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            table_lines = []
            while idx < len(lines):
                candidate = lines[idx].strip()
                if not (candidate.startswith("|") and candidate.endswith("|")):
                    break
                table_lines.append(candidate)
                idx += 1
            rows = []
            for table_line in table_lines:
                cells = [cell.strip() for cell in table_line.strip("|").split("|")]
                if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                    continue
                rows.append(cells)
            if rows:
                story.append(make_table(rows, available_width))
                story.append(Spacer(1, 5 * mm))
            continue

        image_match = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
        if image_match:
            flush_paragraph()
            alt, relative_path = image_match.groups()
            if not skipped_cover_photo and relative_path.endswith("hong-kong.jpg"):
                skipped_cover_photo = True
                idx += 1
                continue
            image_path = ROOT / relative_path
            if image_path.exists():
                story.append(Spacer(1, 2 * mm))
                story.append(fit_image(image_path, available_width, 118 * mm))
                if alt:
                    story.append(Paragraph(inline_markup(alt), STYLES["caption"]))
            idx += 1
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            title = heading.group(2)
            if level == 1 and not skipped_title:
                skipped_title = True
                idx += 1
                continue
            if level == 2:
                if seen_first_h2:
                    story.append(PageBreak())
                seen_first_h2 = True
            story.append(Paragraph(inline_markup(title), STYLES[f"h{level}"]))
            idx += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            quote_lines = []
            while idx < len(lines) and lines[idx].strip().startswith(">"):
                quote_lines.append(lines[idx].strip()[1:].strip())
                idx += 1
            story.append(
                Paragraph(inline_markup(" ".join(quote_lines)), STYLES["quote"])
            )
            continue

        if re.match(r"^[-*]\s+", stripped):
            flush_paragraph()
            item = re.sub(r"^[-*]\s+", "", stripped)
            story.append(
                Paragraph(
                    inline_markup(item),
                    ParagraphStyle(
                        "Bullet",
                        parent=STYLES["body"],
                        leftIndent=6 * mm,
                        firstLineIndent=-3.5 * mm,
                        bulletIndent=1 * mm,
                    ),
                    bulletText="•",
                )
            )
            idx += 1
            continue

        numbered = re.match(r"^(\d+)\.\s+(.+)$", stripped)
        if numbered:
            flush_paragraph()
            story.append(
                Paragraph(
                    inline_markup(numbered.group(2)),
                    ParagraphStyle(
                        "Numbered",
                        parent=STYLES["body"],
                        leftIndent=7 * mm,
                        firstLineIndent=-5 * mm,
                    ),
                    bulletText=f"{numbered.group(1)}.",
                )
            )
            idx += 1
            continue

        if stripped == "---":
            flush_paragraph()
            story.append(
                HRFlowable(
                    width="100%",
                    thickness=0.6,
                    color=colors.HexColor(GRID),
                    spaceBefore=4,
                    spaceAfter=6,
                )
            )
            idx += 1
            continue

        if not stripped:
            flush_paragraph()
        else:
            paragraph_buffer.append(line)
        idx += 1

    flush_paragraph()
    return story


def draw_header_footer(canvas, doc) -> None:
    canvas.saveState()
    width, height = A4
    if doc.page > 1:
        canvas.setStrokeColor(colors.HexColor(GRID))
        canvas.setLineWidth(0.4)
        canvas.line(18 * mm, height - 14 * mm, width - 18 * mm, height - 14 * mm)
        canvas.setFont(REGULAR, 7.2)
        canvas.setFillColor(colors.HexColor(MUTED))
        canvas.drawString(18 * mm, height - 10.5 * mm, "NOVATOR24 · Стратегия 2026–2031")
        canvas.drawRightString(width - 18 * mm, 10 * mm, f"{doc.page}")
    canvas.restoreState()


def build_pdf() -> None:
    markdown_text = SOURCE.read_text(encoding="utf-8")
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=19 * mm,
        bottomMargin=17 * mm,
        title="NOVATOR24: стратегия компании на 1, 3 и 5 лет",
        author="Strategic analysis based on novator24/roadmaps",
        subject="Mission, SWOT, PESTEL, BSC, roadmap and UAE/Hong Kong operating model",
    )
    story: list = []
    add_cover(story, doc.width)
    story.extend(markdown_to_story(markdown_text, doc.width))
    doc.build(story, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)


def main() -> None:
    generate_charts()
    build_pdf()
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
