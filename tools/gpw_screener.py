"""Momentum discovery + value confirmation screener for GPW stocks.

Layer 1 (momentum): close above the 60-day high with volume confirmation
(5-day avg volume > 1.5x the 20-day avg) puts a stock into the candidate pool.
Layer 2 (value): six fundamental checks on the latest reported quarters.
Signal tiers: 3/6 = starter position 3% | 4/6 = standard 5% | 5-6/6 = conviction 8%.

Usage:
  python tools/gpw_screener.py                    # scan the watchlist (data/watchlist.json)
  python tools/gpw_screener.py PKN CDR XTB        # scan specific tickers
  python tools/gpw_screener.py --set PKN 2026-05-15 "Q1 2026" --rev-yoy 12.0 --gm 24.0 --eps-beat 5.0

Quarterly fundamentals live in data/fundamentals.json and are maintained by the
agent: rev_yoy = revenue growth y/y %, gm = gross margin %, eps_beat = EPS
surprise vs consensus % (no consensus available? use net profit growth y/y and
note it in the label).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import json
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gpw_data import ohlc

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
FUND_FILE = os.path.join(DATA_DIR, "fundamentals.json")
WATCHLIST_FILE = os.path.join(DATA_DIR, "watchlist.json")

DEFAULT_WATCHLIST = {
    "wig20": ["PKN", "PKO", "PEO", "PZU", "KGH", "ALE", "DNP", "CDR", "LPP", "SPL",
              "KRU", "KTY", "BDX", "MBK", "ALR", "JSW", "PGE", "OPL", "CPS", "ZAB"],
    "mwig40": ["XTB", "TXT", "CIG", "WPL", "ATT", "MIL", "ENA", "ASB", "DVL", "GPW",
               "DOM", "PCO", "BFT", "11B", "PLW", "TEN"],
    "swig80_and_quality": ["SNT", "RBW", "DAT", "PCR", "APR"],
}


def load_json(path, default):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def check_momentum(candles):
    if len(candles) < 61:
        return None
    last = candles[-1]
    close = last["close"]

    highs_60 = [c["high"] for c in candles[-61:-1]]
    new_high = close > max(highs_60)

    vol5 = sum(c["volume"] for c in candles[-5:]) / 5
    vol20 = sum(c["volume"] for c in candles[-20:]) / 20
    vol_ratio = vol5 / vol20 if vol20 > 0 else 0

    close_30d = candles[-31]["close"] if len(candles) > 30 else candles[0]["close"]
    change_30d = (close - close_30d) / close_30d * 100

    # breakout within the last 5 sessions, not necessarily today
    recent_breakout = any(
        candles[i]["close"] > max(c["high"] for c in candles[i - 60:i])
        for i in range(-5, 0)
    )

    return {
        "triggered": (new_high or recent_breakout) and vol_ratio > 1.5,
        "close": round(close, 2),
        "date": last["date"],
        "new_60d_high": new_high,
        "vol_ratio": round(vol_ratio, 2),
        "change_30d": round(change_30d, 1),
    }


def check_value(ticker, signal_date=None):
    funds = load_json(FUND_FILE, {})
    if ticker not in funds or not funds[ticker].get("quarters"):
        return None
    quarters = sorted(funds[ticker]["quarters"].items())
    if signal_date:
        quarters = [(d, q) for d, q in quarters if d <= signal_date]
    if not quarters:
        return None

    cur = quarters[-1][1]
    prev = quarters[-2][1] if len(quarters) >= 2 else None
    prev2 = quarters[-3][1] if len(quarters) >= 3 else None

    checks = {}
    checks["revenue accelerating"] = cur["rev_yoy"] > prev["rev_yoy"] if prev else cur["rev_yoy"] > 20
    checks["margin expanding"] = (cur["gm"] > prev["gm"] or cur["gm"] > 55) if prev else cur["gm"] > 45
    checks["earnings surprise"] = cur["eps_beat"] > 10
    checks["high revenue growth"] = cur["rev_yoy"] > 15
    checks["healthy margin"] = cur["gm"] > 40
    if prev and prev2:
        checks["margin up 2 quarters"] = cur["gm"] > prev["gm"] > prev2["gm"]
    elif prev:
        checks["margin up 2 quarters"] = cur["gm"] > prev["gm"]
    else:
        checks["margin up 2 quarters"] = False

    score = sum(checks.values())

    # standalone pass conditions, calibrated on the NVDA/MU backtests upstream
    standalone, reason = False, ""
    if checks["margin up 2 quarters"] and cur["gm"] > 45:
        standalone, reason = True, "margin rising 2 quarters and above 45%"
    if cur["eps_beat"] > 30:
        standalone, reason = True, "EPS surprise above 30% (cyclical bottom signal)"

    return {"score": score, "max": 6, "checks": checks, "fund": cur,
            "fund_label": cur.get("label", ""), "standalone": standalone, "reason": reason}


def grade(momentum, value):
    if not momentum or not momentum["triggered"]:
        return "SKIP", "no momentum signal"
    if not value:
        return "WATCH", "momentum triggered, no fundamentals on file - add with --set"
    s, alt = value["score"], value["standalone"]
    if s >= 5 or (s >= 4 and alt):
        return "BUY_8%", f"conviction position ({s}/6)"
    if s >= 4 or (s >= 3 and alt):
        return "BUY_5%", f"standard position ({s}/6)"
    if s >= 3:
        return "BUY_3%", f"starter position ({s}/6)"
    if alt:
        return "BUY_3%", f"standalone condition: {value['reason']}"
    return "PASS", f"momentum without fundamentals to back it ({s}/6)"


def scan(ticker):
    try:
        candles = ohlc(ticker, "1y")
    except Exception as e:
        print(f"  {ticker:<6} ERROR: {e}")
        return None
    m = check_momentum(candles)
    v = check_value(ticker)
    verdict, reason = grade(m, v)
    if verdict == "SKIP":
        return {"ticker": ticker, "grade": verdict}
    print(f"  {ticker:<6} {m['close']:<8} 30d {m['change_30d']:+.1f}%  vol {m['vol_ratio']}x  -> {verdict}: {reason}")
    if v and verdict.startswith("BUY"):
        marks = "  ".join(f"[{'x' if ok else ' '}] {name}" for name, ok in v["checks"].items())
        f = v["fund"]
        print(f"         fundamentals ({v['fund_label']}): revenue {f['rev_yoy']:+.1f}% y/y, "
              f"margin {f['gm']:.1f}%, EPS surprise {f['eps_beat']:+.1f}%")
        print(f"         {marks}")
    return {"ticker": ticker, "grade": verdict, "reason": reason, "momentum": m, "value": v}


def set_quarter(argv):
    ticker, date, label = argv[0].upper(), argv[1], argv[2]
    vals = {}
    for key in ("rev-yoy", "gm", "eps-beat"):
        vals[key.replace("-", "_")] = float(argv[argv.index("--" + key) + 1])
    funds = load_json(FUND_FILE, {})
    funds.setdefault(ticker, {"quarters": {}})["quarters"][date] = {"label": label, **vals}
    save_json(FUND_FILE, funds)
    print(f"saved {ticker} {label}: {vals}")


def main():
    args = sys.argv[1:]
    if args and args[0] == "--set":
        set_quarter(args[1:])
        return
    if not os.path.exists(WATCHLIST_FILE):
        save_json(WATCHLIST_FILE, DEFAULT_WATCHLIST)
        print(f"created default watchlist: {WATCHLIST_FILE}")
    if args:
        tickers = [t.upper() for t in args]
    else:
        wl = load_json(WATCHLIST_FILE, {})
        tickers = [t for group in wl.values() for t in group]

    print(f"momentum + value screen, {len(tickers)} tickers")
    buys, watches = [], []
    for t in tickers:
        r = scan(t)
        if r and r["grade"].startswith("BUY"):
            buys.append(r)
        elif r and r["grade"] == "WATCH":
            watches.append(r)

    print("\n--- summary ---")
    print(f"buy signals: {len(buys)}" + "".join(
        f"\n  {b['grade']:<8} {b['ticker']:<6} {b['reason']}" for b in buys))
    if watches:
        print("missing fundamentals (--set): " + ", ".join(w["ticker"] for w in watches))
    if not buys and not watches:
        print("no signals today - that is also a result")


if __name__ == "__main__":
    main()
