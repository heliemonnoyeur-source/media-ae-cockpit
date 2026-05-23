"""
Cursor Enterprise — PG + Disco Challenge
Prep deck for the Cursor GTM interview exercise (60 min, 3 parts).

V4 — English version. Same structure as V3.

Structure:
  Part 1 — Greenfield Pipeline (Spain & Italy GTM)     20–25 min
  Part 2 — Mock Discovery Call (Figma inbound)          20–25 min
  Part 3 — Reflection & Debrief                         10–15 min
  Meta   — What is being evaluated (candidate-only)

Known Figma facts to leverage in discovery:
  - Marcel Weekes, VP of Engineering, ~650 engineers
  - ~85% on VS Code (drop-in for Cursor — VS Code fork)
  - GitHub Copilot deployed team-wide
  - Currently evaluating Claude Code
  - 31 Cursor Pro shadow users (mixed Privacy Mode)
  - Meeting: Marcel + Security Eng Leader + Security team member
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor


# ---------------------------------------------------------------------------
# Brand
# ---------------------------------------------------------------------------
BG          = RGBColor(0x0A, 0x0A, 0x0A)
BG_PANEL    = RGBColor(0x14, 0x14, 0x14)
BG_PANEL_2  = RGBColor(0x1C, 0x1C, 0x1C)
HAIRLINE    = RGBColor(0x2A, 0x2A, 0x2A)
TEXT        = RGBColor(0xF5, 0xF5, 0xF5)
TEXT_DIM    = RGBColor(0xA0, 0xA0, 0xA0)
TEXT_MUTED  = RGBColor(0x6B, 0x6B, 0x6B)
ACCENT      = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT_SOFT = RGBColor(0xE5, 0xE5, 0xE5)

FONT = "Inter"
FONT_MONO = "JetBrains Mono"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def add_slide():
    s = prs.slides.add_slide(BLANK)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    bg.line.fill.background()
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG
    bg.shadow.inherit = False
    return s


def add_text(slide, x, y, w, h, text, *,
             size=18, bold=False, color=TEXT, font=FONT,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             line_spacing=1.15, letter_spacing=None, italic=False):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor

    lines = text.split("\n") if isinstance(text, str) else text
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        r = p.add_run()
        r.text = line
        r.font.name = font
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
        if letter_spacing is not None:
            rPr = r._r.get_or_add_rPr()
            rPr.set("spc", str(letter_spacing))
    return tb


def add_rect(slide, x, y, w, h, color, line=False):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = color
    if not line:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = HAIRLINE
        sh.line.width = Pt(0.5)
    sh.shadow.inherit = False
    return sh


def add_hairline(slide, x, y, w):
    return add_rect(slide, x, y, w, Emu(6350), HAIRLINE)


def page_chrome(slide, page_num, total, section_label, part=None):
    add_text(slide, Inches(0.55), Inches(0.35), Inches(3), Inches(0.4),
             "● cursor", size=11, color=TEXT, bold=True, letter_spacing=20)
    right = section_label.upper()
    if part is not None:
        right = f"PART {part}  ·  " + right
    add_text(slide, Inches(7.0), Inches(0.35), Inches(5.8), Inches(0.4),
             right, size=9, color=TEXT_MUTED,
             align=PP_ALIGN.RIGHT, letter_spacing=200)
    add_text(slide, Inches(0.55), Inches(7.05), Inches(6.5), Inches(0.3),
             "Cursor Enterprise — PG + Disco Challenge  ·  Prep deck",
             size=9, color=TEXT_MUTED, letter_spacing=80)
    add_text(slide, Inches(11.5), Inches(7.05), Inches(1.3), Inches(0.3),
             f"{page_num:02d} / {total:02d}",
             size=9, color=TEXT_MUTED, align=PP_ALIGN.RIGHT,
             font=FONT_MONO, letter_spacing=50)
    add_hairline(slide, Inches(0.55), Inches(0.85), Inches(12.25))


def section_title(slide, kicker, title, subtitle=None, title_y=1.65,
                  title_size=34, subtitle_top=2.85):
    add_text(slide, Inches(0.55), Inches(1.25), Inches(10), Inches(0.4),
             kicker.upper(), size=10, color=TEXT_MUTED, letter_spacing=300)
    add_text(slide, Inches(0.55), Inches(title_y), Inches(12), Inches(1.2),
             title, size=title_size, bold=True, color=TEXT, line_spacing=1.05)
    if subtitle:
        add_text(slide, Inches(0.55), Inches(subtitle_top), Inches(12), Inches(0.9),
                 subtitle, size=14, color=TEXT_DIM, line_spacing=1.35)


def part_divider(slide, part_num, label, title, body):
    add_rect(slide, Inches(8.2), 0, Inches(5.13), SH, BG_PANEL)
    add_rect(slide, Inches(8.2), 0, Emu(6350), SH, HAIRLINE)
    add_text(slide, Inches(0.55), Inches(0.55), Inches(3), Inches(0.4),
             "● cursor", size=12, color=TEXT, bold=True, letter_spacing=20)
    add_text(slide, Inches(0.55), Inches(2.3), Inches(8), Inches(0.5),
             f"PART {part_num} · {label}", size=11, color=TEXT_MUTED, letter_spacing=400)
    add_text(slide, Inches(0.55), Inches(2.75), Inches(8.5), Inches(2.6),
             title, size=50, bold=True, color=TEXT, line_spacing=1.02)
    add_text(slide, Inches(0.55), Inches(5.1), Inches(7.5), Inches(1.5),
             body, size=15, color=TEXT_DIM, line_spacing=1.45, italic=True)


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

TOTAL = 24


# =============================================================================
# 01 — Master cover
# =============================================================================
s = add_slide()
add_rect(s, Inches(8.2), 0, Inches(5.13), SH, BG_PANEL)
add_rect(s, Inches(8.2), 0, Emu(6350), SH, HAIRLINE)

add_text(s, Inches(0.55), Inches(0.55), Inches(3), Inches(0.4),
         "● cursor", size=12, color=TEXT, bold=True, letter_spacing=20)

add_text(s, Inches(0.55), Inches(2.2), Inches(8), Inches(0.5),
         "PG + DISCO CHALLENGE · 60 MIN", size=11, color=TEXT_MUTED, letter_spacing=400)

add_text(s, Inches(0.55), Inches(2.65), Inches(8.8), Inches(2.7),
         "Cursor Enterprise\nPipeline + Discovery.",
         size=52, bold=True, color=TEXT, line_spacing=1.02)

add_text(s, Inches(0.55), Inches(5.0), Inches(8), Inches(1.5),
         "Cursor wins on workflow, context, and execution.\n"
         "~70% of the Fortune 1000 already use it.",
         size=15, color=TEXT_DIM, line_spacing=1.4, italic=True)

add_text(s, Inches(8.6), Inches(2.2), Inches(4), Inches(0.4),
         "STRUCTURE", size=10, color=TEXT_MUTED, letter_spacing=300)
add_text(s, Inches(8.6), Inches(2.6), Inches(4.5), Inches(3.5),
         "P1 · Greenfield (Spain & Italy)  (20–25')\n"
         "P2 · Mock Disco Figma  (20–25')\n"
         "P3 · Reflection & Debrief  (10–15')",
         size=13, color=TEXT, line_spacing=2.0)

add_text(s, Inches(8.6), Inches(5.5), Inches(4), Inches(0.4),
         "POSTURE", size=10, color=TEXT_MUTED, letter_spacing=300)
add_text(s, Inches(8.6), Inches(5.85), Inches(4.5), Inches(1.0),
         "Discovery > pitch.\nOpinionated, not scripted.\nGround claims, no hype.",
         size=12.5, color=TEXT, line_spacing=1.4)

add_text(s, Inches(0.55), Inches(7.05), Inches(8), Inches(0.3),
         "Confidential — Internal prep document",
         size=9, color=TEXT_MUTED, letter_spacing=80)
add_text(s, Inches(11.5), Inches(7.05), Inches(1.3), Inches(0.3),
         f"01 / {TOTAL:02d}", size=9, color=TEXT_MUTED,
         align=PP_ALIGN.RIGHT, font=FONT_MONO)


# =============================================================================
# 02 — Roadmap of the 60 minutes
# =============================================================================
s = add_slide(); page_chrome(s, 2, TOTAL, "Roadmap")
section_title(s, "60 minutes, three connected exercises",
              "How the time will be spent.",
              "Account-development mindset informs discovery. One story, three proofs.")

rows = [
    ("PART 1", "0–25 min",
     "Greenfield Pipeline (Spain & Italy)",
     "Top 5 ranked · deep-dive #1 · stakeholder map · entry & 90 days."),
    ("PART 2", "25–50 min",
     "Mock Discovery — Figma inbound",
     "Marcel Weekes · 650 engs · 85% VS Code · Copilot + Claude Code · 31 shadow Pro."),
    ("PART 3", "50–60 min",
     "Reflection & Debrief",
     "Top insights · deal hypothesis · 4 strategic questions · self-assessment."),
]
y = Inches(3.9)
for tag, tm, title, desc in rows:
    add_rect(s, Inches(0.55), y, Inches(12.25), Inches(0.95), BG_PANEL)
    add_rect(s, Inches(0.55), y, Inches(12.25), Emu(6350), HAIRLINE)
    add_text(s, Inches(0.85), y + Inches(0.2), Inches(1.1), Inches(0.5),
             tag, size=11, color=TEXT_MUTED, bold=True, letter_spacing=200, font=FONT_MONO)
    add_text(s, Inches(2.1), y + Inches(0.2), Inches(1.5), Inches(0.5),
             tm, size=12, color=TEXT_DIM, font=FONT_MONO)
    add_text(s, Inches(3.85), y + Inches(0.15), Inches(4.0), Inches(0.5),
             title, size=15, bold=True, color=TEXT)
    add_text(s, Inches(3.85), y + Inches(0.5), Inches(8.7), Inches(0.45),
             desc, size=11.5, color=TEXT_DIM, line_spacing=1.3)
    y += Inches(1.05)


# =============================================================================
# 03 — PART 1 DIVIDER
# =============================================================================
s = add_slide()
part_divider(s, 1, "GREENFIELD PIPELINE",
             "Spain & Italy\nfrom zero.",
             "Iberia + Italy GTM. Top 5 ranked, deep dive on Santander:\n"
             "account thesis, stakeholder map, entry sequencing, first 90 days.")
add_text(s, Inches(11.5), Inches(7.05), Inches(1.3), Inches(0.3),
         f"03 / {TOTAL:02d}", size=9, color=TEXT_MUTED,
         align=PP_ALIGN.RIGHT, font=FONT_MONO)


# =============================================================================
# 04 — Ranking criteria
# =============================================================================
s = add_slide(); page_chrome(s, 4, TOTAL, "Ranking criteria", part=1)
section_title(s, "Before the Top 5",
              "How I rank an ENT account in Spain & Italy.",
              "Five lenses, weighted. Any exception — I find out why.")

crits = [
    ("01 · Eng headcount",
     "≥ 5K engineers for a meaningful enterprise deal. The bigger, the louder ROI math gets."),
    ("02 · Public AI mandate",
     "Executive-announced AI roadmap → easier champion uptake, urgency already exists."),
    ("03 · Reg / privacy posture",
     "EU regulated (DORA, EU AI Act, ECB) = Privacy Mode = enabler, not blocker. Our edge."),
    ("04 · Codebase complexity",
     "Legacy + modern + mono/multi-repo = large codebase performance becomes pivotal."),
    ("05 · Procurement reach",
     "Identifiable dev-tools team + traceable procurement path = deal velocity."),
]
y = Inches(3.65)
for k, v in crits:
    add_text(s, Inches(0.55), y, Inches(0.3), Inches(0.4), "→", size=16, color=TEXT_MUTED)
    add_text(s, Inches(1.0), y, Inches(4.5), Inches(0.4), k, size=14, bold=True, color=TEXT)
    add_text(s, Inches(5.6), y, Inches(7.2), Inches(0.7), v,
             size=12, color=TEXT_DIM, line_spacing=1.4)
    add_hairline(s, Inches(0.55), y + Inches(0.65), Inches(12.25))
    y += Inches(0.68)


# =============================================================================
# 05 — Top 5
# =============================================================================
s = add_slide(); page_chrome(s, 5, TOTAL, "Top 5 prospects", part=1)
section_title(s, "Greenfield · ranked",
              "Top 5 — Spain & Italy GTM.",
              "Defensible ranking. Santander as #1 → deep-dive on the next 4 slides.")

prospects = [
    ("#1", "Santander",
     "~15–20K tech · 'One Transformation' under Dirk Marzluf · multi-jurisdiction regulated · Openbank = digital-native wedge.",
     "Largest Iberia TAM + champion-ready."),
    ("#2", "BBVA",
     "~10K tech · ChatGPT Enterprise already rolled out org-wide · 'born digital' under Carlos Torres.",
     "AI-ready buyer, strong deal velocity."),
    ("#3", "Enel",
     "~15K tech · energy transition = urgency · OpenInnovability AI lab · mature CISO function.",
     "Largest Italy TAM."),
    ("#4", "EssilorLuxottica",
     "~5–7K tech / 190K total · Industry 4.0 + e-commerce push · regulated (medical devices).",
     "FR/IT footprint, industrial leverage."),
    ("#5", "El Corte Inglés",
     "~2–3K tech · e-commerce + supply chain transformation under Marta Álvarez · less crowded.",
     "Less competitive crowding, accessible."),
]
y = Inches(3.55)
for rk, name, why, edge in prospects:
    add_rect(s, Inches(0.55), y, Inches(12.25), Inches(0.66), BG_PANEL)
    add_rect(s, Inches(0.55), y, Inches(12.25), Emu(6350), HAIRLINE)
    add_text(s, Inches(0.8), y + Inches(0.12), Inches(0.8), Inches(0.5),
             rk, size=18, bold=True, color=TEXT, font=FONT_MONO)
    add_text(s, Inches(1.85), y + Inches(0.12), Inches(2.5), Inches(0.5),
             name, size=13, bold=True, color=TEXT)
    add_text(s, Inches(4.5), y + Inches(0.13), Inches(6.0), Inches(0.45),
             why, size=10.5, color=TEXT_DIM, line_spacing=1.25)
    add_text(s, Inches(10.6), y + Inches(0.18), Inches(2.2), Inches(0.45),
             edge, size=10, color=ACCENT_SOFT, line_spacing=1.25, italic=True)
    y += Inches(0.72)


# =============================================================================
# 06 — Santander · Account thesis
# =============================================================================
s = add_slide(); page_chrome(s, 6, TOTAL, "Deep dive · Santander", part=1)
section_title(s, "Top prospect · Account thesis",
              "Santander — why now, where Cursor wins.",
              "4 angles. Every one has a public, citable proof point.")

cols = [
    ("WHY SANTANDER",
     "~15–20K tech (Santander Global\nT&O + Openbank + Cardinal).\nAna Botín references AI on every\nearnings call.\nOpenAI + Google Cloud partnerships\nannounced in 2024."),
    ("WHY NOW",
     "'One Transformation' T&O launched\n2024 under Dirk Marzluf.\nBBVA deployed ChatGPT Enterprise\norg-wide → direct competitive pressure.\nDORA + EU AI Act = AI governance\nurgency."),
    ("CURSOR LEVERS",
     "Velocity (Openbank, digital-native).\nGovernance (Privacy Mode for\nECB / BoE / Fed).\nOnboarding (rotations across 10+\ncountries).\nCost (lower IT spend / revenue ratio)."),
    ("MARKET FORCES",
     "AI talent costly in Iberia →\ntool = hiring & retention lever.\nModel neutrality = resilience vs\nEU sovereign-AI ecosystem.\nClaude Code being evaluated at EU\npeers (ING, BNP)."),
]
xw = Inches(2.95); gap = Inches(0.15)
x = Inches(0.55)
for label, body in cols:
    add_rect(s, x, Inches(3.7), xw, Inches(3.3), BG_PANEL)
    add_rect(s, x, Inches(3.7), xw, Emu(6350), HAIRLINE)
    add_text(s, x + Inches(0.25), Inches(3.85), xw - Inches(0.5), Inches(0.4),
             label, size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
    add_text(s, x + Inches(0.25), Inches(4.25), xw - Inches(0.5), Inches(2.8),
             body, size=11, color=TEXT, line_spacing=1.5)
    x += xw + gap


# =============================================================================
# 07 — Santander · Stakeholder map
# =============================================================================
s = add_slide(); page_chrome(s, 7, TOTAL, "Santander · Stakeholders", part=1)
section_title(s, "Engineering org map",
              "Who I target, in what order, and why.",
              "Power signals: T&O budget, T&O hiring in Madrid/London, sponsorship of board-level AI initiatives.")

stk = [
    ("01", "Openbank CTO + Head of Engineering",
     "Wedge #1. Digital-native subsidiary, autonomous, shorter procurement.",
     "Cold + LinkedIn. Message: '30-day pilot on one squad, metrics pre-defined.'"),
    ("02", "VP / Director of Developer Productivity — Santander T&O",
     "Economic buyer at Group level. Owns the dev tools budget.",
     "Warm intro via Madrid tech community + EU bank reference customer."),
    ("03", "AppSec leadership (under the Group CISO)",
     "Gatekeeper. Not a blocker if Privacy Mode + SOC 2 + DORA-aligned anticipated.",
     "Include them early, send SIG + pentest + DPA before asking."),
    ("04", "Dirk Marzluf (Group Head of T&O)",
     "Executive sponsor. Not first-touch — engaged once we have a quantified POC.",
     "Once POC live: board-level ROI + risk reduction narrative."),
    ("05", "Engineers (bottom-up)",
     "Shadow adoption = Marcel-style signal. Free-tier monitoring on @santander.com.",
     "Track signups, identify a staff IC champion in Madrid."),
]
y = Inches(3.55)
for n, who, why, how in stk:
    add_text(s, Inches(0.55), y, Inches(0.7), Inches(0.4),
             n, size=14, color=TEXT_MUTED, font=FONT_MONO)
    add_text(s, Inches(1.3), y, Inches(3.6), Inches(0.4),
             who, size=12, bold=True, color=TEXT)
    add_text(s, Inches(5.05), y, Inches(4.2), Inches(0.7),
             why, size=10.5, color=TEXT_DIM, line_spacing=1.3)
    add_text(s, Inches(9.4), y, Inches(3.4), Inches(0.7),
             how, size=10.5, color=ACCENT_SOFT, line_spacing=1.3, italic=True)
    add_hairline(s, Inches(0.55), y + Inches(0.62), Inches(12.25))
    y += Inches(0.66)


# =============================================================================
# 08 — Santander · Entry + 90 days
# =============================================================================
s = add_slide(); page_chrome(s, 8, TOTAL, "Santander · Entry + 90 days", part=1)
section_title(s, "Pipeline & sequencing",
              "How I create momentum.",
              "Multi-channel, sequenced, measurable outreach. 90 days to a quantified Openbank POC.")

# left: entry channels
add_rect(s, Inches(0.55), Inches(3.55), Inches(6.1), Inches(3.55), BG_PANEL)
add_rect(s, Inches(0.55), Inches(3.55), Inches(6.1), Emu(6350), HAIRLINE)
add_text(s, Inches(0.85), Inches(3.7), Inches(5.5), Inches(0.4),
         "ENTRY POINTS — sequenced", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
entries = [
    ("Openbank-first", "Digital-native wedge. Target Openbank CTO + Head of Eng. Shorter procurement."),
    ("Cold outbound", "Dir DevProd Santander T&O + AppSec, 3 touches/week, ROI + EU bank reference."),
    ("Warm intro", "Madrid tech community (South Summit, Endeavor, Wayra alumni). Small world."),
    ("Conference", "South Summit Madrid · Money 20/20 Europe · DevOpsCon Madrid."),
    ("Bottom-up", "Free-tier monitoring on @santander.com → IC champion in Madrid/Boston."),
]
yy = Inches(4.1)
for k, v in entries:
    add_text(s, Inches(0.85), yy, Inches(1.8), Inches(0.4),
             k, size=11, bold=True, color=TEXT)
    add_text(s, Inches(2.75), yy, Inches(3.7), Inches(0.7),
             v, size=10.5, color=TEXT_DIM, line_spacing=1.3)
    yy += Inches(0.55)

# right: first 90 days
add_rect(s, Inches(6.85), Inches(3.55), Inches(5.95), Inches(3.55), BG_PANEL)
add_rect(s, Inches(6.85), Inches(3.55), Inches(5.95), Emu(6350), HAIRLINE)
add_text(s, Inches(7.15), Inches(3.7), Inches(5.5), Inches(0.4),
         "FIRST 90 DAYS", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
days = [
    ("D0–D30",  "Research Openbank + Santander T&O.\n3 cold touches/week + 1 warm intro Madrid.\nSuccess: 1 mtg Openbank CTO, 1 mtg AppSec."),
    ("D30–D60", "Discovery Openbank + parallel T&O intro.\nSuccess: 20–30-engineer POC signed on\none Openbank squad (mobile or backend)."),
    ("D60–D90", "POC live, Privacy Mode mandated + DORA-aligned.\nSuccess: cycle-time + PR + NPS measured.\nOpens Group T&O conversation on 1K+ seats."),
]
yy = Inches(4.1)
for k, v in days:
    add_text(s, Inches(7.15), yy, Inches(1.0), Inches(0.4),
             k, size=11, bold=True, color=TEXT, font=FONT_MONO)
    add_text(s, Inches(8.25), yy, Inches(4.4), Inches(1.0),
             v, size=10.5, color=TEXT_DIM, line_spacing=1.35)
    yy += Inches(0.92)


# =============================================================================
# 09 — Santander · Pilot motion
# =============================================================================
s = add_slide(); page_chrome(s, 9, TOTAL, "Santander · Pilot motion", part=1)
section_title(s, "Initial pilot motion · Openbank wedge",
              "What the quantified POC looks like.",
              "Openbank = path of least resistance. Success here opens Group T&O on 1K+ seats.")

cols = [
    ("SCOPE",
     "20–30 Openbank engineers\n(digital-native, modern stack,\nhigh velocity).\n30 days.\n1 mobile or backend squad,\n1 reference repo."),
    ("METRICS",
     "Cycle time (PR opened → merged)\nPR throughput / engineer / week\nSenior IC adoption rate\nNPS engagement at D+15 and D+30."),
    ("SECURITY DAY 1",
     "Privacy Mode mandatory.\nSOC 2 + SIG sent D-7.\nDORA-aligned: audit logs, EU data\nresidency validated.\nGroup AppSec in the loop from D0."),
    ("EXIT GATE",
     "Cycle-time ↓ ≥ 12%\nNPS ≥ 50\nSenior IC adoption ≥ 60%\n→ opens Group T&O conversation\non Santander Global Tech: 1K–5K seats."),
]
xw = Inches(2.95); gap = Inches(0.15)
x = Inches(0.55)
for label, body in cols:
    add_rect(s, x, Inches(3.7), xw, Inches(3.3), BG_PANEL)
    add_rect(s, x, Inches(3.7), xw, Emu(6350), HAIRLINE)
    add_text(s, x + Inches(0.25), Inches(3.85), xw - Inches(0.5), Inches(0.4),
             label, size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
    add_text(s, x + Inches(0.25), Inches(4.25), xw - Inches(0.5), Inches(2.8),
             body, size=11, color=TEXT, line_spacing=1.5)
    x += xw + gap


# =============================================================================
# 10 — PART 2 DIVIDER · Figma
# =============================================================================
s = add_slide()
part_divider(s, 2, "MOCK DISCOVERY · FIGMA",
             "Marcel Weekes\ninbound.",
             "VP Eng · ~650 engineers · 85% VS Code · Copilot deployed ·\n"
             "Claude Code being evaluated · 31 Cursor Pro shadow users (mixed Privacy Mode).")
add_text(s, Inches(11.5), Inches(7.05), Inches(1.3), Inches(0.3),
         f"10 / {TOTAL:02d}", size=9, color=TEXT_MUTED,
         align=PP_ALIGN.RIGHT, font=FONT_MONO)


# =============================================================================
# 11 — Figma brief
# =============================================================================
s = add_slide(); page_chrome(s, 11, TOTAL, "Brief · Figma", part=2)
section_title(s, "What we know before we walk in",
              "The brief, in 6 facts.",
              "Every fact is a discovery lever. We leverage them — not repeat them.")

facts = [
    ("Marcel Weekes",     "VP of Engineering, leads ~650 engineers.",
     "→ Primary economic buyer. KPIs: velocity, talent."),
    ("~85% on VS Code",   "Dominant internal standard.",
     "→ Cursor = VS Code fork. Drop-in. Muscle memory transfer."),
    ("GitHub Copilot",    "Deployed across the entire team.",
     "→ Known baseline. 'Why change' = quality gap, not absence of tool."),
    ("Claude Code eval",  "Actively under evaluation right now.",
     "→ THE competitor. 'Why now' is already established on their side."),
    ("31 Cursor Pro",     "Shadow internal usage, mixed Privacy Mode.",
     "→ Gold. Silent champion + sec risk = their problem, our wedge."),
    ("Attendees",         "Marcel + Security Eng Leader + Security IC.",
     "→ 2 of 3 are security. This is a security-first conversation."),
]
y = Inches(3.55)
for k, fact, lever in facts:
    add_text(s, Inches(0.55), y, Inches(2.6), Inches(0.4),
             k, size=12, bold=True, color=TEXT)
    add_text(s, Inches(3.3), y, Inches(4.5), Inches(0.4),
             fact, size=11.5, color=TEXT_DIM)
    add_text(s, Inches(8.0), y, Inches(4.8), Inches(0.5),
             lever, size=11, color=ACCENT_SOFT, italic=True, line_spacing=1.3)
    add_hairline(s, Inches(0.55), y + Inches(0.45), Inches(12.25))
    y += Inches(0.48)


# =============================================================================
# 12 — Disco agenda
# =============================================================================
s = add_slide(); page_chrome(s, 12, TOTAL, "Disco · Agenda", part=2)
section_title(s, "Call structure",
              "20–25 minutes, timeboxed.",
              "Marcel speaks first. Security joins minute 5. Goal = specific follow-up, not pilot close.")

rows = [
    ("0:00 – 1:30",  "Framing",               "Agenda · permission · anchor on the 31 Pro users."),
    ("1:30 – 9:30",  "Discovery",             "Marcel first, Security from minute 5."),
    ("9:30 – 13:00", "Thesis + 1 proof point","Why now (their urgency) · why Cursor (vs Claude Code)."),
    ("13:00 – 17:00","Security",              "Privacy Mode 3 bullets + SOC 2. I open it, not them."),
    ("17:00 – 20:00","Specific next step",    "Named follow-up: who, when, what for."),
]
y = Inches(3.85)
for tm, title, desc in rows:
    add_text(s, Inches(0.55), y, Inches(2.1), Inches(0.4),
             tm, size=12, color=TEXT_MUTED, font=FONT_MONO)
    add_text(s, Inches(2.9), y, Inches(3.2), Inches(0.4),
             title, size=14, bold=True, color=TEXT)
    add_text(s, Inches(6.3), y, Inches(6.5), Inches(0.4),
             desc, size=12, color=TEXT_DIM)
    add_hairline(s, Inches(0.55), y + Inches(0.55), Inches(12.25))
    y += Inches(0.58)


# =============================================================================
# 13 — Opener (Marcel-specific script)
# =============================================================================
s = add_slide(); page_chrome(s, 13, TOTAL, "Disco · Opener", part=2)
section_title(s, "The first 90 seconds",
              "Opening script.",
              "Visible preparation (name, facts) · no pitch · pre-engagement on the agenda.")

add_rect(s, Inches(0.55), Inches(3.55), Inches(12.25), Inches(3.25), BG_PANEL)
add_rect(s, Inches(0.55), Inches(3.55), Inches(12.25), Emu(6350), HAIRLINE)
add_text(s, Inches(0.9), Inches(3.8), Inches(0.5), Inches(0.4),
         "“", size=44, color=TEXT_MUTED, font="Georgia")
add_text(s, Inches(1.35), Inches(3.95), Inches(11.1), Inches(2.8),
         "Marcel, thanks for the 20 minutes — and thanks to [Security Eng Lead] "
         "and [Sec team member] for joining, this is exactly the right room for "
         "this conversation. Before we start: I noticed 31 of your engineers are "
         "already on Cursor Pro in mixed Privacy Mode. Rather than pitching, I'd "
         "rather start from that reality — understand what you're seeing internally, "
         "what's pulling the Claude Code evaluation in parallel, and where you want "
         "all of this to be in 6 months. I'm going to spend most of the time asking "
         "questions. My goal on Cursor's side: a specific, useful follow-up, not "
         "a pitch. Does that framing work for you?",
         size=14, color=TEXT, line_spacing=1.55)

add_text(s, Inches(0.55), Inches(6.95), Inches(12), Inches(0.3),
         "EFFECTS — visible preparation (31 Pro, Claude Code) · self-aware (no pitch) · "
         "pre-engagement · security involved from word 1",
         size=10, color=TEXT_MUTED, letter_spacing=80)


# =============================================================================
# 14 — Discovery · Marcel
# =============================================================================
s = add_slide(); page_chrome(s, 14, TOTAL, "Disco · Marcel", part=2)
section_title(s, "8 minutes · VP of Engineering",
              "Questions anchored on the facts.",
              "Every question points at a known fact. No generic questions.")

qs = [
    ("01", "Origin of shadow",
     "\"31 engineers on Cursor Pro — how did that happen, and what do they say when you ask them?\"",
     "→ Bottom-up signal. If Marcel didn't know, that's a visibility gap = wedge."),
    ("02", "Pressure-test Claude Code",
     "\"What made you look at Claude Code now rather than 6 months ago, and what would you expect from a switch?\"",
     "→ 'Why now' lives here. We let Marcel articulate it for us."),
    ("03", "Copilot gap",
     "\"Copilot is deployed wall-to-wall — what work should be assisted but isn't today?\"",
     "→ Refactors · large context · review. Where Cursor has a tangible edge."),
    ("04", "Senior IC opt-out",
     "\"Are senior and junior engineers using Copilot the same way? Is there a tier that's quietly disengaged?\"",
     "→ Senior opt-out = org ROI capped at ~5%. Our strongest gap proof."),
]
y = Inches(3.55)
for n, k, q, hint in qs:
    add_text(s, Inches(0.55), y, Inches(0.7), Inches(0.4),
             n, size=14, color=TEXT_MUTED, font=FONT_MONO)
    add_text(s, Inches(1.2), y, Inches(3), Inches(0.4),
             k, size=12.5, bold=True, color=TEXT)
    add_text(s, Inches(4.2), y, Inches(8.6), Inches(0.5),
             q, size=11.5, color=ACCENT_SOFT, line_spacing=1.35)
    add_text(s, Inches(4.2), y + Inches(0.45), Inches(8.6), Inches(0.4),
             hint, size=10.5, color=TEXT_MUTED, line_spacing=1.3)
    add_hairline(s, Inches(0.55), y + Inches(0.88), Inches(12.25))
    y += Inches(0.88)


# =============================================================================
# 15 — Discovery · Security
# =============================================================================
s = add_slide(); page_chrome(s, 15, TOTAL, "Disco · Security", part=2)
section_title(s, "Bring security in (2 of 3 attendees)",
              "Security questions anchored on the shadow Cursor reality.",
              "The topic is already on their desk — 31 Pro users in mixed Privacy Mode. We name it.")

qs = [
    ("05", "Shadow Cursor",
     "\"The 31 Pro users in mixed Privacy Mode — has that triggered an internal review yet, or not?\"",
     "→ Surface the existing risk without dramatizing it."),
    ("06", "Sanction criteria",
     "\"What does an AI coding tool need to prove to be sanctioned at Figma — beyond SOC 2?\"",
     "→ Audit logs? Data residency? BYO-key? We note it to anticipate."),
    ("07", "Claude Code security posture",
     "\"How is the Claude Code evaluation going on the security side — what are you looking at alongside product capability?\"",
     "→ Reveals the comparison terrain. Privacy Mode is a differentiated argument."),
]
y = Inches(3.55)
for n, k, q, hint in qs:
    add_text(s, Inches(0.55), y, Inches(0.7), Inches(0.4),
             n, size=14, color=TEXT_MUTED, font=FONT_MONO)
    add_text(s, Inches(1.2), y, Inches(3), Inches(0.4),
             k, size=12.5, bold=True, color=TEXT)
    add_text(s, Inches(4.2), y, Inches(8.6), Inches(0.65),
             q, size=11.5, color=ACCENT_SOFT, line_spacing=1.35)
    add_text(s, Inches(4.2), y + Inches(0.6), Inches(8.6), Inches(0.4),
             hint, size=10.5, color=TEXT_MUTED, line_spacing=1.3)
    add_hairline(s, Inches(0.55), y + Inches(1.05), Inches(12.25))
    y += Inches(1.08)


# =============================================================================
# 16 — Why Cursor (calibrated for Figma)
# =============================================================================
s = add_slide(); page_chrome(s, 16, TOTAL, "Why Cursor", part=2)
section_title(s, "Three angles that match their reality",
              "Why Cursor — calibrated for this specific account.",
              "We take the 4 official differentiators and zoom them onto Figma.")

claims = [
    ("01", "VS Code fork = drop-in",
     "85% of the team is already on VS Code. Muscle memory, extensions, keymaps, "
     "settings carry over. Adoption cost ≈ 0."),
    ("02", "Large codebase performance",
     "C++/WASM editor + Rust/TS infra = complex repo. Exactly where Cursor outperforms — "
     "semantic search, indexing, retrieval."),
    ("03", "Model neutrality vs Claude Code",
     "Claude Code = Anthropic-locked. Cursor keeps SOTA access flowing — "
     "you don't bet the next year on a single provider."),
    ("04", "Platform, not just a tool",
     "Plan · write · review · debug · iterate in one environment. "
     "Not a CLI next to the IDE. Workflow integration > raw intelligence."),
]
y = Inches(3.55)
for n, k, body in claims:
    add_rect(s, Inches(0.55), y, Inches(12.25), Inches(0.78), BG_PANEL)
    add_rect(s, Inches(0.55), y, Inches(12.25), Emu(6350), HAIRLINE)
    add_text(s, Inches(0.85), y + Inches(0.15), Inches(0.6), Inches(0.5),
             n, size=18, color=TEXT_MUTED, font=FONT_MONO)
    add_text(s, Inches(1.75), y + Inches(0.15), Inches(3.7), Inches(0.5),
             k, size=14, bold=True, color=TEXT)
    add_text(s, Inches(5.65), y + Inches(0.17), Inches(7.1), Inches(0.55),
             body, size=11, color=TEXT_DIM, line_spacing=1.35)
    y += Inches(0.85)


# =============================================================================
# 17 — Privacy Mode + SOC 2
# =============================================================================
s = add_slide(); page_chrome(s, 17, TOTAL, "Security · Privacy Mode", part=2)
section_title(s, "Minute 13 — I raise it myself",
              "The topic is already with them. We resolve it.",
              "31 Pro users in mixed Privacy Mode = real existing risk. Here's how Cursor resolves it.")

items = [
    ("01", "Code not retained",
     "Customer code is not stored or retained — contractual, not a toggle."),
    ("02", "No training",
     "Code is not used to train models — neither ours, nor third-party providers'."),
    ("03", "Ephemeral requests",
     "Requests are isolated and ephemeral — no persistent prompt logs."),
    ("04", "Enterprise readiness",
     "SOC 2 · admin controls · visibility · SSO. Security ↔ security call within 7 days."),
    ("05", "Shadow → sanctioned",
     "The 31 current Pro users can switch to mandated Privacy Mode in < 1 day."),
]
y = Inches(3.55)
for n, k, body in items:
    add_text(s, Inches(0.55), y, Inches(0.7), Inches(0.5),
             n, size=15, color=TEXT_MUTED, font=FONT_MONO)
    add_text(s, Inches(1.4), y, Inches(3.5), Inches(0.5),
             k, size=13.5, bold=True, color=TEXT)
    add_text(s, Inches(5.2), y, Inches(7.6), Inches(0.7),
             body, size=11.5, color=TEXT_DIM, line_spacing=1.4)
    add_hairline(s, Inches(0.55), y + Inches(0.65), Inches(12.25))
    y += Inches(0.68)


# =============================================================================
# 18 — Close
# =============================================================================
s = add_slide(); page_chrome(s, 18, TOTAL, "Disco · Close", part=2)
section_title(s, "Minute 17 — the exit",
              "The exercise goal: a specific follow-up.",
              "Not a pilot. Not a 'let's reconnect.' A named meeting, dated, with a purpose.")

# central proposal box
add_rect(s, Inches(0.55), Inches(3.55), Inches(12.25), Inches(2.6), BG_PANEL)
add_rect(s, Inches(0.55), Inches(3.55), Inches(12.25), Emu(6350), HAIRLINE)
add_text(s, Inches(0.85), Inches(3.75), Inches(11), Inches(0.4),
         "PROPOSED FOLLOW-UP", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
add_text(s, Inches(0.85), Inches(4.15), Inches(11.5), Inches(0.7),
         "60 minutes, within 10 days — Cursor SE + Cursor Security ↔ Figma DevEx + AppSec.",
         size=17, bold=True, color=TEXT, line_spacing=1.3)
add_text(s, Inches(0.85), Inches(5.0), Inches(11.5), Inches(1.2),
         "Purpose: (1) technical scoping of a 20–30-engineer POC on a named repo, pre-defined metrics,\n"
         "Privacy Mode mandated; (2) parallel security review (SIG, pentest, architecture, DPA sent D-7).",
         size=12, color=TEXT_DIM, line_spacing=1.55)

# script line
add_text(s, Inches(0.55), Inches(6.45), Inches(12.25), Inches(0.5),
         "WHAT TO SAY", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
add_text(s, Inches(0.55), Inches(6.8), Inches(12.25), Inches(0.4),
         "\"Marcel, is it worth blocking 60 minutes within 10 days — you + security + our counterparts? "
         "I'll send you a draft agenda today.\"",
         size=12, color=ACCENT_SOFT, italic=True, line_spacing=1.4)


# =============================================================================
# 19 — PART 3 DIVIDER · Debrief
# =============================================================================
s = add_slide()
part_divider(s, 3, "REFLECTION & DEBRIEF",
             "10 minutes.\nStructured thinking.",
             "2–3 silent minutes to gather. Then: top insights · deal hypothesis ·\n"
             "strategic questions · risks · self-assessment.")
add_text(s, Inches(11.5), Inches(7.05), Inches(1.3), Inches(0.3),
         f"19 / {TOTAL:02d}", size=9, color=TEXT_MUTED,
         align=PP_ALIGN.RIGHT, font=FONT_MONO)


# =============================================================================
# 20 — Top insights + deal hypothesis
# =============================================================================
s = add_slide(); page_chrome(s, 20, TOTAL, "Debrief · Insights", part=3)
section_title(s, "To fill in during the 2 silent minutes",
              "Top 3–5 insights + deal hypothesis.",
              "Format: one insight = one observed fact from discovery + what it triggers.")

# left: insights template
add_rect(s, Inches(0.55), Inches(3.55), Inches(7.6), Inches(3.5), BG_PANEL)
add_rect(s, Inches(0.55), Inches(3.55), Inches(7.6), Emu(6350), HAIRLINE)
add_text(s, Inches(0.85), Inches(3.7), Inches(7), Inches(0.4),
         "TOP INSIGHTS (formulate live)", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
hypotheses = [
    "1. Does Marcel know about the 31? → if yes, potential champion; if no, visibility gap.",
    "2. Claude Code = real eval or scouting? → real urgency or parked.",
    "3. Senior IC opt-out on Copilot? → proof of quality gap, not tool absence.",
    "4. Security posture: blocking or facilitating? → deal velocity.",
    "5. Pre-allocated budget? → 3-month vs 9-month signature delay.",
]
yy = Inches(4.15)
for h in hypotheses:
    add_text(s, Inches(0.85), yy, Inches(7), Inches(0.5),
             h, size=11.5, color=TEXT, line_spacing=1.4)
    yy += Inches(0.55)

# right: deal hypothesis
add_rect(s, Inches(8.35), Inches(3.55), Inches(4.45), Inches(3.5), BG_PANEL_2)
add_rect(s, Inches(8.35), Inches(3.55), Inches(4.45), Emu(6350), HAIRLINE)
add_text(s, Inches(8.65), Inches(3.7), Inches(4), Inches(0.4),
         "DEAL HYPOTHESIS", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
add_text(s, Inches(8.65), Inches(4.1), Inches(4), Inches(2.6),
         "Typical setup:\n"
         "• Medium urgency (Claude Code\n   is in eval, not decision)\n"
         "• Champion TBD (Marcel? or a\n   staff IC among the 31 Pro?)\n"
         "• Security = real variable\n   (deal-maker or deal-killer)\n"
         "• Realistic deal: 60-day POC,\n   500–650 seats at 6–9 months.",
         size=11, color=TEXT, line_spacing=1.5)


# =============================================================================
# 21 — Strategic questions
# =============================================================================
s = add_slide(); page_chrome(s, 21, TOTAL, "Debrief · Strategic questions", part=3)
section_title(s, "The 4 questions from the prompt",
              "Pre-prepared answers — to reformulate live.",
              "Don't recite. Reformulate with what you heard in discovery.")

qa = [
    ("Why does Figma need an AI coding solution — Cursor or not?",
     "650 engineers on C++/WASM + Rust + TS = high-complexity work. Without a structured "
     "AI lever, senior talent looks for productivity elsewhere (internal or external)."),
    ("What happens if they do nothing for 3–6 months?",
     "Shadow Cursor grows from 31 to 100+. Claude Code may roll out without governance. "
     "The cost isn't the tool — it's uncontrolled security + patterns locked on Copilot."),
    ("Is there a credible champion? Evidence?",
     "To test: does Marcel know about the 31? Is a staff IC among them identifiable? "
     "Champion = someone who defends the deal when we're not in the room."),
    ("How is Cursor uniquely positioned?",
     "VS Code fork (drop-in for 85% of the team) + model neutrality (vs Claude Code) + "
     "large codebase performance (vs Copilot) + Privacy Mode (vs current shadow usage)."),
]
y = Inches(3.5)
for q, a in qa:
    add_text(s, Inches(0.55), y, Inches(0.3), Inches(0.4), "→", size=14, color=TEXT_MUTED)
    add_text(s, Inches(0.95), y, Inches(11.8), Inches(0.4),
             q, size=12.5, bold=True, color=TEXT)
    add_text(s, Inches(0.95), y + Inches(0.4), Inches(11.8), Inches(0.5),
             a, size=11, color=TEXT_DIM, line_spacing=1.4)
    add_hairline(s, Inches(0.55), y + Inches(0.92), Inches(12.25))
    y += Inches(0.92)


# =============================================================================
# 22 — Risks + self-assessment
# =============================================================================
s = add_slide(); page_chrome(s, 22, TOTAL, "Debrief · Risks + Self-assess", part=3)
section_title(s, "Anticipate, then self-critique",
              "Expected risks + what I would change.",
              "Self-aware > overconfident. Name the fragilities before they're called out.")

# left: deal risks
add_rect(s, Inches(0.55), Inches(3.55), Inches(6.1), Inches(3.5), BG_PANEL)
add_rect(s, Inches(0.55), Inches(3.55), Inches(6.1), Emu(6350), HAIRLINE)
add_text(s, Inches(0.85), Inches(3.7), Inches(5.5), Inches(0.4),
         "ANTICIPATED DEAL RISKS", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
risks = [
    ("Claude Code competition", "Eval may conclude 'good enough' before we ship our POC."),
    ("Security as blocker",     "If AppSec isn't addressed D0, pilot slips 3 months."),
    ("Internal politics",       "Copilot has an internal sponsor — switch read as a failure."),
    ("Tool sprawl",             "Cursor + Copilot + Claude Code in parallel = no one decides."),
    ("Procurement",             "Vendor risk review + DPA = 60–90 days, non-compressible."),
]
yy = Inches(4.15)
for k, v in risks:
    add_text(s, Inches(0.85), yy, Inches(2.0), Inches(0.4),
             k, size=11, bold=True, color=TEXT)
    add_text(s, Inches(2.9), yy, Inches(3.6), Inches(0.7),
             v, size=10.5, color=TEXT_DIM, line_spacing=1.3)
    yy += Inches(0.55)

# right: self-assessment
add_rect(s, Inches(6.85), Inches(3.55), Inches(5.95), Inches(3.5), BG_PANEL_2)
add_rect(s, Inches(6.85), Inches(3.55), Inches(5.95), Emu(6350), HAIRLINE)
add_text(s, Inches(7.15), Inches(3.7), Inches(5.5), Inches(0.4),
         "SELF-ASSESSMENT (template)", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
sa = [
    ("What worked",       "Opening on the 31 Pro = proof of prep.\nLetting Marcel articulate 'why now'."),
    ("What I'd change",   "More time on concrete use cases (refactors vs review).\nPush earlier on budget."),
    ("Greenfield → disco","Account thesis fuels targeted questions.\nKnown facts = wedges, not accessories."),
]
yy = Inches(4.15)
for k, v in sa:
    add_text(s, Inches(7.15), yy, Inches(5.5), Inches(0.4),
             k, size=11.5, bold=True, color=TEXT)
    add_text(s, Inches(7.15), yy + Inches(0.35), Inches(5.5), Inches(0.7),
             v, size=10.5, color=TEXT_DIM, line_spacing=1.4)
    yy += Inches(0.95)


# =============================================================================
# 23 — Anti-blank phrases
# =============================================================================
s = add_slide(); page_chrome(s, 23, TOTAL, "Anti-blank · key phrases", part=2)
section_title(s, "When you lose the thread",
              "6 phrases to use word-for-word.",
              "Take the wheel back without pitching. Keep executive presence under pressure.")

phrases = [
    ("If silence drags",     "\"I'd rather give you the time — this is your conversation.\""),
    ("If Cursor gets hit",   "\"Fair feedback — here's what we do well, here's where we're not the best.\""),
    ("If asked a number you don't know",
                             "\"I don't want to make one up — I'll get back to you with the real answer today.\""),
    ("To pressure-test",     "\"What would need to be true for this to be a no?\""),
    ("To pivot to security", "\"Before we go further, I want to open security — that's where this gets real.\""),
    ("To close",             "\"One question before we book the follow-up: what should I have asked?\""),
]
y = Inches(3.55); x_cols = [Inches(0.55), Inches(6.95)]
for i, (k, v) in enumerate(phrases):
    x = x_cols[i % 2]
    yy = y + (i // 2) * Inches(1.1)
    add_text(s, x, yy, Inches(5.85), Inches(0.4),
             k.upper(), size=10, color=TEXT_MUTED, letter_spacing=200, bold=True)
    add_text(s, x, yy + Inches(0.32), Inches(5.85), Inches(0.7),
             v, size=12, color=ACCENT_SOFT, italic=True, line_spacing=1.4)


# =============================================================================
# 24 — Meta · evaluation rubric (candidate-only)
# =============================================================================
s = add_slide(); page_chrome(s, 24, TOTAL, "Meta · candidate-only")
section_title(s, "Hide during the exercise",
              "What is actually being evaluated.",
              "Six dimensions, explicit in the prompt. To project actively across the full 60 min.")

add_rect(s, Inches(0.55), Inches(3.55), Inches(6.1), Inches(3.5), BG_PANEL)
add_rect(s, Inches(0.55), Inches(3.55), Inches(6.1), Emu(6350), HAIRLINE)
add_text(s, Inches(0.85), Inches(3.7), Inches(5.5), Inches(0.4),
         "WHAT'S BEING EVALUATED (from prompt)", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
eval_items = [
    "Strategic thinking & account thesis",
    "Enterprise stakeholder mapping",
    "Ability to CREATE urgency (not just respond)",
    "Quality + sequencing of discovery",
    "Executive presence & clarity of thought",
    "Structured thinking in debrief",
]
yy = Inches(4.15)
for item in eval_items:
    add_text(s, Inches(0.85), yy, Inches(0.3), Inches(0.4),
             "●", size=12, color=ACCENT_SOFT)
    add_text(s, Inches(1.2), yy, Inches(5.3), Inches(0.4),
             item, size=12, color=TEXT, line_spacing=1.4)
    yy += Inches(0.45)

add_rect(s, Inches(6.85), Inches(3.55), Inches(5.95), Inches(3.5), BG_PANEL_2)
add_rect(s, Inches(6.85), Inches(3.55), Inches(5.95), Emu(6350), HAIRLINE)
add_text(s, Inches(7.15), Inches(3.7), Inches(5.5), Inches(0.4),
         "SIGNALS (from Cursor prep doc)", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
add_text(s, Inches(7.15), Inches(4.1), Inches(5.5), Inches(0.4),
         "STRONG — to project", size=10, color=ACCENT_SOFT, letter_spacing=200, bold=True)
strong = ["Prepared", "Self-aware", "Composed", "Tactically sharp", "Coachable"]
yy = Inches(4.4)
for item in strong:
    add_text(s, Inches(7.15), yy, Inches(5.3), Inches(0.3),
             "● " + item, size=11.5, color=TEXT, line_spacing=1.4)
    yy += Inches(0.3)

add_text(s, Inches(7.15), Inches(6.0), Inches(5.5), Inches(0.4),
         "WEAK — to avoid", size=10, color=TEXT_MUTED, letter_spacing=200, bold=True)
weak = ["Feature dump", "AI hype", "Overconfident without grounding"]
yy = Inches(6.3)
for item in weak:
    add_text(s, Inches(7.15), yy, Inches(5.3), Inches(0.3),
             "○ " + item, size=11.5, color=TEXT_MUTED, line_spacing=1.4)
    yy += Inches(0.28)


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out = "/workspace/decks/Cursor_Enterprise_Disco_Challenge.pptx"
prs.save(out)
print(f"OK  →  {out}  ·  {len(prs.slides)} slides")
