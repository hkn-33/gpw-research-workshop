English | [Polski](README_PL.md)

# GPW Research Workshop

An AI-agent workshop for equity research on the Warsaw Stock Exchange: **what to buy, what to sell, and when**. Four value-investing lenses — Buffett, Munger, Duan Yongping, Li Lu — turned into 14 repeatable research playbooks with hard anti-bias rules, exact-decimal arithmetic and a numbers audit before any report is trusted.

Inspired by [xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) (MIT), re-built for the GPW with its own toolchain.

> Research tool, not investment advice. It executes no trades — decisions and orders are yours.

## How it works

Skills are plain-markdown playbooks: a precise, opinionated procedure an LLM agent follows — which data to pull, which tools to run, what the report must contain (always ending in tiered price ranges, never "on one hand, on the other hand"). Agents are role definitions the heavier skills delegate to: a data scout, four independent master lenses that are designed to disagree, an auditor that re-verifies numbers, a timing specialist. Tools are dependency-free Python CLIs for market data, screening, backtesting and exact arithmetic.

## Quick start (Claude Code)

```bash
git clone <your-repo-url> gpw && cd gpw
scripts/install-claude.bat        # Windows; on macOS/Linux: sh scripts/install-claude.sh
cp portfolio.example.md portfolio.md   # then fill in your positions
```

Open the folder in Claude Code and type your first command:

```
/gpw-scanner            # hunt for momentum+value buy signals on the watchlist
/gpw-analyze XTB        # full four-lens analysis with buy/sell price ranges
/gpw-portfolio          # SELL / BUY / WAIT orders for your current positions
```

## Using other models (ChatGPT, DeepSeek, Codex, ...)

Nothing here is Claude-specific:

- **Any chat model**: paste the content of a `skills/*.md` file plus your ticker as the prompt. Give it the `agents/*.md` role files when the skill references them. `AGENTS.md` carries the project-wide rules many agent CLIs (e.g. Codex) pick up automatically.
- **Tools**: plain Python 3, standard library only — `python tools/gpw_data.py quote PKN` works anywhere.

## The 14 skills

### Finding ideas
| Skill | What it does | Time |
|-------|--------------|------|
| `gpw-scanner` | 60-day breakouts + volume, confirmed by fundamentals → BUY signals with 3/5/8% position weights | minutes |
| `gpw-quality-screen` | 7 hard criteria (ROE, FCF, margins, debt, dilution) eliminate weak companies | ~30 min |
| `gpw-funnel` | whole theme → ≤10 candidates → 3 deep dives → portfolio proposal | hours |
| `gpw-sector` | value-chain map: who earns what, which link is investable in Warsaw | hours |

### Deciding
| Skill | What it does | Time |
|-------|--------------|------|
| `gpw-checklist` | Buffett's 6 gates + the mirror test — worth digging at all? | ~10 min |
| `gpw-analyze` | **the workhorse**: four master lenses in one pass → ratings, buy/hold/sell ranges in PLN | 10–20 min |
| `gpw-analyze-team` | heavyweight: 4 independent agents in parallel + full numbers audit — for big positions | 30–60 min |
| `gpw-management` | management X-ray: promises vs delivery, insider trades, political appointments | ~30 min |

### Monitoring
| Skill | What it does | Time |
|-------|--------------|------|
| `gpw-daily` | briefing: market, price alerts on your positions, ESPI filings, earnings calendar | ~5 min |
| `gpw-pulse` | the stock moved hard — attribution: what ACTUALLY happened | 10–15 min |
| `gpw-earnings` | quarterly report read from primary sources, impact on your thesis | ~30 min |
| `gpw-thesis` | thesis check: do your reasons still hold? Falsified = a plain "SELL" | ~10 min |

### Portfolio and quality
| Skill | What it does |
|-------|--------------|
| `gpw-portfolio` | full review: SELL / BUY / WAIT orders with price levels |
| `gpw-audit` | verifies a sample of a report's numbers against independent sources |

A typical flow:

```
gpw-scanner → signal → gpw-checklist (10 min) → passed?
→ gpw-analyze → price ranges + thesis → you place the order at your broker
→ position goes into portfolio.md → gpw-daily every morning, gpw-portfolio weekly
```

## The 7 agents

| Agent | Role |
|-------|------|
| `gpw-scout` | collects data: quotes, fundamentals, ESPI filings, news — every key number from 2 sources |
| `master-business` | Duan Yongping: is this even a good business |
| `master-financials` | Buffett: numbers, valuation, price ranges |
| `master-risk` | Munger: devil's advocate — how this company dies |
| `master-certainty` | Li Lu: the 10-year test, management quality |
| `gpw-auditor` | re-verifies report numbers (PASS/FAIL verdict) |
| `gpw-timing` | when to enter/exit: tranches, levels, invalidation |

## The tools

```
python tools/gpw_data.py quote PKN CDR ALE       # quotes via Yahoo (.WA auto-appended)
python tools/gpw_data.py signals XTB             # SMA50/200, momentum, 52-week distance
python tools/gpw_screener.py                     # momentum+value scan of the watchlist
python tools/gpw_backtest.py XTB --years 5       # honesty check: strategy vs buy-and-hold
python tools/report_audit.py extract --report reports/XTB/XTB-analysis-20260707.md
python tools/financial_rigor.py three-scenario --price 121 --eps 10.5 --growth 20 10 0 --pe 15 11 8
```

No dependencies beyond Python 3 standard library. All financial arithmetic uses `decimal.Decimal`.

## Continuous mode

One-off: run skills when you want. Continuous: schedule `gpw-daily` every morning (in Claude Code: `/schedule run /gpw-daily daily at 8:00`) — you get alerts only when a position crosses its sell range, a watched name enters its buy range, a thesis condition trips, or results are due.

## Repository layout

```
skills/     14 research playbooks          agents/    7 role definitions
tools/      Python CLIs (stdlib only)      docs/      methodology
reports/    published research output      research/  working notes
data/       watchlist + fundamentals       scripts/   Claude Code installers
assets/     README images
```

`.gitignore` keeps `portfolio.md` (your positions), `CLAUDE.local.md` (personal preferences) and the installed `.claude/` copies out of the repository — the repo ships the system and the research, not your money.

## Methodology

The framework, anti-bias mechanisms, screen exemptions and post-purchase discipline are documented in [docs/methodology.md](docs/methodology.md).

## License

MIT. Methodology structure inspired by [xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) (MIT).
