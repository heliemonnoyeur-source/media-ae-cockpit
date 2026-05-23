"""
Cursor x Figma — Discovery CTO/CISO (20 min)
Génère un deck .pptx au look & feel Cursor (dark, minimal, moderne).

Le template officiel Cursor n'étant pas disponible dans ce workspace,
on recrée la charte: fond #0A0A0A, texte blanc, accent #A0A0A0 / #E5E5E5,
typographies sans-serif système (Inter à défaut), grille aérée 16:9.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
# (fallback import removed)
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

# python-pptx exposes RGBColor at pptx.dml.color
from pptx.dml.color import RGBColor  # noqa: F811

# ---------------------------------------------------------------------------
# Charte
# ---------------------------------------------------------------------------
BG          = RGBColor(0x0A, 0x0A, 0x0A)   # near-black
BG_PANEL    = RGBColor(0x14, 0x14, 0x14)   # subtle panel
HAIRLINE    = RGBColor(0x2A, 0x2A, 0x2A)   # dividers
TEXT        = RGBColor(0xF5, 0xF5, 0xF5)   # primary text
TEXT_DIM    = RGBColor(0xA0, 0xA0, 0xA0)   # secondary
TEXT_MUTED  = RGBColor(0x6B, 0x6B, 0x6B)   # tertiary / labels
ACCENT      = RGBColor(0xFF, 0xFF, 0xFF)   # Cursor accents are usually monochrome
ACCENT_SOFT = RGBColor(0xE5, 0xE5, 0xE5)

FONT = "Inter"          # tombe sur Helvetica / Arial si indispo
FONT_MONO = "JetBrains Mono"

# 16:9
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
             line_spacing=1.15, letter_spacing=None):
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
        r.font.color.rgb = color
        if letter_spacing is not None:
            # tracking via XML (spc in 1/100 pt)
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
    return add_rect(slide, x, y, w, Emu(6350), HAIRLINE)  # ~0.5pt


def page_chrome(slide, page_num, total, section_label):
    # top-left wordmark
    add_text(slide, Inches(0.55), Inches(0.35), Inches(3), Inches(0.4),
             "● cursor", size=11, color=TEXT, bold=True, letter_spacing=20)
    # top-right section
    add_text(slide, Inches(9.5), Inches(0.35), Inches(3.3), Inches(0.4),
             section_label.upper(), size=9, color=TEXT_MUTED,
             align=PP_ALIGN.RIGHT, letter_spacing=200)
    # bottom-left meta
    add_text(slide, Inches(0.55), Inches(7.05), Inches(6), Inches(0.3),
             "Cursor × Figma  ·  Discovery CTO / CISO  ·  20 min",
             size=9, color=TEXT_MUTED, letter_spacing=80)
    # bottom-right page number
    add_text(slide, Inches(11.5), Inches(7.05), Inches(1.3), Inches(0.3),
             f"{page_num:02d} / {total:02d}",
             size=9, color=TEXT_MUTED, align=PP_ALIGN.RIGHT,
             font=FONT_MONO, letter_spacing=50)
    # hairline under header
    add_hairline(slide, Inches(0.55), Inches(0.85), Inches(12.25))


def section_title(slide, kicker, title, subtitle=None):
    add_text(slide, Inches(0.55), Inches(1.25), Inches(8), Inches(0.4),
             kicker.upper(), size=10, color=TEXT_MUTED, letter_spacing=300)
    add_text(slide, Inches(0.55), Inches(1.65), Inches(12), Inches(1.2),
             title, size=36, bold=True, color=TEXT, line_spacing=1.05)
    if subtitle:
        add_text(slide, Inches(0.55), Inches(2.85), Inches(12), Inches(0.6),
                 subtitle, size=15, color=TEXT_DIM, line_spacing=1.3)


# ---------------------------------------------------------------------------
# Slides
# ---------------------------------------------------------------------------

TOTAL = 16  # mis à jour à la main

# --- 01 — Cover ---------------------------------------------------------------
s = add_slide()
# subtle panel à droite
add_rect(s, Inches(8.2), 0, Inches(5.13), SH, BG_PANEL)
# vertical hairline
add_rect(s, Inches(8.2), 0, Emu(6350), SH, HAIRLINE)

add_text(s, Inches(0.55), Inches(0.55), Inches(3), Inches(0.4),
         "● cursor", size=12, color=TEXT, bold=True, letter_spacing=20)

add_text(s, Inches(0.55), Inches(2.4), Inches(8), Inches(0.5),
         "DISCOVERY · 20 MIN", size=11, color=TEXT_MUTED, letter_spacing=400)

add_text(s, Inches(0.55), Inches(2.85), Inches(8.5), Inches(2.5),
         "Cursor × Figma\nCTO & CISO.",
         size=54, bold=True, color=TEXT, line_spacing=1.02)

add_text(s, Inches(0.55), Inches(5.1), Inches(7.5), Inches(1),
         "Plan de l'appel, questions de découverte,\nthèse Why Now / Why Change / Why Cursor.",
         size=16, color=TEXT_DIM, line_spacing=1.4)

# right panel: meta block
add_text(s, Inches(8.6), Inches(2.4), Inches(4), Inches(0.4),
         "OBJECTIFS", size=10, color=TEXT_MUTED, letter_spacing=300)
add_text(s, Inches(8.6), Inches(2.8), Inches(4.5), Inches(3),
         "→  Earn a technical deep dive\n→  Earn a security review\n→  Ne pas pitcher — qualifier",
         size=14, color=TEXT, line_spacing=1.7)

add_text(s, Inches(8.6), Inches(5.4), Inches(4), Inches(0.4),
         "DATE", size=10, color=TEXT_MUTED, letter_spacing=300)
add_text(s, Inches(8.6), Inches(5.75), Inches(4), Inches(0.4),
         "—", size=14, color=TEXT)

add_text(s, Inches(0.55), Inches(7.05), Inches(8), Inches(0.3),
         "Confidential — Internal prep document",
         size=9, color=TEXT_MUTED, letter_spacing=80)
add_text(s, Inches(11.5), Inches(7.05), Inches(1.3), Inches(0.3),
         "01 / " + f"{TOTAL:02d}", size=9, color=TEXT_MUTED,
         align=PP_ALIGN.RIGHT, font=FONT_MONO)


# --- 02 — Agenda --------------------------------------------------------------
s = add_slide(); page_chrome(s, 2, TOTAL, "Agenda")
section_title(s, "Structure de l'appel",
              "20 minutes, timeboxé.",
              "Discipline > improvisation. Le client doit parler 60 % du temps.")

rows = [
    ("0:00 – 1:30",  "Cadrage",                "Agenda, permission, posture humble."),
    ("1:30 – 9:30",  "Discovery",              "CTO d'abord, CISO à partir de 5:00."),
    ("9:30 – 14:00", "Thèse + 1 proof point",  "Why Now / Why Change / Why Cursor."),
    ("14:00 – 17:00","Objection CISO",         "Je la pose moi-même, avant qu'elle ne tombe."),
    ("17:00 – 20:00","Next steps",             "Deux tracks parallèles — tech & sécurité."),
]

y = Inches(3.7)
for tm, title, desc in rows:
    add_text(s, Inches(0.55), y, Inches(2.1), Inches(0.4),
             tm, size=12, color=TEXT_MUTED, font=FONT_MONO)
    add_text(s, Inches(2.9), y, Inches(3.2), Inches(0.4),
             title, size=15, bold=True, color=TEXT)
    add_text(s, Inches(6.3), y, Inches(6.5), Inches(0.4),
             desc, size=13, color=TEXT_DIM)
    add_hairline(s, Inches(0.55), y + Inches(0.55), Inches(12.25))
    y += Inches(0.62)


# --- 03 — Contexte Figma ------------------------------------------------------
s = add_slide(); page_chrome(s, 3, TOTAL, "Pre-call · Contexte")
section_title(s, "Ce qu'il faut savoir avant d'entrer",
              "Figma, en une slide.",
              "On ne perd pas une seule seconde à se présenter Figma — on le démontre.")

cols = [
    ("STACK",
     "Éditeur C++/WASM\nInfra Rust + TypeScript\nMonorepo, perf-critical\n→ contexte long, refactos, multi-repo."),
    ("PRODUIT IA",
     "Figma AI, Make,\nfeatures génératives en prod.\n→ ils pensent évals, latence, trust\ndéjà en interne."),
    ("ÉCHELLE",
     "~1 500+ employés\n~500–650 ingénieurs estimés\n→ base ROI à valider en live\nsur l'appel."),
    ("MOMENTUM",
     "Post-Adobe, route IPO,\nhardening pré-public.\n→ « why now » sécurité\nest naturellement chaud."),
]
xw = Inches(2.95); gap = Inches(0.15)
x = Inches(0.55)
for label, body in cols:
    add_rect(s, x, Inches(3.8), xw, Inches(3.0), BG_PANEL)
    add_rect(s, x, Inches(3.8), xw, Emu(6350), HAIRLINE)
    add_text(s, x + Inches(0.25), Inches(3.95), xw - Inches(0.5), Inches(0.4),
             label, size=10, color=TEXT_MUTED, letter_spacing=300)
    add_text(s, x + Inches(0.25), Inches(4.35), xw - Inches(0.5), Inches(2.5),
             body, size=12, color=TEXT, line_spacing=1.45)
    x += xw + gap


# --- 04 — Personas ------------------------------------------------------------
s = add_slide(); page_chrome(s, 4, TOTAL, "Personas")
section_title(s, "Deux acheteurs, deux grilles de lecture",
              "CTO ≠ CISO.",
              "Ils n'évaluent pas le même produit. Adapter à la phrase près.")

# 2 colonnes
def persona(x, label, title, rows):
    add_rect(s, x, Inches(3.5), Inches(6.1), Inches(3.55), BG_PANEL)
    add_rect(s, x, Inches(3.5), Inches(6.1), Emu(6350), HAIRLINE)
    add_text(s, x + Inches(0.3), Inches(3.65), Inches(5.5), Inches(0.4),
             label, size=10, color=TEXT_MUTED, letter_spacing=300)
    add_text(s, x + Inches(0.3), Inches(4.0), Inches(5.5), Inches(0.5),
             title, size=20, bold=True, color=TEXT)
    yy = Inches(4.65)
    for k, v in rows:
        add_text(s, x + Inches(0.3), yy, Inches(1.8), Inches(0.35),
                 k.upper(), size=9, color=TEXT_MUTED, letter_spacing=200)
        add_text(s, x + Inches(2.05), yy, Inches(3.9), Inches(0.4),
                 v, size=12, color=TEXT, line_spacing=1.35)
        yy += Inches(0.55)

persona(Inches(0.55), "PERSONA 1", "CTO", [
    ("Ce qui le hante", "Vélocité, gap IA vs concurrence, attrition seniors"),
    ("KPI",             "Cycle time, PRs/eng, % code AI-assisté"),
    ("Sa peur",         "« Encore un outil, +10 % sur Copilot »"),
    ("À prouver",       "Step-function, pas incrément"),
])
persona(Inches(6.75), "PERSONA 2", "CISO", [
    ("Ce qui le hante", "Exfiltration code, secrets, prompt injection, audit"),
    ("KPI",             "# shadow tools, time-to-approve, 0 incident IP"),
    ("Sa peur",         "« Encore un vendor avec mon code »"),
    ("À prouver",       "Cursor sanctionné > shadow IT actuelle"),
])


# --- 05 — Opener -------------------------------------------------------------
s = add_slide(); page_chrome(s, 5, TOTAL, "Opener · 1 min 30")
section_title(s, "Les 90 premières secondes",
              "Script d'ouverture.",
              "À mémoriser presque mot pour mot — c'est là que la salle se détend ou se ferme.")

add_rect(s, Inches(0.55), Inches(3.7), Inches(12.25), Inches(3.0), BG_PANEL)
add_rect(s, Inches(0.55), Inches(3.7), Inches(12.25), Emu(6350), HAIRLINE)
add_text(s, Inches(0.9), Inches(3.95), Inches(0.5), Inches(0.4),
         "“", size=44, color=TEXT_MUTED, font="Georgia")
add_text(s, Inches(1.35), Inches(4.05), Inches(11.1), Inches(2.6),
         "Merci pour ces 20 minutes — je sais que c'est cher. Je vais passer le plus "
         "clair du temps à poser des questions, parce que je préfère vous être utile "
         "qu'impressionnant. Deux objectifs côté Cursor : comprendre où l'IA dans le SDLC "
         "vous aide ou vous gêne aujourd'hui, et voir si un pilote ciblé vaut le temps "
         "de vos équipes. Quick check sur l'agenda : ~8 min de questions, ~5 sur ce qu'on "
         "voit chez vos pairs, ~5 sur la sécurité, ~2 sur les next steps. Ça vous va ?",
         size=15, color=TEXT, line_spacing=1.55)

add_text(s, Inches(0.55), Inches(6.85), Inches(12), Inches(0.3),
         "EFFETS — respect du temps · baisse de garde · pré-engagement sur l'agenda · "
         "bloc sécurité réservé pour garder le CISO",
         size=10, color=TEXT_MUTED, letter_spacing=80)


# --- 06 — Discovery CTO -------------------------------------------------------
s = add_slide(); page_chrome(s, 6, TOTAL, "Discovery · CTO")
section_title(s, "8 minutes de questions · CTO en premier",
              "4 questions, pas 12.",
              "Après chaque question : compter jusqu'à 3 avant de combler le silence.")

qs = [
    ("01", "État des lieux",
     "« Quel est votre standard IA dans l'IDE aujourd'hui, et comment noteriez-vous adoption + impact, honnêtement ? »",
     "→ Copilot déployé large mais plateau ; sentiment mitigé."),
    ("02", "Plafond à 12 mois",
     "« Le gap entre le meilleur outil IA dev et le médian — il s'élargit ou se compresse sur 12 mois ? »",
     "→ S'élargit = on a gagné l'argument Why Change."),
    ("03", "Où ça fait mal",
     "« Quelle étape du SDLC l'IA devrait aider mais n'aide pas — review, refactos, onboarding, tests, incidents ? »",
     "→ Refactos / large-context = sweet spot Cursor."),
    ("04", "Signal org",
     "« Les seniors et juniors utilisent-ils l'IA pareil ? Y a-t-il un tier qui a discrètement abandonné ? »",
     "→ Senior IC opt-out = signal très fort, pitch atterrit dur."),
]
y = Inches(3.7)
for n, k, q, hint in qs:
    add_text(s, Inches(0.55), y, Inches(0.7), Inches(0.4),
             n, size=14, color=TEXT_MUTED, font=FONT_MONO)
    add_text(s, Inches(1.2), y, Inches(3), Inches(0.4),
             k, size=13, bold=True, color=TEXT)
    add_text(s, Inches(4.2), y, Inches(8.6), Inches(0.45),
             q, size=12, color=ACCENT_SOFT, line_spacing=1.35)
    add_text(s, Inches(4.2), y + Inches(0.45), Inches(8.6), Inches(0.35),
             hint, size=11, color=TEXT_MUTED, line_spacing=1.3)
    add_hairline(s, Inches(0.55), y + Inches(0.85), Inches(12.25))
    y += Inches(0.85)


# --- 07 — Discovery CISO ------------------------------------------------------
s = add_slide(); page_chrome(s, 7, TOTAL, "Discovery · CISO")
section_title(s, "Embarquer le CISO à partir de la minute 5",
              "3 questions sécurité.",
              "Ne pas attendre qu'il s'invite — l'appeler par son nom et lui passer la main.")

qs = [
    ("05", "Posture actuelle",
     "« Quelle est votre politique sur les outils IA de code — sanctionnés, shadow, entre les deux ? Quel a été le facteur décisif sur les sanctionnés ? »",
     "→ IP-in-training ? Résidence ? Audit ? On saura quoi mettre en avant."),
    ("06", "Shadow IT",
     "« Si on faisait un sondage anonyme cet aprèm — quel % de vos ingés colle du code dans ChatGPT / Claude / Gemini chaque semaine ? »",
     "→ La réponse honnête est 40–70 %. C'est notre meilleur levier Why Change."),
    ("07", "Pré-IPO / audit",
     "« En durcissant pour la prochaine étape de la boîte — quels 2–3 items IA sont déjà sur le radar des auditeurs ? »",
     "→ Pre-position nos contrôles enterprise sur leurs items réels."),
]
y = Inches(3.7)
for n, k, q, hint in qs:
    add_text(s, Inches(0.55), y, Inches(0.7), Inches(0.4),
             n, size=14, color=TEXT_MUTED, font=FONT_MONO)
    add_text(s, Inches(1.2), y, Inches(3), Inches(0.4),
             k, size=13, bold=True, color=TEXT)
    add_text(s, Inches(4.2), y, Inches(8.6), Inches(0.6),
             q, size=12, color=ACCENT_SOFT, line_spacing=1.35)
    add_text(s, Inches(4.2), y + Inches(0.6), Inches(8.6), Inches(0.35),
             hint, size=11, color=TEXT_MUTED, line_spacing=1.3)
    add_hairline(s, Inches(0.55), y + Inches(1.0), Inches(12.25))
    y += Inches(1.0)


# --- 08 — Why now ------------------------------------------------------------
s = add_slide(); page_chrome(s, 8, TOTAL, "Thèse · Why now")
section_title(s, "Pourquoi maintenant",
              "La courbe modèle a basculé.",
              "Choisir 1–2 leviers, pas les 4. Toujours raccrocher à ce qu'ils viennent de dire.")

cards = [
    ("01 · Modèles",
     "Les frontières des 12 derniers mois sont passées de l'autocomplete sophistiqué "
     "à la tenue d'une tâche multi-fichiers en mémoire de travail. La base des 2–3 "
     "prochaines années de productivité se joue maintenant."),
    ("02 · Agentic SDLC",
     "Background agents, exécution longue, review au niveau PR : en prod cette "
     "année chez des centaines de larges eng orgs. Choisir sa plateforme après "
     "T4 = 12 mois de retard outils, patterns internes et sécurité."),
    ("03 · Pré-IPO Figma",
     "À mesure que Figma durcit ses contrôles, le coût des outils IA non-sanctionnés "
     "monte chaque trimestre. Ne rien faire est en soi une décision sécurité."),
    ("04 · Talent",
     "Les seniors posent la question des outils IA en entretien. Levier hiring "
     "et levier attrition simultanés."),
]

xs = [Inches(0.55), Inches(6.95)]
ys = [Inches(3.7), Inches(5.45)]
for i, (k, body) in enumerate(cards):
    x = xs[i % 2]; y = ys[i // 2]
    add_rect(s, x, y, Inches(6.25), Inches(1.55), BG_PANEL)
    add_rect(s, x, y, Inches(6.25), Emu(6350), HAIRLINE)
    add_text(s, x + Inches(0.3), y + Inches(0.15), Inches(5), Inches(0.35),
             k, size=11, color=TEXT_MUTED, letter_spacing=200, bold=True)
    add_text(s, x + Inches(0.3), y + Inches(0.5), Inches(5.8), Inches(1.1),
             body, size=11.5, color=TEXT, line_spacing=1.4)


# --- 09 — Why change ---------------------------------------------------------
s = add_slide(); page_chrome(s, 9, TOTAL, "Thèse · Why change")
section_title(s, "Pourquoi changer (du sortant — quasi sûrement Copilot)",
              "Un gap qualité, pas une bataille de marque.",
              "On ne descend pas Copilot. On nomme ce qui mange les journées des seniors.")

bullets = [
    ("Le travail qui coûte cher",
     "Refactos multi-fichiers, navigation d'un service inconnu, repro de bug, "
     "tests manquants. C'est là que le gap est le plus large — et il s'est "
     "élargi sur 9 mois, pas refermé."),
    ("Senior IC opt-out",
     "Pattern récurrent : quand vos meilleurs ingés n'utilisent pas l'outil, "
     "le plafond ROI org est ~5 %. Quand ils l'utilisent, c'est 20–30 %."),
    ("Coût du sur-place",
     "Chaque mois passé sur un outil plafonné = patterns internes qui se figent "
     "autour de ses limites. Le switch devient plus cher, pas moins cher."),
]

y = Inches(3.7)
for k, v in bullets:
    add_text(s, Inches(0.55), y, Inches(0.4), Inches(0.4),
             "→", size=18, color=TEXT_MUTED)
    add_text(s, Inches(1.05), y, Inches(4.0), Inches(0.4),
             k, size=15, bold=True, color=TEXT)
    add_text(s, Inches(5.2), y, Inches(7.6), Inches(1.0),
             v, size=12.5, color=TEXT_DIM, line_spacing=1.45)
    add_hairline(s, Inches(0.55), y + Inches(1.1), Inches(12.25))
    y += Inches(1.2)


# --- 10 — Why Cursor ---------------------------------------------------------
s = add_slide(); page_chrome(s, 10, TOTAL, "Thèse · Why Cursor")
section_title(s, "Trois claims tranchants",
              "Why Cursor.",
              "Pas de feature dump. Trois affirmations, défendables sous le feu.")

claims = [
    ("01", "Capacité",
     "Cursor est conçu pour le travail full-repo et agentique — exactement\n"
     "là où se joue la prochaine année de gains de productivité."),
    ("02", "Choix + futur-proof",
     "Les modèles frontières s'échangent à mesure qu'ils sortent.\n"
     "Pas de lock-in sur la roadmap d'un seul provider."),
    ("03", "Trust enterprise",
     "SOC 2 Type II, ISO 27001, Privacy Mode (zero data retention),\n"
     "no training on your code, SAML/SCIM, audit logs."),
]
y = Inches(3.7)
for n, k, body in claims:
    add_rect(s, Inches(0.55), y, Inches(12.25), Inches(1.05), BG_PANEL)
    add_rect(s, Inches(0.55), y, Inches(12.25), Emu(6350), HAIRLINE)
    add_text(s, Inches(0.85), y + Inches(0.2), Inches(0.6), Inches(0.6),
             n, size=22, color=TEXT_MUTED, font=FONT_MONO)
    add_text(s, Inches(1.85), y + Inches(0.2), Inches(2.5), Inches(0.5),
             k, size=16, bold=True, color=TEXT)
    add_text(s, Inches(4.6), y + Inches(0.2), Inches(8.2), Inches(0.8),
             body, size=12, color=TEXT_DIM, line_spacing=1.4)
    y += Inches(1.15)


# --- 11 — Pain numbers · productivité ----------------------------------------
s = add_slide(); page_chrome(s, 11, TOTAL, "Pain numbers · Productivité")
section_title(s, "Repères à mémoriser",
              "Les chiffres qui débloquent le CTO.",
              "Toujours formuler : « ce qu'on voit chez des clients de votre taille »,\njamais comme une vérité universelle.")

stats = [
    ("30–40 %", "du temps des seniors passé à\nlire / naviguer du code\nqu'ils n'ont pas écrit."),
    ("15–25 %", "réduction cycle-time chez les\norgs IA-adoptantes — au-dessus\nde 60 % d'usage hebdo seniors."),
    ("10–15 %", "du temps eng = PR review,\nplus gros sink après coding.\nCompressible nettement."),
    ("≤ 35 %",  "des suggestions multi-lignes\nacceptées chez les outils\ncomplétion-only. Inversé en agentique."),
]
x = Inches(0.55)
for big, body in stats:
    add_rect(s, x, Inches(4.1), Inches(2.95), Inches(2.6), BG_PANEL)
    add_rect(s, x, Inches(4.1), Inches(2.95), Emu(6350), HAIRLINE)
    add_text(s, x + Inches(0.3), Inches(4.3), Inches(2.6), Inches(0.9),
             big, size=34, bold=True, color=TEXT, letter_spacing=-20)
    add_text(s, x + Inches(0.3), Inches(5.25), Inches(2.6), Inches(1.4),
             body, size=11.5, color=TEXT_DIM, line_spacing=1.4)
    x += Inches(3.1)


# --- 12 — ROI math (live) -----------------------------------------------------
s = add_slide(); page_chrome(s, 12, TOTAL, "ROI · à faire en live")
section_title(s, "Le calcul à projeter à l'écran",
              "ROI : capter 5 % ou 50 % de l'upside ?",
              "Demander à Figma de corriger N. La correction = engagement.")

# left: formula
add_rect(s, Inches(0.55), Inches(3.7), Inches(7.0), Inches(3.2), BG_PANEL)
add_rect(s, Inches(0.55), Inches(3.7), Inches(7.0), Emu(6350), HAIRLINE)
add_text(s, Inches(0.85), Inches(3.85), Inches(6), Inches(0.4),
         "MODÈLE", size=10, color=TEXT_MUTED, letter_spacing=300)
add_text(s, Inches(0.85), Inches(4.25), Inches(6.4), Inches(2.5),
         "N  =  ingénieurs   (≈ 500, à confirmer en live)\n"
         "C  =  coût chargé   ≈ $275 K / an (SF Bay)\n"
         "T  =  temps récupéré   8–12 % conservateur,\n"
         "        20 %+ avec adoption forte\n\n"
         "Capacité réclamée  =  N × C × T",
         size=13, color=TEXT, font=FONT_MONO, line_spacing=1.55)

# right: numbers
add_rect(s, Inches(7.85), Inches(3.7), Inches(4.95), Inches(3.2), BG_PANEL)
add_rect(s, Inches(7.85), Inches(3.7), Inches(4.95), Emu(6350), HAIRLINE)
add_text(s, Inches(8.15), Inches(3.85), Inches(4), Inches(0.4),
         "EXEMPLE FIGMA", size=10, color=TEXT_MUTED, letter_spacing=300)
add_text(s, Inches(8.15), Inches(4.25), Inches(4.5), Inches(0.9),
         "≈ $13,7 M / an",
         size=30, bold=True, color=TEXT, letter_spacing=-10)
add_text(s, Inches(8.15), Inches(5.15), Inches(4.5), Inches(1.5),
         "500 ingés × $275 K × 10 %\n\n"
         "Coût outil enterprise typique :\n< 3 % de la capacité récupérée.",
         size=12, color=TEXT_DIM, line_spacing=1.45)

add_text(s, Inches(0.55), Inches(7.05 - 0.2), Inches(12), Inches(0.3),
         "PHRASE À DIRE  —  « La question n'est pas si l'outil se paye. C'est si vous "
         "captez 5 % ou 50 % de l'upside — fonction du choix de plateforme et du rollout. »",
         size=10.5, color=ACCENT_SOFT, letter_spacing=20)


# --- 13 — Pain numbers · sécurité --------------------------------------------
s = add_slide(); page_chrome(s, 13, TOTAL, "Pain numbers · Sécurité")
section_title(s, "Repères à mémoriser",
              "Les chiffres qui réveillent le CISO.",
              "Reframe : ce n'est pas « pourquoi ajouter un outil » → c'est « pourquoi tolérer l'incontrôlé ».")

stats = [
    ("50–75 %", "des ingénieurs utilisent un outil\nIA de code chaque semaine."),
    ("30–60 %", "admettent coller du code dans\ndes produits IA grand public."),
    ("5–7",     "outils IA non-sanctionnés présents\nau moment où l'un est enfin approuvé."),
    ("6–9 mois","du « il faut évaluer » à « en prod\navec SSO + audit ». 6–9 mois\nd'exposition non-gérée."),
]
x = Inches(0.55)
for big, body in stats:
    add_rect(s, x, Inches(4.1), Inches(2.95), Inches(2.6), BG_PANEL)
    add_rect(s, x, Inches(4.1), Inches(2.95), Emu(6350), HAIRLINE)
    add_text(s, x + Inches(0.3), Inches(4.3), Inches(2.6), Inches(0.9),
             big, size=30, bold=True, color=TEXT, letter_spacing=-20)
    add_text(s, x + Inches(0.3), Inches(5.25), Inches(2.6), Inches(1.4),
             body, size=11.5, color=TEXT_DIM, line_spacing=1.4)
    x += Inches(3.1)


# --- 14 — Objection CISO -----------------------------------------------------
s = add_slide(); page_chrome(s, 14, TOTAL, "Objection · CISO")
section_title(s, "Minute 14 — je la pose moi-même",
              "« Encore un vendor avec notre code. »",
              "Trois réponses préparées. Aucune n'est une feature, toutes sont contractuelles.")

items = [
    ("01", "Zero training",
     "Votre code n'entraîne aucun modèle — ni le nôtre, ni celui des providers. "
     "C'est contractuel, pas un toggle."),
    ("02", "Privacy Mode + ZDR",
     "Prompts et completions peuvent ne pas persister sur notre infrastructure. "
     "On déroule à votre équipe ce qui est loggé et ce qui ne l'est pas."),
    ("03", "Contrôles enterprise",
     "SOC 2 Type II · ISO 27001 · SAML SSO · SCIM · export audit logs · "
     "policies par équipe. Call security ↔ security sous 7 jours, "
     "SIG + résumé pentest envoyés en amont."),
]
y = Inches(3.7)
for n, k, body in items:
    add_text(s, Inches(0.55), y, Inches(0.7), Inches(0.5),
             n, size=18, color=TEXT_MUTED, font=FONT_MONO)
    add_text(s, Inches(1.5), y, Inches(3.5), Inches(0.5),
             k, size=15, bold=True, color=TEXT)
    add_text(s, Inches(5.2), y, Inches(7.6), Inches(1.0),
             body, size=12.5, color=TEXT_DIM, line_spacing=1.45)
    add_hairline(s, Inches(0.55), y + Inches(1.05), Inches(12.25))
    y += Inches(1.15)


# --- 15 — Close · two tracks --------------------------------------------------
s = add_slide(); page_chrome(s, 15, TOTAL, "Close · Next steps")
section_title(s, "17:00 — la sortie",
              "Deux tracks parallèles, jamais « un pilote ».",
              "Aucun des deux personas n'est le bottleneck de l'autre.")

# two columns
def track(x, label, title, body, target):
    add_rect(s, x, Inches(3.6), Inches(6.1), Inches(3.4), BG_PANEL)
    add_rect(s, x, Inches(3.6), Inches(6.1), Emu(6350), HAIRLINE)
    add_text(s, x + Inches(0.3), Inches(3.75), Inches(5.5), Inches(0.4),
             label, size=10, color=TEXT_MUTED, letter_spacing=300)
    add_text(s, x + Inches(0.3), Inches(4.1), Inches(5.5), Inches(0.5),
             title, size=20, bold=True, color=TEXT)
    add_text(s, x + Inches(0.3), Inches(4.8), Inches(5.5), Inches(1.7),
             body, size=12.5, color=TEXT_DIM, line_spacing=1.5)
    add_text(s, x + Inches(0.3), Inches(6.4), Inches(5.5), Inches(0.4),
             "OWNER CÔTÉ FIGMA", size=9, color=TEXT_MUTED, letter_spacing=200)
    add_text(s, x + Inches(0.3), Inches(6.65), Inches(5.5), Inches(0.3),
             target, size=12, color=TEXT)

track(Inches(0.55), "TRACK 1", "Technique",
      "30 min avec l'owner dev tooling.\n"
      "Pilote ciblé sur LA zone qu'ils ont nommée\n"
      "(refactos / review / onboarding…).\n"
      "Métriques de succès définies AVANT le pilote.",
      "Head of Platform / DevEx")
track(Inches(6.75), "TRACK 2", "Sécurité",
      "45 min security ↔ security.\n"
      "On envoie SOC 2, SIG, pentest, archi, DPA.\n"
      "Quand le pilote tech finit,\n"
      "la sécurité n'est pas à zéro.",
      "CISO + lead AppSec")

add_text(s, Inches(0.55), Inches(7.05 - 0.2), Inches(12), Inches(0.3),
         "PHRASE À DIRE  —  « Vous pouvez me mettre en contact avec la bonne personne "
         "sur chaque track cette semaine ? »  Puis se taire.",
         size=10.5, color=ACCENT_SOFT, letter_spacing=20)


# --- 16 — Rappels tactiques ---------------------------------------------------
s = add_slide(); page_chrome(s, 16, TOTAL, "Rappels tactiques")
section_title(s, "À garder en tête",
              "Le détail qui fait gagner.",
              "Petites choses, gros impact sur l'issue de l'appel.")

tips = [
    ("Pré-envoyer  ·  rien de lourd",
     "Email de 2 lignes max — agenda. On garde les artefacts pour le screen-share."),
    ("Citer 2–3 pairs",
     "Mêmes taille + stack, en clients enterprise Cursor. UN qui a résolu pile l'objection sécurité du CISO."),
    ("Regarder l'horloge visiblement",
     "À 17:00 — « je veux respecter votre temps, passons aux next steps. » Discipline = crédibilité."),
    ("Followup < 2 h",
     "Pas 24. Un paragraphe par persona. On reprend ce qu'ILS ont dit, pas ce qu'on a dit."),
    ("Senior IC opt-out",
     "Si ça sort en discovery — épingler l'info, c'est le wedge le plus puissant pour le pilote."),
    ("Silence > comblement",
     "Compter 3 secondes après chaque question. Le premier qui parle perd."),
]
y = Inches(3.7); x_cols = [Inches(0.55), Inches(6.95)]
for i, (k, v) in enumerate(tips):
    x = x_cols[i % 2]
    yy = y + (i // 2) * Inches(1.05)
    add_text(s, x, yy, Inches(0.3), Inches(0.4), "→", size=16, color=TEXT_MUTED)
    add_text(s, x + Inches(0.35), yy, Inches(5.7), Inches(0.4),
             k, size=13, bold=True, color=TEXT)
    add_text(s, x + Inches(0.35), yy + Inches(0.4), Inches(5.7), Inches(0.6),
             v, size=11.5, color=TEXT_DIM, line_spacing=1.4)


# --- Save ---------------------------------------------------------------------
out = "/workspace/decks/Cursor_x_Figma_Discovery_20min.pptx"
prs.save(out)
print(f"OK  →  {out}")
