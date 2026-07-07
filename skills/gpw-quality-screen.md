# /gpw-quality-screen — quality sieve: fast elimination of weak companies

Screen: $ARGUMENTS (companies, an index like "WIG20", a sector like "GPW banks", or a theme). No arguments: screen the watchlist from `portfolio.md`.

Purpose: cheaply remove companies that cannot be first-rate, so deep analysis time goes only to survivors. Exemption rules and rationale: `docs/methodology.md`.

## Seven hard criteria (fail one = out, unless an exemption applies)

| # | Metric | Reject when | What it measures |
|---|--------|-------------|------------------|
| 1 | 10-year average ROE | < 8% | capital efficiency |
| 2 | Cumulative 5-year FCF | negative | whether profit is real cash |
| 3 | Interest coverage (EBIT/interest) | < 2x | debt safety (skip for banks/insurers) |
| 4 | Long-term gross margin | < 15% | pricing power |
| 5 | Operating CF / net profit (5y avg) | < 0.7 | earnings quality |
| 6 | Long-term net margin | < 5% | resilience |
| 7 | Share count growth over 5 years | > 20% (non-M&A) | dilution |

Exemptions A/B/C (strategic investment phase; deliberately suppressed margin; high-turnover thin-margin model) — apply per `docs/methodology.md`.

## Flow

1. Resolve the company list (index → WebSearch for constituents; sector/theme → 10–20 largest).
2. Data: `python tools/gpw_data.py quote/signals` plus biznesradar.pl / stockwatch.pl for historical ratios. With more than 8 companies, split across parallel `gpw-scout` agents in batches.
3. Judge each company against the 7 criteria. Result: PASS / FAIL (which criterion) / GRAY (missing data).
4. For passers add a technical-trend column from `gpw_data.py signals` — informational only, never a criterion.

## Output

Summary table + pass-rate stats + a **shortlist of candidates for `/gpw-analyze`** (max 5, ranked). Save to `reports/screen-{topic}-{YYYYMMDD}.md`.

Rule: better to let a weak company through than to kill a great one — when in doubt, GRAY, not FAIL. Write the report in the user's language.
