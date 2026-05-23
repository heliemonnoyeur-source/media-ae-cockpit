"""
Cursor x Figma — Discovery CTO/CISO (20 min)
Génère un deck .pptx au look & feel Cursor (dark, minimal, moderne).

V2 — affiné après lecture du « 2026 Cursor GTM Discovery / Deal Review
Interview Prep ». Ce qui change :

- Positionnement officiel Cursor utilisé tel quel
  (« workflow, context, execution » + « ~70% Fortune 1000 »).
- Why Change refait : Copilot ET Claude Code (2026 = Claude Code = compétiteur #1).
- Why Cursor refait sur les 4 différenciateurs officiels :
  Model neutrality · Large codebase performance · Time to value · Platform.
- Privacy Mode décrit avec les 3 bullets exacts du doc.
- Pain numbers softés (rubrique « no overconfident claims »).
- Discovery CTO Q3 reformulée pour pressure-test l'urgence.
- Rappels tactiques recadrés sur la grille d'évaluation Cursor.
- Slide 17 ajoutée : meta-rubrique candidate-only.

Le template officiel Cursor n'est pas dans le repo : on recrée la charte
(fond #0A0A0A, texte blanc, accents discrets, sans-serif, grille 16:9).
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


def page_chrome(slide, page_num, total, section_label):
    add_text(slide, Inches(0.55), Inches(0.35), Inches(3), Inches(0.4),
             "● cursor", size=11, color=TEXT, bold=True, letter_spacing=20)
    add_text(slide, Inches(9.5), Inches(0.35), Inches(3.3), Inches(0.4),
             section_label.upper(), size=9, color=TEXT_MUTED,
             align=PP_ALIGN.RIGHT, letter_spacing=200)
    add_text(slide, Inches(0.55), Inches(7.05), Inches(6), Inches(0.3),
             "Cursor × Figma  ·  Discovery CTO / CISO  ·  20 min",
             size=9, color=TEXT_MUTED, letter_spacing=80)
    add_text(slide, Inches(11.5), Inches(7.05), Inches(1.3), Inches(0.3),
             f"{page_num:02d} / {total:02d}",
             size=9, color=TEXT_MUTED, align=PP_ALIGN.RIGHT,
             font=FONT_MONO, letter_spacing=50)
    add_hairline(slide, Inches(0.55), Inches(0.85), Inches(12.25))


def section_title(slide, kicker, title, subtitle=None):
    add_text(slide, Inches(0.55), Inches(1.25), Inches(8), Inches(0.4),
             kicker.upper(), size=10, color=TEXT_MUTED, letter_spacing=300)
    add_text(slide, Inches(0.55), Inches(1.65), Inches(12), Inches(1.2),
             title, size=36, bold=True, color=TEXT, line_spacing=1.05)
    if subtitle:
        add_text(slide, Inches(0.55), Inches(2.85), Inches(12), Inches(0.7),
                 subtitle, size=15, color=TEXT_DIM, line_spacing=1.3)


# ---------------------------------------------------------------------------
# Slides
# ---------------------------------------------------------------------------

TOTAL = 17

# --- 01 — Cover ---------------------------------------------------------------
s = add_slide()
add_rect(s, Inches(8.2), 0, Inches(5.13), SH, BG_PANEL)
add_rect(s, Inches(8.2), 0, Emu(6350), SH, HAIRLINE)

add_text(s, Inches(0.55), Inches(0.55), Inches(3), Inches(0.4),
         "● cursor", size=12, color=TEXT, bold=True, letter_spacing=20)

add_text(s, Inches(0.55), Inches(2.4), Inches(8), Inches(0.5),
         "DISCOVERY · 20 MIN", size=11, color=TEXT_MUTED, letter_spacing=400)

add_text(s, Inches(0.55), Inches(2.85), Inches(8.5), Inches(2.5),
         "Cursor × Figma\nCTO & CISO.",
         size=54, bold=True, color=TEXT, line_spacing=1.02)

add_text(s, Inches(0.55), Inches(5.1), Inches(7.5), Inches(1.3),
         "Cursor wins on workflow, context, and execution.\n"
         "~70 % des Fortune 1000 l'utilisent déjà.",
         size=15, color=TEXT_DIM, line_spacing=1.4, italic=True)

add_text(s, Inches(8.6), Inches(2.4), Inches(4), Inches(0.4),
         "OBJECTIFS", size=10, color=TEXT_MUTED, letter_spacing=300)
add_text(s, Inches(8.6), Inches(2.8), Inches(4.5), Inches(3),
         "→  Lead with discovery, not pitch\n→  Earn a technical deep dive\n→  Earn a security review",
         size=14, color=TEXT, line_spacing=1.7)

add_text(s, Inches(8.6), Inches(5.4), Inches(4), Inches(0.4),
         "POSTURE", size=10, color=TEXT_MUTED, letter_spacing=300)
add_text(s, Inches(8.6), Inches(5.75), Inches(4.5), Inches(0.9),
         "Opinionated, not scripted.\nGround claims, no AI hype.",
         size=13, color=TEXT, line_spacing=1.4)

add_text(s, Inches(0.55), Inches(7.05), Inches(8), Inches(0.3),
         "Confidential — Internal prep document",
         size=9, color=TEXT_MUTED, letter_spacing=80)
add_text(s, Inches(11.5), Inches(7.05), Inches(1.3), Inches(0.3),
         f"01 / {TOTAL:02d}", size=9, color=TEXT_MUTED,
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
    ("03", "Pressure-test urgence",
     "« Pourquoi vous regardez ça maintenant plutôt qu'au prochain renouvellement Copilot ? Qu'est-ce qui a changé ce trimestre ? »",
     "→ Pas de réponse claire = l'urgence est faible, on calibre les next steps."),
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


# --- 09 — Why change · paysage compétitif ------------------------------------
s = add_slide(); page_chrome(s, 9, TOTAL, "Thèse · Why change")
section_title(s, "Le paysage 2026",
              "Copilot et Claude Code, deux conversations différentes.",
              "On ne descend personne. On nomme ce que Cursor applique mieux.")

# Two competitor framings side by side
def competitor(x, label, title, lines):
    add_rect(s, x, Inches(3.6), Inches(6.1), Inches(3.5), BG_PANEL)
    add_rect(s, x, Inches(3.6), Inches(6.1), Emu(6350), HAIRLINE)
    add_text(s, x + Inches(0.3), Inches(3.75), Inches(5.5), Inches(0.4),
             label, size=10, color=TEXT_MUTED, letter_spacing=300)
    add_text(s, x + Inches(0.3), Inches(4.1), Inches(5.5), Inches(0.5),
             title, size=18, bold=True, color=TEXT)
    yy = Inches(4.75)
    for left, right in lines:
        add_text(s, x + Inches(0.3), yy, Inches(2.4), Inches(0.4),
                 left, size=11, color=TEXT_DIM)
        add_text(s, x + Inches(2.65), yy, Inches(0.3), Inches(0.4),
                 "→", size=11, color=TEXT_MUTED)
        add_text(s, x + Inches(3.0), yy, Inches(2.9), Inches(0.4),
                 right, size=11, color=TEXT, bold=True)
        yy += Inches(0.42)

competitor(Inches(0.55), "VS GITHUB COPILOT", "Du snippet à la tâche", [
    ("Snippet help",          "Task completion"),
    ("Local suggestions",     "Codebase context"),
    ("Isolated assistance",   "Workflow support"),
    ("Point solution",        "Integrated platform"),
])

competitor(Inches(6.75), "VS CLAUDE CODE", "Le compétiteur #1 en 2026", [
    ("Single-provider",       "Model neutrality"),
    ("Raw model wrapper",     "Workflow integration"),
    ("Limited repo context",  "Large codebase performance"),
    ("DIY setup",             "Faster time to value"),
])

add_text(s, Inches(0.55), Inches(7.18 - 0.13), Inches(12), Inches(0.3),
         "L'edge n'est pas une intelligence exclusive — c'est l'intelligence appliquée plus "
         "efficacement aux workflows d'ingénierie réels.",
         size=10.5, color=ACCENT_SOFT, letter_spacing=20, italic=True)


# --- 10 — Why Cursor · 4 différenciateurs officiels --------------------------
s = add_slide(); page_chrome(s, 10, TOTAL, "Thèse · Why Cursor")
section_title(s, "Les 4 différenciateurs",
              "Why Cursor.",
              "Workflow · Context · Execution. Tout part de là.")

claims = [
    ("01", "Model neutrality",
     "Flexibilité, pas de lock-in. Le meilleur modèle change tout le temps — "
     "Cursor donne accès au SOTA sans forcer à quitter une plateforme."),
    ("02", "Large codebase performance",
     "Pas juste un wrapper de modèle. Semantic search, indexing, "
     "retrieval — d'autant plus déterminant que le repo est gros et messy."),
    ("03", "Faster time to value",
     "Marche out of the box. Les équipes standardisent vite ; les power users "
     "vont profond, mais le baseline est déjà fort."),
    ("04", "Platform, not just a tool",
     "Couvre tout le SDLC — plan, write, review, debug, iterate. L'intelligence "
     "est appliquée là où les devs travaillent vraiment."),
]
y = Inches(3.65)
for n, k, body in claims:
    add_rect(s, Inches(0.55), y, Inches(12.25), Inches(0.78), BG_PANEL)
    add_rect(s, Inches(0.55), y, Inches(12.25), Emu(6350), HAIRLINE)
    add_text(s, Inches(0.85), y + Inches(0.15), Inches(0.6), Inches(0.5),
             n, size=18, color=TEXT_MUTED, font=FONT_MONO)
    add_text(s, Inches(1.75), y + Inches(0.15), Inches(3.5), Inches(0.5),
             k, size=15, bold=True, color=TEXT)
    add_text(s, Inches(5.45), y + Inches(0.18), Inches(7.3), Inches(0.55),
             body, size=11.5, color=TEXT_DIM, line_spacing=1.35)
    y += Inches(0.85)


# --- 11 — Pain numbers · productivité ----------------------------------------
s = add_slide(); page_chrome(s, 11, TOTAL, "Pain numbers · Productivité")
section_title(s, "Repères à manier avec précaution",
              "Les chiffres qui débloquent le CTO.",
              "Toujours : « ce qu'on voit chez des clients de votre taille ».\nJamais une vérité universelle — pas d'AI hype.")

stats = [
    ("~70 %",   "des Fortune 1000\nutilisent Cursor.\n(positionnement officiel)"),
    ("15–25 %", "réduction cycle-time chez les\norgs IA-adoptantes — au-dessus\nde 60 % d'usage hebdo seniors."),
    ("10–15 %", "du temps eng = PR review,\nplus gros sink après coding.\nCompressible nettement."),
    ("Senior IC", "opt-out = signal #1.\nQuand les meilleurs n'utilisent pas,\nplafond ROI org ≈ 5 %."),
]
x = Inches(0.55)
for big, body in stats:
    add_rect(s, x, Inches(4.1), Inches(2.95), Inches(2.6), BG_PANEL)
    add_rect(s, x, Inches(4.1), Inches(2.95), Emu(6350), HAIRLINE)
    add_text(s, x + Inches(0.3), Inches(4.3), Inches(2.6), Inches(0.9),
             big, size=32, bold=True, color=TEXT, letter_spacing=-20)
    add_text(s, x + Inches(0.3), Inches(5.3), Inches(2.6), Inches(1.4),
             body, size=11.5, color=TEXT_DIM, line_spacing=1.4)
    x += Inches(3.1)


# --- 12 — ROI math (live) -----------------------------------------------------
s = add_slide(); page_chrome(s, 12, TOTAL, "ROI · à faire en live")
section_title(s, "Le calcul à projeter à l'écran",
              "Modèle, pas promesse.",
              "Demander à Figma de corriger N. La correction = engagement.")

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
         size=10.5, color=ACCENT_SOFT, letter_spacing=20, italic=True)


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


# --- 14 — Objection CISO · Privacy Mode --------------------------------------
s = add_slide(); page_chrome(s, 14, TOTAL, "Objection · CISO")
section_title(s, "Minute 14 — je la pose moi-même",
              "« Encore un vendor avec notre code. »",
              "Privacy Mode + SOC 2. Trois bullets exacts, pas de feature dump.")

items = [
    ("01", "Code non-stocké",
     "Customer code is not stored or retained — c'est contractuel, "
     "pas un toggle. Le code n'atterrit pas sur nos disques."),
    ("02", "Pas d'entraînement",
     "Code is not used to train models — ni les nôtres, ni ceux "
     "des providers tiers. Garantie contractuelle."),
    ("03", "Requêtes éphémères",
     "Requests are isolated and ephemeral — pas de log persistant "
     "des prompts ni des completions en mode privé."),
    ("04", "Enterprise readiness",
     "SOC 2 · contrôles admin · visibilité · SSO. Call security ↔ "
     "security sous 7 jours, avec SIG + pentest en amont."),
]
y = Inches(3.65)
for n, k, body in items:
    add_text(s, Inches(0.55), y, Inches(0.7), Inches(0.5),
             n, size=16, color=TEXT_MUTED, font=FONT_MONO)
    add_text(s, Inches(1.4), y, Inches(3.5), Inches(0.5),
             k, size=14, bold=True, color=TEXT)
    add_text(s, Inches(5.2), y, Inches(7.6), Inches(0.8),
             body, size=12, color=TEXT_DIM, line_spacing=1.4)
    add_hairline(s, Inches(0.55), y + Inches(0.78), Inches(12.25))
    y += Inches(0.85)


# --- 15 — Close · two tracks --------------------------------------------------
s = add_slide(); page_chrome(s, 15, TOTAL, "Close · Next steps")
section_title(s, "17:00 — la sortie",
              "Deux tracks parallèles, jamais « un pilote ».",
              "Aucun des deux personas n'est le bottleneck de l'autre.")

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
         size=10.5, color=ACCENT_SOFT, letter_spacing=20, italic=True)


# --- 16 — Rappels tactiques ---------------------------------------------------
s = add_slide(); page_chrome(s, 16, TOTAL, "Rappels tactiques")
section_title(s, "À garder en tête sur le call",
              "Le détail qui fait gagner.",
              "Petites choses, gros impact sur l'issue de l'appel.")

tips = [
    ("Lead with discovery, not pitch",
     "60 % du temps c'est eux qui parlent. On poursuit la compréhension avant l'opinion."),
    ("Opinionated, not scripted",
     "Avoir un point de vue. Reconnaître les tradeoffs vs Copilot et Claude Code."),
    ("Pressure-test l'urgence",
     "« Pourquoi maintenant, pas dans 6 mois ? » Si pas de réponse claire = pas de deal."),
    ("Adjust par persona",
     "CTO = vélocité et talent. CISO = privacy mode + SOC 2. Pas la même histoire."),
    ("Customer stories > AI hype",
     "Citer des pairs (Fortune 1000, ~70 %) plutôt que des claims génériques."),
    ("Silence > comblement",
     "Compter 3 secondes après chaque question. Le premier qui parle perd."),
]
y = Inches(3.65); x_cols = [Inches(0.55), Inches(6.95)]
for i, (k, v) in enumerate(tips):
    x = x_cols[i % 2]
    yy = y + (i // 2) * Inches(1.1)
    add_text(s, x, yy, Inches(0.3), Inches(0.4), "→", size=16, color=TEXT_MUTED)
    add_text(s, x + Inches(0.35), yy, Inches(5.7), Inches(0.4),
             k, size=13, bold=True, color=TEXT)
    add_text(s, x + Inches(0.35), yy + Inches(0.4), Inches(5.7), Inches(0.65),
             v, size=11.5, color=TEXT_DIM, line_spacing=1.4)


# --- 17 — Meta · ce qui est évalué (candidate-only) --------------------------
s = add_slide(); page_chrome(s, 17, TOTAL, "Meta · candidate-only")
section_title(s, "À masquer pendant le role-play",
              "Ce qui est vraiment évalué.",
              "Cinq signaux à émettre activement pendant les 20 minutes.")

# Two-column: signals vs anti-signals
def signal_col(x, label, items, color_dot):
    add_rect(s, x, Inches(3.6), Inches(6.1), Inches(3.4), BG_PANEL)
    add_rect(s, x, Inches(3.6), Inches(6.1), Emu(6350), HAIRLINE)
    add_text(s, x + Inches(0.3), Inches(3.75), Inches(5.5), Inches(0.4),
             label, size=10, color=TEXT_MUTED, letter_spacing=300)
    yy = Inches(4.15)
    for item in items:
        add_text(s, x + Inches(0.3), yy, Inches(0.3), Inches(0.4),
                 "●", size=12, color=color_dot)
        add_text(s, x + Inches(0.65), yy, Inches(5.3), Inches(0.4),
                 item, size=13, color=TEXT, line_spacing=1.4)
        yy += Inches(0.45)

signal_col(Inches(0.55), "SIGNAUX FORTS — à émettre", [
    "Prepared — preuves de recherche Figma",
    "Self-aware — nommer ses tradeoffs",
    "Composed — gérer le silence",
    "Tactically sharp — questions ciblées",
    "Coachable — accueillir le pushback",
], ACCENT_SOFT)

signal_col(Inches(6.75), "SIGNAUX FAIBLES — à éviter", [
    "Feature dump",
    "AI hype générique",
    "Overconfident sans grounding",
    "Pitcher avant d'avoir compris",
    "Donner une opinion sans contexte",
], TEXT_MUTED)

add_text(s, Inches(0.55), Inches(7.05 - 0.2), Inches(12), Inches(0.3),
         "Rubrique : prepared · self-aware · composed · tactically sharp · coachable.",
         size=10.5, color=ACCENT_SOFT, letter_spacing=20, italic=True)


# --- Save ---------------------------------------------------------------------
out = "/workspace/decks/Cursor_x_Figma_Discovery_20min.pptx"
prs.save(out)
print(f"OK  →  {out}")
