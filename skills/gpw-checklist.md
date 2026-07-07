# /gpw-checklist — Buffett's pre-purchase checklist (6 gates, decision in 10 minutes)

Run the checklist on: $ARGUMENTS (one or several companies — several get a single comparison table).

## Six gates (sequential; failing a gate = STOP, do not continue)

1. **Circle of competence** — do I understand how this company makes money? (one sentence)
2. **Good business** — what are the economics? (margins, recurrence, capital intensity)
3. **Moat** — how deep is the advantage and is it deepening?
4. **Management** — can they be trusted? (actions, not words; on the GPW: political appointments)
5. **Margin of safety** — is the price low enough? (compute with `tools/financial_rigor.py`)
6. **Decision discipline** — rational or FOMO? (why NOW?)

Each gate: 1–5 rating + verdict PASS / FAIL / GRAY.

## Mirror test (mandatory finale)

"I am buying {COMPANY} at {PRICE} PLN because: (1) the business essence is... (2) the moat is... (3) management... (4) price vs value... (5) even if I am wrong, the downside is limited because..."

**Doesn't fit in 5 sentences = don't buy. No exceptions.**

## Data

Quotes: `python tools/gpw_data.py quote/signals`. Fundamentals: biznesradar.pl / stockwatch.pl (WebSearch/WebFetch). Several companies → parallel `gpw-scout` agents.

Save to `reports/{TICKER}/{TICKER}-checklist-{YYYYMMDD}.md`; multi-company runs to `reports/comparison-checklist-{YYYYMMDD}.md`. Final verdict per company: Pass / Conditional / Gray / Fail + summary table. Write in the user's language.
