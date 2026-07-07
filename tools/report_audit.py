"""Spot-check the numbers in a research report before it is trusted.

Samples 15% of the numeric data points found in a markdown report (minimum 5).
The agent then verifies each sampled value against an independent source and
feeds the results back for a verdict: PASS, FAIL or INCOMPLETE.

Step 1 - extract data points and draw the sample:
  python tools/report_audit.py extract --report reports/XTB/XTB-analysis-20260707.md
Step 2 - the agent looks each value up in an independent source
Step 3 - verdict (default tolerance 2%):
  python tools/report_audit.py verdict --results @checked.json

Handles both English and Polish number formats: "3.4bn PLN", "1,239 million",
"3,4 mld zl", "12.5%", "C/Z 11x", "145 zl".
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import argparse
import json
import re
from random import Random

_NUM = r"[-+]?\d[\d\s.,]*"
_PATTERNS = [
    (rf"({_NUM})\s*%", "%"),
    (rf"({_NUM})\s*(bn|billion|mld)\b", "bn"),
    (rf"({_NUM})\s*(m|million|mln)\b", "m"),
    (rf"({_NUM})\s*[x×]", "x"),
    (rf"({_NUM})\s*(zł|PLN)\b", "PLN"),
    (rf"PLN\s*({_NUM})", "PLN"),
]
_LABEL = re.compile(
    r"(?P<label>[\w /ĄĆĘŁŃÓŚŹŻ"
    r"ąćęłńóśźż()%-]{3,40}?)"
    r"[:|]\s*[~ca.]*\s*(?P<rest>.+)"
)


def parse_num(s):
    s = s.strip().replace(" ", "").replace("\xa0", "")
    # handle both 1,234.5 and 1.234,5 conventions
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".") if s.count(",") == 1 else s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def extract(path, sample_pct=15, seed=42):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    points = []
    for ln, line in enumerate(lines, 1):
        if line.lstrip().startswith(("```", "<!--")):
            continue
        for pattern, unit in _PATTERNS:
            for m in re.finditer(pattern, line):
                val = parse_num(m.group(1))
                if val is None:
                    continue
                ctx = line.strip()
                label = ctx[:60]
                lm = _LABEL.match(ctx)
                if lm:
                    label = lm.group("label").strip()
                points.append({"line": ln, "label": label, "report_value": val,
                               "unit": unit, "context": ctx[:120]})
    seen, unique = set(), []
    for p in points:
        key = (p["line"], p["report_value"], p["unit"])
        if key not in seen:
            seen.add(key)
            unique.append(p)
    n = max(5, round(len(unique) * sample_pct / 100)) if unique else 0
    sample = Random(seed).sample(unique, min(n, len(unique)))
    print(f"data points found: {len(unique)}; sampled for verification ({sample_pct}%): {len(sample)}\n")
    print(json.dumps(sample, ensure_ascii=False, indent=2))
    print('\nFor each point: look the value up in an independent source, add '
          '"fetched_value" and "source" fields, then run the verdict step.')


def verdict(results, tol_pct=2.0):
    bad, unchecked = [], []
    for r in results:
        fetched = r.get("fetched_value")
        if fetched is None:
            unchecked.append(r)
            continue
        reported = r["report_value"]
        dev = abs(fetched - reported) / abs(fetched) * 100 if fetched else (0 if reported == 0 else 999)
        r["deviation_pct"] = round(dev, 2)
        if dev > tol_pct:
            bad.append(r)
    print(f"checked: {len(results) - len(unchecked)}/{len(results)}, tolerance {tol_pct}%")
    for r in bad:
        print(f"  MISMATCH {r.get('label', '?')}: report {r['report_value']} vs source "
              f"{r['fetched_value']} ({r.get('source', '?')}), deviation {r['deviation_pct']}%")
    for r in unchecked:
        print(f"  UNCHECKED {r.get('label', '?')}")
    if bad:
        print("\nVERDICT: FAIL - correct the numbers above and re-run the audit")
        sys.exit(1)
    if unchecked:
        print("\nVERDICT: INCOMPLETE - resolve the unchecked points")
        sys.exit(2)
    print("\nVERDICT: PASS")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract")
    e.add_argument("--report", required=True)
    e.add_argument("--percent", type=float, default=15)
    e.add_argument("--seed", type=int, default=42)
    v = sub.add_parser("verdict")
    v.add_argument("--results", required=True, help="JSON string or @file.json")
    v.add_argument("--tolerance", type=float, default=2.0)
    a = ap.parse_args()
    if a.cmd == "extract":
        extract(a.report, a.percent, a.seed)
    else:
        raw = a.results
        if raw.startswith("@"):
            with open(raw[1:], encoding="utf-8") as f:
                raw = f.read()
        verdict(json.loads(raw), a.tolerance)


if __name__ == "__main__":
    main()
