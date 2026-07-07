# /gpw-portfolio — portfolio review: what to buy, what to sell, when

Review the portfolio. Optional arguments: $ARGUMENTS — e.g. an ad-hoc mix "PKN 30%, PKO 20%, cash 50%". No arguments: read `portfolio.md`.

## Flow

1. **State**: load `portfolio.md` (positions, entry prices, theses, watchlist). Pull current prices and signals: `python tools/gpw_data.py quote ...` and `signals ...` for all positions plus the watchlist.
2. **Thesis check**: for every position read `reports/{TICKER}/{TICKER}-thesis.md` — any falsification condition met? Quick WebSearch for fresh events (last month) per position.
3. **Portfolio structure**: concentration (largest position?), sector exposure, combined weight of state-owned companies (their political risk is correlated!), cash level.
4. **Price levels**: compare current prices with the buy/hold/sell ranges from the latest analyses; a position with no analysis on file gets flagged with a `/gpw-analyze` suggestion.

## Output

1. **Portfolio table**: position / weight / entry / current / result % / thesis status (valid / watch / falsified) / action
2. **Orders** (concrete, no hedging):
   - **SELL**: what, why, at what price (thesis falsified, or price above the sell range)
   - **BUY/ADD**: what, at what price, target weight
   - **WAIT**: what to watch and which level triggers action
3. **Structural risks**: concentration, correlations, politics
4. Update the "Last review" section of `portfolio.md` and save the report to `reports/portfolio-current.md` (overwrite).

Rule: selling requires a reason (thesis dead / price above value / clearly better alternative) — never "because it dropped". Write in the user's language.
