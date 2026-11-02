# nba-fantasy: weekly LePhilly roast

Scheduled job (Mon 20:00 UTC) roasts the finished ESPN matchup week and republishes the Artifact page.

- `scripts/fetch_week.py [period]` - pulls and computes all numbers (scores, margins, top players, all-play, biggest/lowest day, standings, live week). Exits non-zero if the week is not final.
- `scripts/render_pdf.js in.html out.pdf` - renders the 1080x1500 dark PDF with Playwright.
- `history/weekN.html` and `history/matchup-roast-weekN.pdf` - each week's published page and PDF.
- `history/jokes.md` - joke log; read before writing, append after.
