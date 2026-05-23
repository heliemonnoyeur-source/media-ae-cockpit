"""
Cursor Enterprise — PG + Disco Challenge
Prep deck pour l'exercice d'entretien Cursor GTM (60 min, 3 parties).

V3 — affiné après lecture du « Cursor Enterprise: PG + Disco Challenge Prompt »
et du « 2026 Cursor GTM Discovery / Deal Review Interview Prep ».

Structure :
  Partie 1 — Greenfield Pipeline (Fortune 100)        20–25 min
  Partie 2 — Mock Discovery Call (Figma inbound)       20–25 min
  Partie 3 — Reflection & Debrief                      10–15 min
  Meta     — Ce qui est évalué (candidate-only)

Faits Figma connus (à exploiter dans la disco) :
  - Marcel Weekes, VP of Engineering, ~650 ingénieurs
  - ~85 % sur VS Code (drop-in pour Cursor — VS Code fork)
  - GitHub Copilot déployé sur toute l'équipe
  - Évaluent Claude Code en ce moment
  - 31 Cursor Pro users en shadow (Privacy Mode mixte)
  - Meeting : Marcel + Security Eng Leader + Security team member
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor


# ---------------------------------------------------------------------------
# Charte
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
         "~70 % des Fortune 1000 l'utilisent déjà.",
         size=15, color=TEXT_DIM, line_spacing=1.4, italic=True)

add_text(s, Inches(8.6), Inches(2.2), Inches(4), Inches(0.4),
         "STRUCTURE", size=10, color=TEXT_MUTED, letter_spacing=300)
add_text(s, Inches(8.6), Inches(2.6), Inches(4.5), Inches(3.5),
         "P1 · Greenfield F100  (20–25')\n"
         "P2 · Mock Disco Figma  (20–25')\n"
         "P3 · Reflection & Debrief  (10–15')",
         size=14, color=TEXT, line_spacing=2.0)

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
section_title(s, "60 minutes, trois exercices connectés",
              "Comment le temps va passer.",
              "Account-development mindset informe la discovery. Une histoire, trois preuves.")

rows = [
    ("PART 1", "0–25 min",
     "Greenfield Pipeline (F100)",
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
             "GTM Iberia + Italie. Top 5 ranked, deep dive sur Santander :\n"
             "account thesis, stakeholder map, entry sequencing, first 90 days.")
add_text(s, Inches(11.5), Inches(7.05), Inches(1.3), Inches(0.3),
         f"03 / {TOTAL:02d}", size=9, color=TEXT_MUTED,
         align=PP_ALIGN.RIGHT, font=FONT_MONO)


# =============================================================================
# 04 — Critères de sélection F100
# =============================================================================
s = add_slide(); page_chrome(s, 4, TOTAL, "Critères de ranking", part=1)
section_title(s, "Avant le Top 5",
              "Comment je classe un compte ENT Spain & Italy.",
              "Cinq lentilles, pondérées. Toute exception = on cherche pourquoi.")

crits = [
    ("01 · Eng headcount",
     "≥ 5 K ingés pour un deal enterprise pertinent. Plus c'est gros, plus le math ROI parle."),
    ("02 · AI mandate public",
     "Roadmap IA exécutive annoncée → champion réception facilitée, urgence existante."),
    ("03 · Reg / privacy posture",
     "Régulés EU (DORA, EU AI Act, ECB) = Privacy Mode = enabler, pas blocker. Notre edge."),
    ("04 · Codebase complexité",
     "Legacy + modern + mono / multi repo = large codebase performance pertinent."),
    ("05 · Procurement reach",
     "Équipe dev-tools identifiable + path procurement traçable = vélocité de deal."),
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
# 05 — Top 5 Fortune 100
# =============================================================================
s = add_slide(); page_chrome(s, 5, TOTAL, "Top 5 prospects", part=1)
section_title(s, "Greenfield · ranked",
              "Top 5 GTM Spain & Italy.",
              "Ranking défendable. Santander en #1 → deep-dive sur les 4 slides qui suivent.")

prospects = [
    ("#1", "Santander",
     "~15–20 K tech · « One Transformation » sous Dirk Marzluf · régulé multi-juridictions · Openbank = wedge digital-native.",
     "Plus gros TAM Iberia + champion-ready."),
    ("#2", "BBVA",
     "~10 K tech · ChatGPT Enterprise déjà déployé org-wide · narrative « born digital » sous Carlos Torres.",
     "AI-ready buyer, vélocité forte."),
    ("#3", "Enel",
     "~15 K tech · transition énergétique = urgence · OpenInnovability AI lab · CISO mature.",
     "Plus gros TAM Italie."),
    ("#4", "EssilorLuxottica",
     "~5–7 K tech / 190 K total · Industry 4.0 + e-commerce push · régulé (medical devices).",
     "Compte FR/IT, leverage industriel."),
    ("#5", "El Corte Inglés",
     "~2–3 K tech · transformation e-commerce + supply chain sous Marta Álvarez · moins de concurrence.",
     "Moins crowded, deal accessible."),
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
# 06 — #1 JPMorgan : Account thesis
# =============================================================================
s = add_slide(); page_chrome(s, 6, TOTAL, "Deep dive · Santander", part=1)
section_title(s, "Top prospect · Account thesis",
              "Santander — why now, where Cursor wins.",
              "4 angles. Tous ont une preuve publique citable (analyst calls, presse Iberia).")

cols = [
    ("WHY SANTANDER",
     "~15–20 K tech (Santander Global\nT&O + Openbank + Cardinal).\nAna Botín mentionne l'IA à chaque\nresults call.\nPartenariats OpenAI + Google Cloud\nannoncés en 2024."),
    ("WHY NOW",
     "« One Transformation » T&O lancée\n2024 sous Dirk Marzluf.\nBBVA a déployé ChatGPT Enterprise\norg-wide → pression compétitive directe.\nDORA + EU AI Act = urgence\ngouvernance IA."),
    ("LEVIERS CURSOR",
     "Velocity (Openbank, digital-native).\nGovernance (Privacy Mode pour\nECB / BoE / Fed).\nOnboarding (rotations 10+ pays).\nCost (réduction IT spend / revenue)."),
    ("FORCES MARCHÉ",
     "Talent IA cher en Iberia →\noutil = levier hiring & rétention.\nModel neutrality = résilience face à\nl'écosystème EU souverain.\nClaude Code en éval chez les pairs\nEuropéens (ING, BNP)."),
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
# 07 — JPMorgan : Stakeholder map
# =============================================================================
s = add_slide(); page_chrome(s, 7, TOTAL, "Santander · Stakeholders", part=1)
section_title(s, "Engineering org map",
              "Qui je cible, dans quel ordre, et pourquoi.",
              "Power signals : budget T&O, hiring T&O Madrid/London, sponsorship d'initiatives IA Botín-niveau.")

stk = [
    ("01", "Openbank CTO + Head of Engineering",
     "Wedge #1. Filiale digital-native, autonome, procurement plus court.",
     "Cold + LinkedIn. Message : « pilote 30 j sur 1 squad, métriques pré-définies »."),
    ("02", "Dir / VP Developer Productivity — Santander T&O",
     "Buyer économique au niveau Groupe. Porte le budget dev tools.",
     "Warm intro Madrid tech community + ref customer EU bank si dispo."),
    ("03", "AppSec leadership (sous le CISO Groupe)",
     "Gatekeeper. Pas un blocker si Privacy Mode + SOC 2 + DORA-aligned anticipés.",
     "On les inclut tôt, on envoie SIG + pentest + DPA avant de demander."),
    ("04", "Dirk Marzluf (Group Head of T&O)",
     "Exec sponsor. Pas en first touch — on l'engage quand on a un POC chiffré.",
     "Une fois POC live : board-level ROI + risk reduction story."),
    ("05", "Engineers (bottom-up)",
     "Adoption shadow = signal Marcel-style. Free tier monitoring sur emails Santander.",
     "On surveille signups, on identifie un staff IC champion à Madrid."),
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
# 08 — JPMorgan : Entry points & 90 days
# =============================================================================
s = add_slide(); page_chrome(s, 8, TOTAL, "Santander · Entry + 90 days", part=1)
section_title(s, "Pipeline & sequencing",
              "Comment je crée le momentum.",
              "Outreach multi-canal, séquencé, mesurable. 90 jours pour un POC Openbank chiffré.")

# left: entry channels
add_rect(s, Inches(0.55), Inches(3.55), Inches(6.1), Inches(3.55), BG_PANEL)
add_rect(s, Inches(0.55), Inches(3.55), Inches(6.1), Emu(6350), HAIRLINE)
add_text(s, Inches(0.85), Inches(3.7), Inches(5.5), Inches(0.4),
         "ENTRY POINTS — séquencés", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
entries = [
    ("Openbank-first", "Wedge digital-native. Cible Openbank CTO + Head of Eng. Procurement plus court."),
    ("Cold outbound", "Dir DevProd Santander T&O + AppSec, 3 touches/sem, ROI + ref EU bank."),
    ("Warm intro", "Madrid tech community (South Summit, Endeavor, Wayra alumni). Petit monde."),
    ("Conférence", "South Summit Madrid · Money 20/20 Europe · DevOpsCon Madrid."),
    ("Bottom-up", "Free tier monitoring sur @santander.com → champion IC à Madrid/Boston."),
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
    ("J0–J30", "Research Openbank + Santander T&O.\n3 cold touches/sem + 1 warm intro Madrid.\nSuccess : 1 mtg Openbank CTO, 1 mtg AppSec."),
    ("J30–J60", "Discovery Openbank + parallel intro T&O.\nSuccess : POC 20–30 ingés signé sur 1 squad\nOpenbank (mobile ou backend)."),
    ("J60–J90", "POC live, Privacy Mode mandaté + DORA-aligned.\nSuccess : cycle-time + PR + NPS mesurés.\nOuvre conversation Groupe T&O sur 1 K+ seats."),
]
yy = Inches(4.1)
for k, v in days:
    add_text(s, Inches(7.15), yy, Inches(1.0), Inches(0.4),
             k, size=11, bold=True, color=TEXT, font=FONT_MONO)
    add_text(s, Inches(8.25), yy, Inches(4.4), Inches(1.0),
             v, size=10.5, color=TEXT_DIM, line_spacing=1.35)
    yy += Inches(0.92)


# =============================================================================
# 09 — JPMorgan : Pilot motion
# =============================================================================
s = add_slide(); page_chrome(s, 9, TOTAL, "Santander · Pilot motion", part=1)
section_title(s, "Initial pilot motion · Openbank wedge",
              "À quoi ressemble le POC chiffré.",
              "Openbank = path of least resistance. Success ici ouvre la conversation Groupe T&O sur 1 K+ seats.")

cols = [
    ("SCOPE",
     "20–30 ingés Openbank (digital-native,\nstack moderne, vélocité élevée).\n30 jours.\n1 squad mobile ou backend, 1 repo de\nréférence."),
    ("MÉTRIQUES",
     "Cycle time (PR opened → merged)\nPR throughput / ingé / semaine\nSenior IC adoption rate\nNPS engagement à J+15 et J+30."),
    ("SECURITY DAY 1",
     "Privacy Mode obligatoire.\nSOC 2 + SIG envoyés J-7.\nDORA-aligned : audit logs, data\nresidency EU validés.\nAppSec Groupe dans la loop dès J0."),
    ("EXIT GATE",
     "Cycle-time ↓ ≥ 12 %\nNPS ≥ 50\nSenior IC adoption ≥ 60 %\n→ ouvre Groupe T&O sur Santander\nGlobal Tech : 1 000–5 000 seats."),
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
             "VP Eng · ~650 ingénieurs · 85 % VS Code · Copilot déployé ·\n"
             "Claude Code en évaluation · 31 Cursor Pro shadow (Privacy Mode mixte).")
add_text(s, Inches(11.5), Inches(7.05), Inches(1.3), Inches(0.3),
         f"10 / {TOTAL:02d}", size=9, color=TEXT_MUTED,
         align=PP_ALIGN.RIGHT, font=FONT_MONO)


# =============================================================================
# 11 — Brief Figma : faits connus
# =============================================================================
s = add_slide(); page_chrome(s, 11, TOTAL, "Brief · Figma", part=2)
section_title(s, "Ce qu'on sait avant d'entrer",
              "Le brief, en 6 faits.",
              "Chaque fait est un levier discovery. On les exploite — pas on les répète.")

facts = [
    ("Marcel Weekes",     "VP of Engineering, leads ~650 engineers.",
     "→ Buyer économique principal. KPI : vélocité, talent."),
    ("~85 % sur VS Code", "Standard interne dominant.",
     "→ Cursor = VS Code fork. Drop-in. Muscle memory transfer."),
    ("GitHub Copilot",    "Déployé sur toute l'équipe.",
     "→ Baseline connu. « Why change » = quality gap, pas absence d'outil."),
    ("Claude Code eval",  "En évaluation active en ce moment.",
     "→ THE compétiteur. Why now est déjà établi de leur côté."),
    ("31 Cursor Pro",     "Shadow usage interne, Privacy Mode mixte.",
     "→ Or pur. Champion silencieux + risque sécu = leur problème, notre wedge."),
    ("Attendees",         "Marcel + Security Eng Leader + Security IC.",
     "→ 2/3 sécu. La conversation est sécurité-first, pas velocity-first."),
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
# 12 — Agenda 20 min (Figma)
# =============================================================================
s = add_slide(); page_chrome(s, 12, TOTAL, "Disco · Agenda", part=2)
section_title(s, "Structure du call",
              "20–25 minutes, timeboxé.",
              "Marcel parle d'abord. Sécu entre minute 5. Goal = follow-up précis, pas pilote.")

rows = [
    ("0:00 – 1:30",  "Cadrage",                "Agenda · permission · ancrage sur les 31 Pro users."),
    ("1:30 – 9:30",  "Discovery",              "Marcel d'abord, Sécurité à partir de 5:00."),
    ("9:30 – 13:00", "Thèse + 1 proof point",  "Why now (urgence eux) · why Cursor (vs Claude Code)."),
    ("13:00 – 17:00","Sécurité",               "Privacy Mode 3 bullets + SOC 2. J'ouvre, pas eux."),
    ("17:00 – 20:00","Next step précis",       "Follow-up nommé : qui, quand, pour quoi faire."),
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
# 13 — Opener (script Marcel-spécifique)
# =============================================================================
s = add_slide(); page_chrome(s, 13, TOTAL, "Disco · Opener", part=2)
section_title(s, "Les 90 premières secondes",
              "Script d'ouverture.",
              "Préparation visible (nom, faits) · pas de pitch · pré-engagement sur l'agenda.")

add_rect(s, Inches(0.55), Inches(3.55), Inches(12.25), Inches(3.25), BG_PANEL)
add_rect(s, Inches(0.55), Inches(3.55), Inches(12.25), Emu(6350), HAIRLINE)
add_text(s, Inches(0.9), Inches(3.8), Inches(0.5), Inches(0.4),
         "“", size=44, color=TEXT_MUTED, font="Georgia")
add_text(s, Inches(1.35), Inches(3.95), Inches(11.1), Inches(2.8),
         "Marcel, merci pour ces 20 minutes — et merci à [Security Eng Lead] et "
         "[Sec team member] de vous être joints, c'est exactement la configuration "
         "la plus utile pour cette conversation. Avant de commencer : j'ai noté que "
         "31 de vos ingénieurs sont déjà sur Cursor Pro en mode mixte. Plutôt que "
         "de pitcher, je préfère partir de cette réalité — comprendre ce que vous "
         "en voyez en interne, ce qui pousse l'évaluation Claude Code en parallèle, "
         "et où vous voulez emmener tout ça à 6 mois. Je vais passer le plus clair "
         "du temps à poser des questions. Goal côté Cursor : un follow-up précis et "
         "utile, pas un pitch. Ça vous va comme cadrage ?",
         size=14, color=TEXT, line_spacing=1.55)

add_text(s, Inches(0.55), Inches(6.95), Inches(12), Inches(0.3),
         "EFFETS — préparation visible (31 Pro, Claude Code) · self-aware (pas de pitch) · "
         "pré-engagement · sécu impliquée dès le mot 1",
         size=10, color=TEXT_MUTED, letter_spacing=80)


# =============================================================================
# 14 — Discovery · Marcel
# =============================================================================
s = add_slide(); page_chrome(s, 14, TOTAL, "Disco · Marcel", part=2)
section_title(s, "8 minutes · VP of Engineering",
              "Questions ancrées sur les faits.",
              "Chaque question pointe un fait connu. Pas de question générique.")

qs = [
    ("01", "Origine du shadow",
     "« 31 ingés sur Cursor Pro — comment c'est arrivé, et qu'est-ce qu'ils en disent quand vous leur demandez ? »",
     "→ Bottom-up signal. Si Marcel l'ignorait, c'est un trou de visibilité = wedge."),
    ("02", "Pressure-test Claude Code",
     "« Qu'est-ce qui vous a fait regarder Claude Code maintenant plutôt qu'il y a 6 mois, et qu'est-ce que vous attendez d'un éventuel switch ? »",
     "→ Le « why now » est ici. On laisse Marcel le formuler à notre place."),
    ("03", "Gap Copilot",
     "« Copilot est déployé wall-to-wall — quel est le travail qui devrait être assisté et ne l'est pas aujourd'hui ? »",
     "→ Refactos · large context · review. Là où Cursor a un edge tangible."),
    ("04", "Senior IC opt-out",
     "« Les seniors et les juniors utilisent Copilot pareil ? Y a-t-il un tier qui a discrètement décroché ? »",
     "→ Senior opt-out = plafond ROI ~5 %. Notre meilleure preuve de gap."),
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
s = add_slide(); page_chrome(s, 15, TOTAL, "Disco · Sécurité", part=2)
section_title(s, "Embarquer la sécurité (2/3 attendees)",
              "Questions sécurité ancrées sur le shadow Cursor.",
              "Le sujet est déjà sur leur table — 31 Pro users en mode mixte. On le nomme.")

qs = [
    ("05", "Shadow Cursor",
     "« Les 31 utilisateurs Pro avec Privacy Mode mixte — ça a déclenché un review interne, ou pas encore ? »",
     "→ Pose la réalité du risque actuel sans la dramatiser."),
    ("06", "Critères de sanction",
     "« Qu'est-ce qu'un outil IA de code doit prouver pour être sanctionné chez Figma — au-delà de SOC 2 ? »",
     "→ Audit logs ? Data residency ? BYO-key ? On note pour anticiper."),
    ("07", "Posture Claude Code",
     "« Comment l'évaluation Claude Code se passe côté sécurité — qu'est-ce que vous regardez en parallèle de la capacité produit ? »",
     "→ Donne le terrain de comparaison. Privacy Mode est un argument différenciateur."),
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
# 16 — Why Cursor (vs Claude Code + VS Code angle)
# =============================================================================
s = add_slide(); page_chrome(s, 16, TOTAL, "Why Cursor", part=2)
section_title(s, "Trois angles qui matchent leur réalité",
              "Pourquoi Cursor — calibré pour ce dossier précis.",
              "On reprend les 4 différenciateurs officiels et on les zoom sur Figma.")

claims = [
    ("01", "VS Code fork = drop-in",
     "85 % de l'équipe est déjà sur VS Code. Muscle memory, extensions, "
     "keymaps, settings transfèrent. Coût d'adoption ≈ 0."),
    ("02", "Large codebase performance",
     "Éditeur C++/WASM + infra Rust/TS = repo complexe. C'est exactement "
     "le terrain où Cursor surperforme — semantic search, indexing, retrieval."),
    ("03", "Model neutrality vs Claude Code",
     "Claude Code = Anthropic-locked. Cursor donne accès au SOTA en continu — "
     "vous ne pariez pas la prochaine année sur un seul provider."),
    ("04", "Platform, not just a tool",
     "Plan · write · review · debug · iterate dans un seul environnement. "
     "Pas un CLI à côté de l'IDE. Workflow integration > intelligence brute."),
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
# 17 — Privacy Mode (3 bullets exacts) + SOC 2
# =============================================================================
s = add_slide(); page_chrome(s, 17, TOTAL, "Sécurité · Privacy Mode", part=2)
section_title(s, "Minute 13 — je l'ouvre moi-même",
              "Le sujet est déjà chez eux. On le tranche.",
              "31 Pro users en Privacy Mode mixte = le risque est déjà réel. Voici comment Cursor le règle.")

items = [
    ("01", "Code non-stocké",
     "Customer code is not stored or retained — c'est contractuel, pas un toggle."),
    ("02", "Pas d'entraînement",
     "Code is not used to train models — ni les nôtres, ni ceux des providers tiers."),
    ("03", "Requêtes éphémères",
     "Requests are isolated and ephemeral — pas de log persistant des prompts."),
    ("04", "Enterprise readiness",
     "SOC 2 · contrôles admin · visibilité · SSO. Call security ↔ security sous 7 jours."),
    ("05", "Conversion shadow → sanctionné",
     "Les 31 Pro users actuels peuvent basculer en Privacy Mode mandaté en < 1 jour."),
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
# 18 — Close : follow-up précis
# =============================================================================
s = add_slide(); page_chrome(s, 18, TOTAL, "Disco · Close", part=2)
section_title(s, "Minute 17 — la sortie",
              "Goal de l'exercice : un follow-up précis.",
              "Pas un pilote. Pas un « on se rappelle ». Un meeting nommé, daté, avec un purpose.")

# central proposal box
add_rect(s, Inches(0.55), Inches(3.55), Inches(12.25), Inches(2.6), BG_PANEL)
add_rect(s, Inches(0.55), Inches(3.55), Inches(12.25), Emu(6350), HAIRLINE)
add_text(s, Inches(0.85), Inches(3.75), Inches(11), Inches(0.4),
         "FOLLOW-UP PROPOSÉ", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
add_text(s, Inches(0.85), Inches(4.15), Inches(11.5), Inches(0.7),
         "60 min, sous 10 jours — Cursor SE + Cursor Security ↔ Figma DevEx + AppSec.",
         size=18, bold=True, color=TEXT, line_spacing=1.3)
add_text(s, Inches(0.85), Inches(5.0), Inches(11.5), Inches(1.2),
         "Purpose : (1) scoping technique d'un POC 20–30 ingés sur un repo nommé, métriques pré-définies,\n"
         "Privacy Mode mandaté ; (2) review sécu parallèle (SIG, pentest, archi, DPA envoyés J-7).",
         size=12, color=TEXT_DIM, line_spacing=1.55)

# script line
add_text(s, Inches(0.55), Inches(6.45), Inches(12.25), Inches(0.5),
         "PHRASE À DIRE", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
add_text(s, Inches(0.55), Inches(6.8), Inches(12.25), Inches(0.4),
         "« Marcel, ça vaut le coup qu'on bloque 60 min sous 10 jours, vous + sécu + nos équivalents ? "
         "Je vous envoie le draft d'agenda dans la journée. »",
         size=12, color=ACCENT_SOFT, italic=True, line_spacing=1.4)


# =============================================================================
# 19 — PART 3 DIVIDER · Debrief
# =============================================================================
s = add_slide()
part_divider(s, 3, "REFLECTION & DEBRIEF",
             "10 minutes.\nStructured thinking.",
             "2–3 min silencieuses pour rassembler. Puis : top insights · deal hypothesis ·\n"
             "questions stratégiques · risks · self-assessment.")
add_text(s, Inches(11.5), Inches(7.05), Inches(1.3), Inches(0.3),
         f"19 / {TOTAL:02d}", size=9, color=TEXT_MUTED,
         align=PP_ALIGN.RIGHT, font=FONT_MONO)


# =============================================================================
# 20 — Top insights + deal hypothesis (template)
# =============================================================================
s = add_slide(); page_chrome(s, 20, TOTAL, "Debrief · Insights", part=3)
section_title(s, "À remplir pendant les 2 min silencieuses",
              "Top 3–5 insights + hypothèse de deal.",
              "Format : un insight = un fait observé en disco + ce qu'il déclenche.")

# left: insights template
add_rect(s, Inches(0.55), Inches(3.55), Inches(7.6), Inches(3.5), BG_PANEL)
add_rect(s, Inches(0.55), Inches(3.55), Inches(7.6), Emu(6350), HAIRLINE)
add_text(s, Inches(0.85), Inches(3.7), Inches(7), Inches(0.4),
         "TOP INSIGHTS (à formuler en live)", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
hypotheses = [
    "1. Marcel sait pour les 31 ? → si oui, champion potentiel ; si non, trou de visibilité.",
    "2. Claude Code = vrai eval ou veille ? → urgence réelle ou parking.",
    "3. Senior IC opt-out sur Copilot ? → preuve de gap quality, pas absence d'outil.",
    "4. Posture sécu : bloquant ou facilitant ? → vitesse de deal.",
    "5. Budget pré-alloué ? → délai de signature 3 mois vs 9 mois.",
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
         "Setup typique :\n"
         "• Urgence moyenne (Claude Code\n   est en eval, pas en décision)\n"
         "• Champion à confirmer (Marcel ?\n   ou un staff IC sur les 31 Pro ?)\n"
         "• Sécu = vraie variable\n   (deal-maker ou deal-killer)\n"
         "• Deal réaliste : POC à 60 j,\n   500–650 seats à 6–9 mois.",
         size=11, color=TEXT, line_spacing=1.5)


# =============================================================================
# 21 — Strategic questions (4 from the prompt, with answers)
# =============================================================================
s = add_slide(); page_chrome(s, 21, TOTAL, "Debrief · Questions stratégiques", part=3)
section_title(s, "Les 4 questions du prompt",
              "Réponses préparées — à reformuler à chaud.",
              "Ne pas réciter. Reformuler avec ce qu'on aura entendu en disco.")

qa = [
    ("Pourquoi Figma a besoin d'une solution IA coding — Cursor ou pas ?",
     "650 ingés sur du C++/WASM + Rust + TS = travail à haute complexité. Sans levier IA "
     "structuré, le talent senior va chercher la productivité ailleurs (interne ou externe)."),
    ("Que se passe-t-il s'ils ne font rien pendant 3–6 mois ?",
     "Shadow Cursor monte de 31 à 100+. Claude Code peut-être déployé sans gouvernance. "
     "Le coût n'est pas l'outil — c'est la sécurité non-contrôlée + patterns figés sur Copilot."),
    ("Y a-t-il un champion crédible ? Preuves ?",
     "À tester : Marcel sait-il pour les 31 ? Un staff IC parmi eux est-il identifiable ? "
     "Champion = quelqu'un qui défend le deal quand on n'est pas dans la salle."),
    ("Comment Cursor est-il uniquement positionné ?",
     "VS Code fork (drop-in pour 85 % de l'équipe) + model neutrality (vs Claude Code) + "
     "large codebase performance (vs Copilot) + Privacy Mode (vs shadow actuel)."),
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
# 22 — Deal risks + self-assessment
# =============================================================================
s = add_slide(); page_chrome(s, 22, TOTAL, "Debrief · Risks + Self-assess", part=3)
section_title(s, "Anticiper, puis se critiquer",
              "Risks attendus + qu'est-ce que je changerais.",
              "Self-aware > overconfident. Nommer les fragilités avant qu'on les pointe.")

# left: deal risks
add_rect(s, Inches(0.55), Inches(3.55), Inches(6.1), Inches(3.5), BG_PANEL)
add_rect(s, Inches(0.55), Inches(3.55), Inches(6.1), Emu(6350), HAIRLINE)
add_text(s, Inches(0.85), Inches(3.7), Inches(5.5), Inches(0.4),
         "DEAL RISKS ANTICIPÉS", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
risks = [
    ("Compétition Claude Code", "L'eval peut conclure « assez bon » avant qu'on ait livré le POC."),
    ("Sécurité bloquante",      "Si AppSec n'est pas adressé J0, le pilote glisse de 3 mois."),
    ("Politique interne",       "Copilot a un sponsor org — switch perçu comme un échec interne."),
    ("Sprawl outils",           "Cursor + Copilot + Claude Code en parallèle = personne ne décide."),
    ("Procurement",             "Vendor risk review + DPA = 60–90 j incompressibles."),
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
    ("Ce qui a marché",  "Ouvrir sur les 31 Pro = preuve de prep.\nLaisser Marcel formuler le « why now »."),
    ("Ce que je changerais", "Plus de temps sur les use-cases concrets (refactos vs review).\nPousser plus tôt sur le budget."),
    ("Greenfield → disco", "Account thesis nourrit les questions ciblées.\nFaits connus = wedges, pas accessoires."),
]
yy = Inches(4.15)
for k, v in sa:
    add_text(s, Inches(7.15), yy, Inches(5.5), Inches(0.4),
             k, size=11.5, bold=True, color=TEXT)
    add_text(s, Inches(7.15), yy + Inches(0.35), Inches(5.5), Inches(0.7),
             v, size=10.5, color=TEXT_DIM, line_spacing=1.4)
    yy += Inches(0.95)


# =============================================================================
# 23 — Phrases-clés à mémoriser (anti-blank)
# =============================================================================
s = add_slide(); page_chrome(s, 23, TOTAL, "Anti-blank · phrases clés", part=2)
section_title(s, "Quand on perd le fil",
              "6 phrases à dire mot pour mot.",
              "Reprendre la main sans pitcher. Garder l'executive presence sous pression.")

phrases = [
    ("Si le silence dure", "« Je préfère vous laisser le temps — c'est votre conversation. »"),
    ("Si on tape sur Cursor",
     "« C'est un retour fair — voilà ce qu'on fait bien, voilà où on n'est pas le meilleur. »"),
    ("Si on demande un chiffre qu'on ignore",
     "« Je ne veux pas inventer — je vous reviens dans la journée avec la vraie réponse. »"),
    ("Pour pressure-test", "« Qu'est-ce qui devrait être vrai pour que ce soit un non ? »"),
    ("Pour passer à la sécu", "« Avant qu'on aille plus loin, je veux ouvrir la sécu — c'est là où ça se joue. »"),
    ("Pour clore", "« Une question avant qu'on bloque le follow-up : qu'est-ce que j'aurais dû demander ? »"),
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
# 24 — Meta · rubrique d'éval (candidate-only)
# =============================================================================
s = add_slide(); page_chrome(s, 24, TOTAL, "Meta · candidate-only")
section_title(s, "À masquer pendant l'exercice",
              "Ce qui est vraiment évalué.",
              "Six dimensions, explicites dans le prompt. À émettre activement les 60 min.")

# Two-column: what they evaluate + strong/weak signals
add_rect(s, Inches(0.55), Inches(3.55), Inches(6.1), Inches(3.5), BG_PANEL)
add_rect(s, Inches(0.55), Inches(3.55), Inches(6.1), Emu(6350), HAIRLINE)
add_text(s, Inches(0.85), Inches(3.7), Inches(5.5), Inches(0.4),
         "CE QUI EST ÉVALUÉ (du prompt)", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
eval_items = [
    "Strategic thinking & account thesis",
    "Enterprise stakeholder mapping",
    "Ability to CREATE urgency (not just respond)",
    "Quality + sequencing of discovery",
    "Executive presence & clarity",
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
         "SIGNAUX (du doc Cursor)", size=10, color=TEXT_MUTED, letter_spacing=300, bold=True)
add_text(s, Inches(7.15), Inches(4.1), Inches(5.5), Inches(0.4),
         "FORTS — à émettre", size=10, color=ACCENT_SOFT, letter_spacing=200, bold=True)
strong = ["Prepared", "Self-aware", "Composed", "Tactically sharp", "Coachable"]
yy = Inches(4.4)
for item in strong:
    add_text(s, Inches(7.15), yy, Inches(5.3), Inches(0.3),
             "● " + item, size=11.5, color=TEXT, line_spacing=1.4)
    yy += Inches(0.3)

add_text(s, Inches(7.15), Inches(6.0), Inches(5.5), Inches(0.4),
         "FAIBLES — à éviter", size=10, color=TEXT_MUTED, letter_spacing=200, bold=True)
weak = ["Feature dump", "AI hype", "Overconfident sans grounding"]
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
