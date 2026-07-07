# /gpw-analyze — single-pass company analysis through four master lenses (target: 10–20 min)

Analyze the company: $ARGUMENTS

Runs all modules yourself, in sequence, in one context — no subagents. For large positions (>10% of portfolio) use the heavyweight `/gpw-analyze-team` instead. Framework background: `docs/methodology.md`.

## Step 0 — Researchability rating (A/B/C)

Rate information availability: A (WIG20-class coverage — beware of echoing consensus, actively hunt counter-arguments) / B (moderate — tag estimated figures with confidence) / C (scarce — first-principles mode: who pays, why do they come back, could a well-funded competitor copy this). Put the rating at the top of the report.

## Step 1 — Data (lean, no agent)

- `python tools/gpw_data.py quote TICKER` and `signals TICKER`
- biznesradar.pl (WebFetch: 5–10 years of ratios) plus 1–2 fresh sources (results, ESPI filings)
- market cap by hand: `python tools/financial_rigor.py verify-market-cap ...`
- Confirm decision-critical numbers (price, EPS/profit, share count, net debt) in 2 sources; do not double-source everything else.

## Step 2 — Four modules (consecutive report sections; the `agents/master-*.md` profiles define each lens)

1. **Business essence (Duan Yongping)**: what the company really earns money on, in one sentence; is it a good business; the irreplaceability test; what will NOT change in 10 years. Rating 1–5.
2. **Financials and valuation (Buffett)**: earnings quality (ROE, FCF vs net profit, debt); three-scenario valuation via `python tools/financial_rigor.py three-scenario` (growth in percent, e.g. 20 10 0); margin of safety vs own 10-year P/E history. Rating 1–5.
3. **Inversion (Munger)**: five ways this company dies, with probabilities; the real bear case; red-flag vetoes; state-owned/regulatory risk. Rating 1–5.
4. **10-year certainty and management (Li Lu)**: the 10-year test (YES/NO/DON'T KNOW); capital allocation record — actions, not words; structural trend alignment. Rating 1–5.

Show the TENSIONS between modules explicitly — disagreement between lenses is information, not a defect.

## Step 3 — Verdict (mandatory, no fence-sitting)

1. One-sentence conclusion + ratings table (4 lenses + composite x.x/5)
2. Tiered recommendation: Aggressive / Moderate / Conservative, each with a price range in PLN
3. Action signals: buy below X / hold / sell above Y, plus measurable thesis-falsification conditions
4. Mirror test: the thesis in 5 sentences or fewer (if it doesn't fit — don't buy)

## Step 4 — Save and quick check

- Report: `reports/{TICKER}/{TICKER}-analysis-{YYYYMMDD}.md`; thesis: `reports/{TICKER}/{TICKER}-thesis.md`
- **Inline mini-audit** (no agent): re-verify 3–5 decision-critical numbers (price, EPS, market cap, price ranges). The full sampled audit runs only in `/gpw-analyze-team` or on demand via `/gpw-audit`.
- Entry timing on request: the `gpw-timing` agent (optional — ask the user).

Write the report in the language the user communicates in.
