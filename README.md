## Limitations

**1. Incomplete price data (residual survivorship bias).**
Of 961 tickers that were index members at some point in 2005–2025, Yahoo
Finance had no data for 309, mostly companies that went bankrupt, were
acquired, or changed ticker. Coverage of each month's members ranges from 53%
to 98% (average 76%) and rises over time, so the early years, including the
2008 crisis, are the least reliable. Because the missing companies are
disproportionately failures, which an equal-weight portfolio would hold but a
momentum strategy usually would not, the benchmark is likely somewhat
flattered relative to momentum. A few missing tickers (e.g. BK, EA) may be
recoverable and were not investigated further.

![Coverage](reports/coverage.png)

**2. Membership data quality.** The membership reconstruction is
community-maintained and may contain errors, particularly in earlier years.

**3. Recycled ticker symbols.** Yahoo returns prices for whichever company
holds a ticker today; if a symbol was reused, prices may be misattributed.
Not checked systematically.

**4. Execution assumptions.**
- No transaction costs, bid-ask spreads, or market impact.
- Trades are assumed to execute at the same month-end close used to compute
  the signal.
- If a held stock's price data stops mid-period, its missing return is
  effectively treated as 0%.

**5. Strategy scope.** Long-only and equally weighted. Academic momentum
studies typically use long-short portfolios across thousands of stocks,
including small companies, so results are not directly comparable.

**6. Statistical evaluation.** Only total and annual return are reported so
far; risk measures and significance tests are not yet included. Two lookbacks
were tested, so the better one may look good partly by chance.
