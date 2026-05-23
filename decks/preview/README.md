# Preview — Cursor × Figma Discovery (20 min)

Rendu PDF + PNG du deck `decks/Cursor_x_Figma_Discovery_20min.pptx`.

## Fichiers

- `Cursor_x_Figma_Discovery_20min.pdf` — version PDF complète, 16 pages 16:9.
- `slide-01.png` … `slide-16.png` — chaque slide en PNG (110 dpi).

## Comment ouvrir

- **Le PDF** : `decks/preview/Cursor_x_Figma_Discovery_20min.pdf` — clic sur GitHub, ou téléchargement direct.
- **Le PPTX éditable** : `decks/Cursor_x_Figma_Discovery_20min.pptx` — à ouvrir dans Keynote, PowerPoint ou Google Slides.

## Sommaire

| # | Slide |
|---|---|
| 01 | Cover |
| 02 | Agenda 20 min |
| 03 | Contexte Figma |
| 04 | Personas CTO vs CISO |
| 05 | Opener (script) |
| 06 | Discovery — CTO (4 questions) |
| 07 | Discovery — CISO (3 questions) |
| 08 | Why Now |
| 09 | Why Change |
| 10 | Why Cursor |
| 11 | Pain numbers — productivité |
| 12 | ROI live |
| 13 | Pain numbers — sécurité |
| 14 | Objection CISO |
| 15 | Close — two tracks |
| 16 | Rappels tactiques |
| 17 | Meta — ce qui est évalué (candidate-only) |

## Regénérer

```bash
pip install python-pptx
python3 decks/build_deck.py
libreoffice --headless --convert-to pdf decks/Cursor_x_Figma_Discovery_20min.pptx --outdir decks/preview
pdftoppm -png -r 110 decks/preview/Cursor_x_Figma_Discovery_20min.pdf decks/preview/slide
```
