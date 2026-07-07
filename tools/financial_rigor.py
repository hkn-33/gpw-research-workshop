"""Exact financial arithmetic for research reports.

LLMs make arithmetic mistakes; a misplaced decimal in a P/E ratio can sink an
investment decision. Every calculation here uses decimal.Decimal, never float.

Commands:
  python tools/financial_rigor.py calc --expr "134.68 * 1.16e9"
  python tools/financial_rigor.py verify-market-cap --price 134.68 --shares 1.16e9 --reported 156e9 --currency PLN
  python tools/financial_rigor.py verify-valuation --price 121 --eps 10.5 --bvps 22.4 --dividend 4.1
  python tools/financial_rigor.py three-scenario --price 121 --eps 10.5 --growth 20 10 0 --pe 15 11 8
  python tools/financial_rigor.py cross-validate --field revenue --values "{\"annual report\": 1720, \"biznesradar\": 1715}"
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import argparse
import json
from decimal import Decimal, getcontext

getcontext().prec = 28


def D(x):
    return Decimal(str(x))


def human(d):
    v = float(d)
    for cut, suffix in ((1e12, "T"), (1e9, "B"), (1e6, "M")):
        if abs(v) >= cut:
            return f"{v / cut:.2f}{suffix}"
    return f"{v:,.2f}"


def calc(args):
    allowed = set("0123456789.+-*/()eE ")
    if not set(args.expr) <= allowed:
        sys.exit(f"expression contains unsupported characters: {args.expr}")
    result = eval(args.expr, {"__builtins__": {}}, {})  # input is whitelisted above
    exact = D(result)
    print(f"expression: {args.expr}")
    print(f"result:     {human(exact)}")
    print(f"exact:      {exact}")


def verify_market_cap(args):
    computed = D(args.price) * D(args.shares)
    reported = D(args.reported)
    dev = abs(computed - reported) / reported * 100
    print(f"price x shares = {human(computed)} {args.currency}")
    print(f"reported       = {human(reported)} {args.currency}")
    print(f"deviation      = {dev:.2f}%")
    if dev > D(args.tolerance):
        print(f"FAIL: deviation above {args.tolerance}% - check share count, currency and scale (m vs bn)")
        sys.exit(1)
    print("OK: market cap verified")


def verify_valuation(args):
    p = D(args.price)
    rows = []
    if args.eps:
        rows.append(("P/E", p / D(args.eps), "x"))
    if args.bvps:
        rows.append(("P/B", p / D(args.bvps), "x"))
    if args.fcf_per_share:
        rows.append(("P/FCF", p / D(args.fcf_per_share), "x"))
        rows.append(("FCF yield", D(args.fcf_per_share) / p * 100, "%"))
    if args.dividend:
        rows.append(("dividend yield", D(args.dividend) / p * 100, "%"))
    for name, val, unit in rows:
        print(f"{name:<15} {val:.2f}{unit}")


def three_scenario(args):
    p = D(args.price)
    eps = D(args.eps)
    years = args.years
    print(f"current price {p}, EPS {eps}, horizon {years}y")
    print(f"{'scenario':<10}{'growth/yr':>10}{'target PE':>10}{'target EPS':>12}{'target':>10}{'upside':>9}")
    for name, g, pe in zip(("bull", "base", "bear"), args.growth, args.pe):
        eps_t = eps * (1 + D(g) / 100) ** years
        target = eps_t * D(pe)
        upside = (target / p - 1) * 100
        print(f"{name:<10}{g + '%':>10}{pe + 'x':>10}{eps_t:>12.2f}{target:>10.2f}{upside:>+8.1f}%")


def cross_validate(args):
    nums = {k: D(v) for k, v in json.loads(args.values).items()}
    lo, hi = min(nums.values()), max(nums.values())
    spread = (hi - lo) / hi * 100 if hi else D(0)
    for src, v in nums.items():
        print(f"{src:<25} {human(v)}")
    print(f"spread: {spread:.2f}%")
    if spread > D(args.tolerance):
        print(f"FAIL: sources differ by more than {args.tolerance}% - reconcile before using")
        sys.exit(1)
    print("OK: sources agree")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("calc")
    c.add_argument("--expr", required=True)
    c.set_defaults(fn=calc)

    m = sub.add_parser("verify-market-cap")
    m.add_argument("--price", required=True)
    m.add_argument("--shares", required=True)
    m.add_argument("--reported", required=True)
    m.add_argument("--currency", default="PLN")
    m.add_argument("--tolerance", default="2")
    m.set_defaults(fn=verify_market_cap)

    v = sub.add_parser("verify-valuation")
    v.add_argument("--price", required=True)
    v.add_argument("--eps")
    v.add_argument("--bvps")
    v.add_argument("--fcf-per-share", dest="fcf_per_share")
    v.add_argument("--dividend")
    v.set_defaults(fn=verify_valuation)

    t = sub.add_parser("three-scenario")
    t.add_argument("--price", required=True)
    t.add_argument("--eps", required=True)
    t.add_argument("--growth", nargs=3, required=True, help="annual growth in %% for bull base bear, e.g. 20 10 0")
    t.add_argument("--pe", nargs=3, required=True, help="target P/E for bull base bear")
    t.add_argument("--years", type=int, default=3)
    t.set_defaults(fn=three_scenario)

    x = sub.add_parser("cross-validate")
    x.add_argument("--field", default="")
    x.add_argument("--values", required=True, help='JSON: {"source": value, ...}')
    x.add_argument("--tolerance", default="2")
    x.set_defaults(fn=cross_validate)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
