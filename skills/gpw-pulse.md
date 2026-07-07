# /gpw-pulse — rapid price-move attribution (10–15 minutes, not deep research)

Explain the price move: $ARGUMENTS (e.g. "PKN" or "CDR -8% in a week").

Goal: before you panic or celebrate, establish WHAT actually happened.

## Flow

1. **Scale of the move**: `python tools/gpw_data.py history TICKER --days 30`, compare with the index (`history WIG20.WA --days 30`) — how much of the move is market beta and how much is the stock?
2. **Four-track recon in parallel** (WebSearch/WebFetch; one `gpw-scout` agent works too):
   - company filings (ESPI/EBI, results, brokerage recommendations)
   - regulation/politics (relevant on the GPW: sector taxes, government decisions on state-owned firms)
   - industry and competitors (is the whole sector moving?)
   - sentiment and flows (recommendations, forums, insider trades)
3. **Attribution, not enumeration**: judge which event ACTUALLY explains the move, with an estimated contribution in % and a confidence level.

## Output (tight)

1. **One-sentence attribution**
2. Table: candidate explanation / estimated contribution / confidence
3. **Mandatory classification**: Value event / Sentiment swing / **Cause unknown** (often the most valuable outcome — possible insider activity) / Mixed
4. **Action**: do nothing / re-check the thesis in `reports/{TICKER}/{TICKER}-thesis.md` / trigger `/gpw-analyze`

Save only if the user asks (this is a quick tool, not a report). Respond in the user's language.
