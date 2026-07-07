# /gpw-earnings — reading a periodic report from primary sources

Analyze the results: $ARGUMENTS (e.g. "PKN 2026Q1", "XTB annual report 2025").

Buffett's rule: **read the company's report, not the analysts' summaries of it**.

## Sources (primary only)

1. The ESPI periodic report + financial statements (company IR page, infostrefa.com)
2. The company's results presentation and the earnings call transcript/recap
3. NO brokerage commentary during analysis — only at the end, as a consensus comparison

## Reading order (the Buffett order)

1. **Cash flow before the income statement** — profit is an opinion, cash is a fact. Operating CF vs net profit.
2. **Balance sheet**: net debt, inventories, receivables (growing faster than revenue is a red flag), provisions.
3. **Income statement**: revenue momentum y/y and q/q, margins (gross → operating → net) and their DIRECTION, one-offs (strip them out).
4. **Notes and fine print**: accounting policy changes, related-party transactions, contingent liabilities, litigation.
5. **Management letter/commentary**: what management highlights — and what it went QUIET about vs last quarter.

All arithmetic: `python tools/financial_rigor.py calc` — never mental math.

## Output

1. Key-numbers table (y/y, q/q, vs consensus if available)
2. **The 3 things that matter most** in this report (facts)
3. **Red flags** (or "none")
4. Thesis impact: check `reports/{TICKER}/{TICKER}-thesis.md` — confirms / weakens / falsifies? Update the thesis.
5. Verdict: do these results move the buy/sell ranges from the last analysis?

Save to `reports/{TICKER}/{TICKER}-earnings-{period}.md`. After saving, spot-check the decision-critical numbers (`python tools/report_audit.py extract --report <file>`). Write in the user's language.
