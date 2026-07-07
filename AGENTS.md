# Project instructions for AI agents

GPW equity-research workshop built on a four-master value framework (Buffett, Munger, Duan Yongping, Li Lu). Works with any capable LLM agent: the skills are plain markdown playbooks, the tools are plain Python.

## Layout

```
skills/     14 research playbooks (run as slash commands in Claude Code, or paste as prompts)
agents/     7 role definitions (scout, 4 master lenses, auditor, timing)
tools/      5 Python CLIs: gpw_data, gpw_screener, gpw_backtest, report_audit, financial_rigor
docs/       methodology.md — the framework in one file
data/       watchlist.json, fundamentals.json (agent-maintained quarterly data)
portfolio.md   the user's positions and watchlist (single source of truth)
reports/       all output, one folder per ticker
```

## Report naming

| Skill | File |
|-------|------|
| gpw-analyze | `reports/{TICKER}/{TICKER}-analysis-{YYYYMMDD}.md` + `{TICKER}-thesis.md` |
| gpw-analyze-team | `reports/{TICKER}/team-{YYYYMMDD}/` (4 lens reports + final-report.md) |
| gpw-quality-screen | `reports/screen-{topic}-{YYYYMMDD}.md` |
| gpw-funnel / gpw-sector | `reports/funnel-...` / `reports/sector-...` |
| gpw-portfolio | `reports/portfolio-current.md` (overwrite) |
| gpw-daily | `reports/journal.md` (prepend) |

## Non-negotiable principles

- Data first, then logic, then conclusion. Facts carry sources; opinions carry the label "judgment"; missing data is "no data", not a guess.
- Key numbers from 2 independent sources; market cap re-derived by hand (price x shares).
- No mental math — use `python tools/financial_rigor.py calc` or `decimal.Decimal`.
- Currency always explicit. Estimates marked "(est.)". Ratings 1–5, no halves.
- Every recommendation is tiered (aggressive / moderate / conservative, with PLN ranges). Fence-sitting conclusions are banned.
- State-owned companies are a separate, correlated political-risk class.
- Write reports in the language the user communicates in.

## Tools quick reference

```
python tools/gpw_data.py quote PKN CDR          # quotes (GPW tickers, .WA auto-appended)
python tools/gpw_data.py signals XTB            # SMA50/200, momentum, 52w distance
python tools/gpw_screener.py                    # momentum+value scan of the watchlist
python tools/gpw_backtest.py XTB --years 5      # strategy honesty check
python tools/report_audit.py extract --report <file>   # sample numbers for verification
python tools/financial_rigor.py three-scenario --price 121 --eps 10.5 --growth 20 10 0 --pe 15 11 8
```

This is a research tool, not investment advice. It executes no trades; decisions belong to the user.
