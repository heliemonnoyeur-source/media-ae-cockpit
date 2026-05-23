# Preview — Cursor Enterprise PG + Disco Challenge

Rendu PDF + PNG du deck `decks/Cursor_Enterprise_Disco_Challenge.pptx`.

## Fichiers

- `Cursor_Enterprise_Disco_Challenge.pdf` — version PDF complète, 24 pages 16:9.
- `slide-01.png` … `slide-24.png` — chaque slide en PNG (110 dpi).

## Comment ouvrir

- **PDF en ligne** : clic direct sur le fichier `.pdf` dans GitHub.
- **PPTX éditable** : `decks/Cursor_Enterprise_Disco_Challenge.pptx` — à ouvrir dans Keynote, PowerPoint ou Google Slides.

## Sommaire — 60 min en 3 parties

| # | Slide | Partie |
|---|---|---|
| 01 | Cover | Intro |
| 02 | Roadmap 60 min | Intro |
| 03 | Divider Part 1 | Greenfield |
| 04 | Critères de ranking F100 | Greenfield |
| 05 | Top 5 Fortune 100 ranked | Greenfield |
| 06 | JPMorgan — account thesis | Greenfield |
| 07 | JPMorgan — stakeholder map | Greenfield |
| 08 | JPMorgan — entry + first 90 days | Greenfield |
| 09 | JPMorgan — pilot motion | Greenfield |
| 10 | Divider Part 2 — Figma | Disco |
| 11 | Brief Figma (6 faits) | Disco |
| 12 | Agenda 20 min | Disco |
| 13 | Opener (script Marcel) | Disco |
| 14 | Discovery — Marcel (4 questions) | Disco |
| 15 | Discovery — Sécurité (3 questions) | Disco |
| 16 | Why Cursor — 4 angles Figma | Disco |
| 17 | Privacy Mode + SOC 2 | Disco |
| 18 | Close — follow-up précis | Disco |
| 19 | Divider Part 3 | Debrief |
| 20 | Top insights + deal hypothesis | Debrief |
| 21 | 4 questions stratégiques | Debrief |
| 22 | Deal risks + self-assessment | Debrief |
| 23 | Phrases-clés anti-blank | Disco |
| 24 | Meta — rubrique d'éval (candidate-only) | Meta |

## Regénérer

```bash
pip install python-pptx
python3 decks/build_deck.py
libreoffice --headless --convert-to pdf decks/Cursor_Enterprise_Disco_Challenge.pptx --outdir decks/preview
pdftoppm -png -r 110 decks/preview/Cursor_Enterprise_Disco_Challenge.pdf decks/preview/slide
```
