# Contributing

Contributions welcome — especially:

- **New or improved skills** (`skills/*.md`): keep the format — one job per skill, an explicit flow, a mandatory output format ending in a verdict. No fence-sitting conclusions.
- **Research reports** (`reports/`): reports generated with this framework, with sources on every key number. Reports that failed the `/gpw-audit` gate will not be merged.
- **Tool fixes** (`tools/`): standard library only, no new dependencies. Every non-trivial change needs a runnable check.
- **Data source fixes**: Yahoo symbols come and go; corrections to `data/watchlist.json` are appreciated.

## Ground rules

1. Facts with sources, opinions labeled as opinions. "No data" beats a plausible guess.
2. All financial arithmetic goes through `tools/financial_rigor.py` — no numbers computed in prose.
3. English for skills, agents, tools and docs. Reports may be in any language (they are written in the user's language by design).
4. Keep diffs small and boring. One topic per pull request.

## Before opening a PR

```
python tools/gpw_data.py quote PKN        # tools still work
python tools/report_audit.py extract --report <your-report>   # if contributing a report
```
