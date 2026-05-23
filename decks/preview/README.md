# Preview — Cursor Enterprise PG + Disco Challenge

PDF + PNG renders of `decks/Cursor_Enterprise_Disco_Challenge.pptx`.

## Files

- `Cursor_Enterprise_Disco_Challenge.pdf` — full PDF, 24 pages 16:9.
- `slide-01.png` … `slide-24.png` — one PNG per slide (110 dpi).

## How to open

- **Online PDF**: click the `.pdf` file directly in GitHub.
- **Editable PPTX**: `decks/Cursor_Enterprise_Disco_Challenge.pptx` — open in Keynote, PowerPoint or Google Slides.

## Contents — 60 min in 3 parts

| # | Slide | Part |
|---|---|---|
| 01 | Cover | Intro |
| 02 | Roadmap 60 min | Intro |
| 03 | Divider Part 1 | Greenfield |
| 04 | Ranking criteria | Greenfield |
| 05 | Top 5 Spain & Italy ranked | Greenfield |
| 06 | Santander — account thesis | Greenfield |
| 07 | Santander — stakeholder map | Greenfield |
| 08 | Santander — entry + first 90 days | Greenfield |
| 09 | Santander — pilot motion (Openbank wedge) | Greenfield |
| 10 | Divider Part 2 — Figma | Disco |
| 11 | Figma brief (6 facts) | Disco |
| 12 | Disco agenda (20 min) | Disco |
| 13 | Opener (Marcel script) | Disco |
| 14 | Discovery — Marcel (4 Qs) | Disco |
| 15 | Discovery — Security (3 Qs) | Disco |
| 16 | Why Cursor — 4 Figma-calibrated angles | Disco |
| 17 | Privacy Mode + SOC 2 | Disco |
| 18 | Close — specific follow-up | Disco |
| 19 | Divider Part 3 | Debrief |
| 20 | Top insights + deal hypothesis | Debrief |
| 21 | 4 strategic questions | Debrief |
| 22 | Deal risks + self-assessment | Debrief |
| 23 | Anti-blank key phrases | Disco |
| 24 | Meta — evaluation rubric (candidate-only) | Meta |

## Regenerate

```bash
pip install python-pptx
python3 decks/build_deck.py
libreoffice --headless --convert-to pdf decks/Cursor_Enterprise_Disco_Challenge.pptx --outdir decks/preview
pdftoppm -png -r 110 decks/preview/Cursor_Enterprise_Disco_Challenge.pdf decks/preview/slide
```
