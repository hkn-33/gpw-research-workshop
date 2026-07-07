# /gpw-scanner — momentum + value scanner (buy signals with position weights)

Run the technical-fundamental scanner for: $ARGUMENTS (tickers; empty = the whole watchlist from `data/watchlist.json`).

Wraps `tools/gpw_screener.py`. Philosophy: momentum DISCOVERS the candidate, fundamentals CONFIRM the buy. A breakout without fundamentals is a watch item, not a purchase.

## Flow

1. `python tools/gpw_screener.py [tickers]` — momentum layer (60-day high + 1.5x volume).
2. For **WATCH** results (momentum without fundamentals on file): pull the last 2–3 quarters (biznesradar.pl or the company's report) and record them:
   `python tools/gpw_screener.py --set TICKER YYYY-MM-DD "Q1 2026" --rev-yoy 12.0 --gm 24.0 --eps-beat 5.0`
   (eps_beat = surprise vs consensus; if no consensus exists, use net profit growth y/y and say so in the label). Then rescan.
3. For **BUY_x%** signals: before handing them over, check the breakout isn't driven by forum pumping, a tender offer or M&A rumor (WebSearch, last 7 days) — a breakout on a takeover bid is a different situation than one on earnings.
4. Optional trust calibration: `python tools/gpw_backtest.py TICKER --years 5` — how this exact strategy performed historically on this stock. On steady compounders momentum often loses to buy-and-hold; show that honestly.

## Output

Table: ticker / signal (BUY_3/5/8% / WATCH / PASS) / reason / news context / backtest result. BUY signals carry a suggested position weight. Reminder: the scanner is not a full analysis — before real money, run `/gpw-analyze` or at minimum `/gpw-checklist`.

Save only if the user asks (this is a daily tool, not a report). Respond in the user's language.
