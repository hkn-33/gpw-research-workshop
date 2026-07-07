# /gpw-funnel — selection funnel: whole market → ≤10 → 3 deep dives

Run a funnel selection for: $ARGUMENTS (an industry or theme, e.g. "Polish banks", "GPW exporters", "EU-funds beneficiaries").

## Stages

1. **Full market scan** (30–60 companies): trading activity + returns + top market caps within the theme. Sources: WebSearch, biznesradar.pl screeners, GPW index lists. Include NewConnect when the theme calls for it (with a liquidity warning).
2. **Rough cut → ≤10**: five hard value filters (as in `/gpw-quality-screen`). EVERY rejected company gets a stated reason — no black box.
3. **Detailed pass on ≤10**: 300–500 words per company (model, moat, financials, valuation, risk).
4. **Final three** — chosen for PORTFOLIO COMPLEMENTARITY (high certainty + moderate upside + high convexity), NOT simply the top three scores.
5. **Four-master analysis** of the final three (800–1200 words each; `master-*` agents in parallel).

## AI-bias countermeasures (apply actively)

- counter large-cap bias: do not skip sWIG80 names,
- counter English-language bias: use Polish sources (bankier, stockwatch, strefainwestorow, PAP Biznes),
- counter narrative bias: a fashionable story is not unit economics,
- mandatory list of "future IPO candidates" — key private players in the theme.

## Output

Recommended portfolio: Core / Satellite / Option (+ possible ETF) with weights and action signals (entry price levels). Run the `gpw-auditor` agent on the final report before delivery. Save to `reports/funnel-{topic}-{YYYYMMDD}.md`. Write in the user's language.
