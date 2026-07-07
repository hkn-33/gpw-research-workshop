"""Warsaw Stock Exchange quotes via Yahoo Finance. No API key needed.

Usage:
  python tools/gpw_data.py quote PKN PKO CDR ALE      # current quotes
  python tools/gpw_data.py history PKN --days 90      # daily closes (CSV)
  python tools/gpw_data.py signals PKN CDR KGH        # SMA50/200, momentum, 52w

GPW tickers go without a suffix (PKN, CDR, ALE...) - .WA is appended
automatically. Symbols containing . ^ or = pass through unchanged
(AAPL.US-style, ^SPX, WIG20.WA, EURPLN=X).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import datetime
import json
import statistics
import urllib.request

UA = {"User-Agent": "Mozilla/5.0"}


def yahoo_symbol(t):
    return t if any(ch in t for ch in ".^=") else t.upper() + ".WA"


def chart(symbol, rng="2y"):
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/"
           f"{urllib.request.quote(yahoo_symbol(symbol))}?range={rng}&interval=1d")
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    result = data["chart"]["result"]
    if not result:
        raise ValueError(f"no data for {symbol}")
    return result[0]


def quote(symbols):
    print("symbol,name,price,currency,52w_low,52w_high,volume")
    for s in symbols:
        try:
            m = chart(s, "5d")["meta"]
            print(f"{s.upper()},{m.get('longName', '?')},{m['regularMarketPrice']},"
                  f"{m['currency']},{m.get('fiftyTwoWeekLow', '')},"
                  f"{m.get('fiftyTwoWeekHigh', '')},{m.get('regularMarketVolume', '')}")
        except Exception as e:
            print(f"{s.upper()},ERROR:{e}")


def ohlc(symbol, rng="2y"):
    """Daily candles: [{date, close, high, low, volume}, ...]."""
    c = chart(symbol, rng)
    ts = c["timestamp"]
    q = c["indicators"]["quote"][0]
    out = []
    for i, t in enumerate(ts):
        if q["close"][i] is not None:
            out.append({
                "date": datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d"),
                "close": q["close"][i],
                "high": q["high"][i] or q["close"][i],
                "low": q["low"][i] or q["close"][i],
                "volume": q["volume"][i] or 0,
            })
    return out


def history(symbol, days):
    rng = "3mo" if days <= 90 else ("1y" if days <= 365 else "2y")
    print("date,close,volume")
    for c in ohlc(symbol, rng)[-days:]:
        print(f"{c['date']},{round(c['close'], 2)},{c['volume']}")


def signals(symbols):
    print("symbol,price,sma50,sma200,trend,mom_1m%,mom_3m%,mom_6m%,mom_12m%,off_52w_high%")
    for sym in symbols:
        try:
            closes = [c["close"] for c in ohlc(sym, "2y")]
        except Exception as e:
            print(f"{sym.upper()},ERROR:{e}")
            continue
        if len(closes) < 60:
            print(f"{sym.upper()},INSUFFICIENT_DATA")
            continue
        price = round(closes[-1], 2)
        sma50 = statistics.mean(closes[-50:])
        sma200 = statistics.mean(closes[-200:]) if len(closes) >= 200 else None
        trend = "?"
        if sma200:
            trend = ("UP" if price > sma50 > sma200
                     else "DOWN" if price < sma50 < sma200 else "FLAT")

        def mom(n):
            return f"{(price / closes[-n] - 1) * 100:.1f}" if len(closes) > n else "-"

        high52 = max(closes[-252:])
        s200 = f"{sma200:.2f}" if sma200 else "-"
        print(f"{sym.upper()},{price},{sma50:.2f},{s200},{trend},"
              f"{mom(21)},{mom(63)},{mom(126)},{mom(252)},{(price / high52 - 1) * 100:.1f}")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "quote":
        quote(args)
    elif cmd == "history":
        days = 365
        if "--days" in args:
            i = args.index("--days")
            days = int(args[i + 1])
            args = args[:i]
        history(args[0], days)
    elif cmd == "signals":
        signals(args)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
