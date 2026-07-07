"""Backtest the momentum strategy on real GPW price history.

Strategy (layer 1 of the screener):
  BUY:  close above the 60-day high AND 5-day avg volume > 1.5x 20-day avg
  SELL: close below SMA50, OR drawdown from the position's peak exceeds the
        trailing stop (default 15%)

The point is honesty calibration: on steady long-trend names momentum often
loses to buy-and-hold, and it is better to know that before trusting a signal.

Usage:
  python tools/gpw_backtest.py PKN                 # 2 years, 15% stop
  python tools/gpw_backtest.py CDR --years 5 --stop 20
  python tools/gpw_backtest.py PKN KGH XTB         # several tickers, summary table
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gpw_data import ohlc


def sma(closes, i, n):
    return sum(closes[i - n + 1:i + 1]) / n


def backtest(ticker, years=2, stop_pct=15.0, verbose=True):
    rng = {1: "1y", 2: "2y", 5: "5y", 10: "10y"}.get(years, "2y")
    candles = ohlc(ticker, rng)
    if len(candles) < 120:
        print(f"{ticker}: not enough data ({len(candles)} sessions)")
        return None
    closes = [c["close"] for c in candles]

    position = None  # {"price", "date", "peak"}
    trades = []
    for i in range(61, len(candles)):
        day = candles[i]
        close = day["close"]
        if position:
            position["peak"] = max(position["peak"], close)
            drawdown = (close / position["peak"] - 1) * 100
            below_sma50 = i >= 50 and close < sma(closes, i, 50)
            if below_sma50 or drawdown < -stop_pct:
                trades.append({
                    "buy_date": position["date"], "buy": position["price"],
                    "sell_date": day["date"], "sell": close,
                    "result": (close / position["price"] - 1) * 100,
                    "exit": "SMA50" if below_sma50 else f"stop {stop_pct:.0f}%",
                })
                position = None
        else:
            high60 = max(c["high"] for c in candles[i - 60:i])
            vol5 = sum(c["volume"] for c in candles[i - 4:i + 1]) / 5
            vol20 = sum(c["volume"] for c in candles[i - 19:i + 1]) / 20
            if close > high60 and vol20 > 0 and vol5 / vol20 > 1.5:
                position = {"price": close, "date": day["date"], "peak": close}

    if position:  # still open - mark to market
        trades.append({
            "buy_date": position["date"], "buy": position["price"],
            "sell_date": "(open)", "sell": closes[-1],
            "result": (closes[-1] / position["price"] - 1) * 100, "exit": "-",
        })

    capital = 1.0
    for t in trades:
        capital *= 1 + t["result"] / 100
    strategy = (capital - 1) * 100
    buy_hold = (closes[-1] / closes[61] - 1) * 100
    winners = sum(1 for t in trades if t["result"] > 0)

    if verbose:
        print(f"\n{ticker} ({candles[61]['date']} to {candles[-1]['date']}, stop {stop_pct:.0f}%)")
        for t in trades:
            print(f"  {t['buy_date']} buy {t['buy']:.2f} -> {t['sell_date']} "
                  f"sell {t['sell']:.2f}  {t['result']:+.1f}%  ({t['exit']})")
        if not trades:
            print("  (no buy signals in the period)")
        print(f"  strategy {strategy:+.1f}% | buy-and-hold {buy_hold:+.1f}% | "
              f"hit rate {winners}/{len(trades)}")
    return {"ticker": ticker, "strategy": strategy, "buy_hold": buy_hold,
            "trades": len(trades), "winners": winners}


def main():
    args = sys.argv[1:]
    years, stop = 2, 15.0
    if "--years" in args:
        i = args.index("--years"); years = int(args[i + 1]); del args[i:i + 2]
    if "--stop" in args:
        i = args.index("--stop"); stop = float(args[i + 1]); del args[i:i + 2]
    if not args:
        print(__doc__)
        sys.exit(1)
    results = [r for t in args if (r := backtest(t.upper(), years, stop))]
    if len(results) > 1:
        print("\nticker,strategy%,buy_hold%,trades,winners")
        for r in results:
            print(f"{r['ticker']},{r['strategy']:.1f},{r['buy_hold']:.1f},{r['trades']},{r['winners']}")


if __name__ == "__main__":
    main()
