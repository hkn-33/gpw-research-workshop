# /gpw-thesis — investment thesis tracker + drift detection

Handle the thesis for: $ARGUMENTS (a ticker — thesis update; or two report files — drift comparison).

## Mode 1: tracker (argument = ticker)

File: `reports/{TICKER}/{TICKER}-thesis.md` (maintained long-term). Structure:

```
## Thesis (max 5 sentences — the mirror test)
## Falsification conditions (concrete and measurable!)
   e.g. "operating margin below 8% for 2 consecutive quarters", "CEO X departs",
        "market share falls 3 quarters in a row" — NOT "sentiment deteriorates"
## Ranges: buy < X / hold X–Y / sell > Y
## Check log (date | event | thesis impact | action)
```

On every invocation: WebSearch for events since the last entry, test EVERY falsification condition, append a log entry. Verdict: VALID / WEAKENED (what to watch) / FALSIFIED — in which case say plainly "SELL, reason: ...".

**Discipline**: a falsified thesis means selling regardless of whether the position is up or down. The purchase price is psychologically irrelevant.

## Mode 2: drift (arguments = two files)

Compare two versions of a thesis/report and split the differences into three buckets:
1. **Fact changes** (new data — legitimate)
2. **Valuation changes** (new numbers on old facts — needs justification)
3. **Narrative changes** (same facts, different words — rationalization warning!)

Bucket 3 is the main warning signal: moving the goalposts to avoid selling. List every instance.

Write in the user's language.
