This is a python backtester for equality stratgies. 

Data: 
The stock prices downloaded from Yahoo Finance, of the companies that belonged to S&P between 2005 to 2025. 
About 24% of historical members no longer has stock data in yFinance. 

Strategies:
- Momentum: Ranks the stocks buy how much their market value increased in the last 12 / 6 months and buy the top 10%. The portfolio is updated every month. 
- Reversal: Buys the bottom 10% instead, with the hopes of it bouncing back. Also updated every month. 
- Equal Weights: Take every stock that was in the S&P that month and put all the money equally in each stock. 
- Trend: Computes the moving average in a 10 month window. Hold the stocks whose average today is higher than the moving average, and vice versa. 

Metrics: 
- Total Return: How much £1 grew in the entire period. 
- Annual Return: The constant yearly growth rate. 
- Volatility: The standard deviation of monthly returns, annualised. 
- Maximum drawdown: The most amount of money lost in the entire period. 
- Sharpe ratio: Return per unit of volatility. 
- Sortino ratio: Return per unit of downside volatility. 
- Calmar ratio: Annaual return per unit of worst loss. 
- Alpha: Then return left over after accounting for market exposure. Note that alpha is measured against the equal weight strategy instead of the conventional S&P500 index. 
- Beta: How much the strategy moves when the market moves. 
- Turnover: How much the strategy changes. 

Results: 
Period: 2006-02-28 to 2025-12-31
Costs: 10 bp per unit of turnover

| Strategy | Total return | Annual return | Volatility | Sharpe | Sortino | Max drawdown | Calmar | Beta | Alpha | Turnover (annual) |
|---|---|---|---|---|---|---|---|---|---|---|
| Momentum 12m | 343.9% | 7.8% | 17.5% | 0.52 | 0.77 | 54.3% | 0.14 | 0.83 | -0.8% | 723% |
| Momentum 6m | 430.3% | 8.7% | 17.6% | 0.57 | 0.85 | 53.5% | 0.16 | 0.85 | -0.1% | 963% |
| Equal weight | 673.2% | 10.8% | 17.1% | 0.69 | 1.05 | 53.4% | 0.20 | 1.00 | 0.0% | 70% |
| Reversal 1m | 259.3% | 6.6% | 25.5% | 0.38 | 0.56 | 73.2% | 0.09 | 1.36 | -6.3% | 2,107% |
| Trend 10m | 264.7% | 6.7% | 8.2% | 0.84 | 1.36 | 15.6% | 0.43 | 0.38 | 2.4% | 222% |

Interpretation: 
- No strategy beat the equal-weight benchmark on return. This is expected for simple and well known rules applied to large US stocks. 
- Momentum suffered because of its low market exposure, namely its beta and alpha is low. The gap between Momentum and Equal Weights was amplified after the 2008 financial crisis. 
- Reversal did not earn much because of its turnover. It also has a higher max drawdown and volatility. 
- Trend folllowing has low volatility and low max drawdown, hence the high Sharpe, Sortino and Calmar ratios. 

