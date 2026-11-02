# Updated routine prompt (paste into https://claude.ai/code/routines/trig_01JfPoVs2JLiax9fenZL4NAX)

Also add the repo bendaly818/nba-fantasy as a source on the routine so it is cloned on each run.

Keep the existing prompt, and make these changes:

1. Add: "REPO: bendaly818/nba-fantasy, branch claude/youthful-sagan-i59q4t (no PR). Read README.md first. Scripts: scripts/fetch_week.py, scripts/render_pdf.js; history/jokes.md is the joke log; history/ holds each week's html and pdf. If the repo is missing, attach it with add_repo (push access) and clone it."
2. DATA step: replace the manual curl description with `python3 scripts/fetch_week.py > week.json` (defaults to currentMatchupPeriod-1; exits non-zero if the week is UNDECIDED or scores are tiny: then stop without publishing).
3. Before writing, read history/jokes.md and avoid every joke in it.
4. PDF step: `node scripts/render_pdf.js matchup-roast.html matchup-roast-weekN.pdf`; upload it as an artifact asset (needs the `assets` capability) and point the page's noprint "Download the Week N PDF" link at it, then republish.
5. New final step: copy the page to history/weekN.html and the PDF to history/matchup-roast-weekN.pdf, append that week's jokes to history/jokes.md, commit, and push to claude/youthful-sagan-i59q4t.
6. Add: "If that week is already published (page weekNo equals the finished period and numbers match), do not republish; say so and stay quiet."
