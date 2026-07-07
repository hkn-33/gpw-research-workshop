# /gpw-audit — report quality gate before a report is trusted

Audit the report: $ARGUMENTS (a path under `reports/`; empty = the most recent report).

Wraps `tools/report_audit.py`. Purpose: a report with wrong numbers never becomes the basis of an investment decision.

## Flow (3 steps)

1. **Extract + 15% sample**:
   `python tools/report_audit.py extract --report <file>` → a JSON list of data points to verify.
2. **Verify** — preferably with the `gpw-auditor` agent: for EVERY sampled point, find the value in an independent source (biznesradar.pl / stockwatch.pl / the company's own report / stooq). The source must be DIFFERENT from the one the report was written from. Build the results JSON with `fetched_value` and `source` fields; leave unverifiable points as `fetched_value: null`.
3. **Verdict** (write the JSON to a temp file, then):
   `python tools/report_audit.py verdict --results @file.json [--tolerance 2]`

## Interpreting the verdict

- **PASS** — the report may drive decisions.
- **FAIL** — fix the flagged numbers IN THE REPORT (and check whether the error changes the conclusions: a wrong valuation input means recomputing the buy/sell ranges), then re-audit.
- **INCOMPLETE** — mark unverifiable points in the report as "(unverified)".

Append a footer to the audited report: `Audit: {date}, sample of N points, verdict {X}`. Respond in the user's language.
