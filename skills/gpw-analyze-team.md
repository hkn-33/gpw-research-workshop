# /gpw-analyze-team — deep analysis by four independent master agents (30–60 min, deliberately)

Run a team analysis of: $ARGUMENTS

The heavyweight path — for large positions and hard calls. For everyday decisions use `/gpw-analyze` (single context). Warn the user about the runtime before starting. Framework background: `docs/methodology.md`.

## Flow

### Step 1 — Scout
The `gpw-scout` agent gathers the data pack for the company. Pass its report to every master in their prompt so four agents don't hunt the same numbers.

### Step 2 — Four masters IN PARALLEL (one message, four Agent calls)
`master-business` (Duan Yongping), `master-financials` (Buffett), `master-risk` (Munger), `master-certainty` (Li Lu). Each receives: the ticker, the scout's report, the A/B/C researchability rating, and an instruction to return a 1–5 rating.

### Step 3 — Save the partial reports
```
reports/{TICKER}/team-{YYYYMMDD}/
├── 01-business-duan.md
├── 02-financials-buffett.md
├── 03-risk-munger.md
├── 04-certainty-lilu.md
└── final-report.md
```

### Step 4 — Synthesis (you as team lead)
Do not average the ratings — surface the tensions between masters. Final report structure:
1. One-sentence conclusion
2. Four-lens ratings table + composite x.x/5
3. Key data (2-year table)
4. Bull vs bear case (5–7 points each)
5. Tiered recommendation (Aggressive / Moderate / Conservative with PLN price ranges)
6. Catalysts: add-to-position signals / reduce signals
7. Mirror test (thesis in 5 sentences or fewer)

Update the thesis and falsification conditions in `reports/{TICKER}/{TICKER}-thesis.md`.

### Step 5 — Full audit (mandatory on this path)
Run the `gpw-auditor` agent on the final report (the `/gpw-audit` workflow). A FAIL verdict means: fix the numbers, recompute the price ranges if affected, only then hand the report to the user.

Write all reports in the language the user communicates in.
