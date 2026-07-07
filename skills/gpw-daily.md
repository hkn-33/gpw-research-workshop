# /gpw-daily — daily briefing: market, portfolio, alerts, actions

Morning/daily GPW briefing. Optional arguments: $ARGUMENTS. Designed for manual runs OR continuous operation via a scheduler.

## Flow (fast — target 5 minutes, not deep research)

1. **Market**: `python tools/gpw_data.py quote WIG20.WA MWIG40.WA SWIG80.WA ^SPX EURPLN=X USDPLN=X` — broad mood.
2. **Portfolio and watchlist**: `python tools/gpw_data.py signals <all tickers from portfolio.md>`.
3. **Alerts** — check EVERY condition:
   - a held position entered its SELL range, or a watched name entered its BUY range (ranges live in `reports/portfolio-current.md` and the thesis files under `reports/*/`)
   - a position moved more than 5% in a day or 10% in a week → mini-attribution as in `/gpw-pulse`
   - an SMA50/SMA200 cross (the `trend` column flipped in signals)
   - a fresh ESPI filing for a portfolio company (WebSearch, last 24h)
4. **Calendar**: WebSearch — today's/tomorrow's quarterly results for portfolio and watchlist names, dividends (record date, not payment date!), shareholder meetings.

## Output

```
## GPW — {date}
**Market**: WIG20 {x}% ... (1–2 sentences)
**Alerts**: action-required / watch-only / (none = say "none")
**Actions today**: a concrete list, or "nothing to do"
**Calendar**: tomorrow / this week
```

- No alerts = short report and stop. Do NOT invent actions — "nothing to do" is a good outcome.
- An action-required alert → immediately suggest the right skill (`/gpw-pulse X`, `/gpw-portfolio`, `/gpw-analyze X`).
- Save: prepend the entry to `reports/journal.md` (one file, newest on top). Write in the user's language.
