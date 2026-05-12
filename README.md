# media-ae-cockpit

Interview presentation assets for a Cursor Account Executive interview.

## Files

- `presentations/generate_cursor_ae_interview_deck.py` - editable PowerPoint generator
- `presentations/export_cursor_ae_deck_pdf.py` - PDF exporter for the generated deck
- `presentations/Cursor_AE_Interview_Deck.pptx` - generated presentation deck
- `presentations/Cursor_AE_Interview_Deck.pdf` - generated PDF version of the deck
- `presentations/cursor_ae_interview_notes.md` - speaker notes and customization guide

## Regenerate the deck

```bash
python3 -m pip install python-pptx
python3 presentations/generate_cursor_ae_interview_deck.py
python3 -m pip install reportlab
python3 presentations/export_cursor_ae_deck_pdf.py
```

## Customize before presenting

Update the `PROFILE` values in `presentations/generate_cursor_ae_interview_deck.py`:

- your name
- contact details
- 2-3 quantified sales wins
- any wording you want to tailor to your experience or interview prompt
