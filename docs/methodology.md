# Methodology

The framework synthesizes four value-investing masters into one process. The design owes its structure to the [ai-berkshire](https://github.com/xbtlin/ai-berkshire) project (MIT); this document is an independent English formulation adapted to the Warsaw Stock Exchange.

## The four lenses

| Lens | Master | Core question |
|------|--------|---------------|
| Business essence | Duan Yongping | Is this "the right business"? What does it really earn on, and would customers miss it? |
| Financials & valuation | Warren Buffett | Do the numbers confirm the moat, and is the price low enough to leave a margin of safety? |
| Inversion & risk | Charlie Munger | How does this company die? Why are smart people on the other side of the trade? |
| 10-year certainty | Li Lu | Will this business be bigger and healthier in 10 years — with enough certainty to act on? |

The lenses are designed to conflict. Buffett saying "genuinely cheap" while Li Lu says "uncertain in 10 years" is not a bug — it is the true state of most investment decisions, and surfacing it prevents blind spots. Never average the four ratings into a bland consensus; report the tensions.

## Anti-bias mechanisms

- **Researchability rating (A/B/C).** Data abundance is not certainty. A-rated companies (heavy coverage) tempt the model into echoing consensus — hunt for non-consensus angles. C-rated companies (scarce data) tempt it into false completeness — switch to first principles: who pays, why do they return, can a funded competitor copy it.
- **Facts vs opinions.** Facts carry sources and dates; opinions carry the label "judgment". Missing data is written as "no data", never filled with plausible guesses.
- **Two-source rule.** Decision-critical numbers (market cap, profit, debt) need two independent sources; deviations above 2% get flagged. Market cap is always re-derived by hand: price times share count.
- **No mental math.** Every calculation runs through `tools/financial_rigor.py` (exact decimal arithmetic), because a misplaced decimal in a P/E ratio changes the conclusion.
- **Sampled report audit.** Before a report ending in a recommendation is trusted, 15% of its numeric claims are re-verified against independent sources (`tools/report_audit.py`). Fail = fix and re-audit.
- **Forced verdicts.** Every analysis ends with tiered price ranges (aggressive / moderate / conservative). "On one hand, on the other hand" is banned as a conclusion.
- **The mirror test.** If the thesis does not fit in five sentences, the answer is: don't buy.

## Quality screen: 7 criteria and 3 exemptions

Seven hard criteria eliminate companies that cannot be first-rate (10y avg ROE < 8%, negative 5y cumulative FCF, interest coverage < 2x, gross margin < 15%, OCF/net profit < 0.7, net margin < 5%, share dilution > 20% in 5 years). The bias is deliberate: better to let a weak company through than to kill a great one. Three exemptions protect atypical excellence:

- **A — strategic investment phase** (waives ROE): listed under 10 years, gross margin above 30%, operating cash flow positive for 2 years. The model works; ROE is low only because the company is still investing. (Classic case: Meituan.)
- **B — deliberately suppressed profitability** (waives net margin): gross margin above 30% and net margin recovering above 5% or clearly trending up. Ability to earn exists; low profit is a reinvestment choice. (Classic case: Amazon.)
- **C — high-turnover thin-margin model** (waives both margin tests): ROE above 20%, OCF/net profit above 1.0, and a membership/platform/turnover business model where profit does not live in product markup. (Classic case: Costco.)

## Selection funnel

Whole market → rough cut (hard filters, every rejection with a stated reason) → ≤10 detailed profiles → final 3 chosen for **portfolio complementarity** (high certainty + moderate upside + high convexity), not by ranking score. A mandatory "future IPO candidates" list guards against the listed-only blind spot.

## Post-purchase discipline

Every purchase creates a thesis file with **measurable falsification conditions** ("operating margin below 8% for two consecutive quarters", not "sentiment worsens"). Reviews test the conditions, not feelings. A falsified thesis means selling regardless of the position's P&L — the purchase price is psychologically irrelevant. Comparing two thesis versions splits changes into facts / valuation / narrative; narrative-only changes are the signature of moving the goalposts.

## Warsaw Stock Exchange specifics

- **State-owned companies** (Orlen, PKO BP, PZU, KGHM, PGE, JSW...) are a separate risk class: post-election board purges, sector taxes, non-commercial objectives. Their political risk is mutually correlated — cap their combined portfolio weight.
- **Liquidity**: outside WIG20/mWIG40, check turnover before trusting any signal; the spread eats the edge.
- **Dividends**: 19% withholding tax; record date and payment date differ.
- **Primary sources**: ESPI/EBI filings via infostrefa.com, then biznesradar.pl, stockwatch.pl, bankier.pl, strefainwestorow.pl.
