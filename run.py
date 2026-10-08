import sys
sys.path.insert(0, "src")

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

from data import load_prices, to_monthly, to_returns
from universe import load_sp500_history, membership_table
from strategies import momentum, equal_weight, reversal, trend
from backtest import run_backtest, first_invested_date, turnover
from metrics import summary

if __name__ == "__main__":
    COST = 0.001   # trading cost per unit of turnover: 10 basis points

    # 1. Data: prices for all historical S&P 500 members we could download
    monthly_prices = to_monthly(load_prices("data/prices_sp500_hist.csv"))
    monthly_returns = to_returns(monthly_prices)

    # 2. Point-in-time membership: who was in the index each month
    hist = load_sp500_history()
    members = membership_table(hist, monthly_prices.index, monthly_prices.columns)

    # 3. Strategies to compare: name -> function (prices in, weights out)
    strategies = {
        "Momentum 12m": lambda p: momentum.weights(p, members=members, lookback=12),
        "Momentum 6m":  lambda p: momentum.weights(p, members=members, lookback=6),
        "Equal weight": lambda p: equal_weight.weights(p, members=members),
        "Reversal 1m":  lambda p: reversal.weights(p, members=members),
        "Trend 10m": lambda p: trend.weights(p, members = members)
    }

    # 4. Weights for each strategy
    all_weights = {name: f(monthly_prices) for name, f in strategies.items()}

    # 5. Common start: the latest first-invested date, so the comparison is fair
    start = max(first_invested_date(w) for w in all_weights.values())

    # 6. Backtest each strategy over the common period, net of costs
    strategy_returns = pd.DataFrame({
        name: run_backtest(w, monthly_returns, cost=COST).loc[start:]
        for name, w in all_weights.items()
    })

    # 7. Comparison table: one row per strategy
    market = strategy_returns["Equal weight"]
    table = pd.DataFrame({name: summary(strategy_returns[name], market=market)
                          for name in strategy_returns}).T
    table["Turnover"] = pd.Series({
        name: turnover(w, monthly_returns).loc[start:].mean() * 12
        for name, w in all_weights.items()
    })

    formatted = table.copy()
    for col in ["Total return", "Annual return", "Volatility", "Max drawdown",
                "Turnover", "Alpha"]:
        formatted[col] = table[col].map("{:.1%}".format)
    for col in ["Sharpe", "Sortino", "Calmar", "Beta"]:
        formatted[col] = table[col].map("{:.2f}".format)

    print(f"Period: {strategy_returns.index[0].date()} to "
          f"{strategy_returns.index[-1].date()}")
    print(f"Costs: {COST * 10000:.0f} bp per unit of turnover\n")
    print(formatted.to_string())

    # 8. Equity curves, only for the plot
    equities = (1 + strategy_returns).cumprod()
    Path("reports").mkdir(exist_ok=True)

    ax = equities.plot(logy=True, title=f"Value of £1 (point-in-time S&P 500, "
                                        f"{COST * 10000:.0f} bp costs)")
    ax.set_yticks([0.25, 0.5, 1, 2, 4, 8])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"£{y:g}"))
    ax.yaxis.set_minor_formatter(mticker.NullFormatter())
    ax.axhline(1, color="grey", linewidth=0.8, linestyle="--")
    ax.set_ylabel("Value of £1 (log scale)")

    plt.savefig("reports/equity_curves_pit.png", dpi=150, bbox_inches="tight")
    plt.show()