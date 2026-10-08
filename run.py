import sys
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as mticker

sys.path.insert(0, "src")

from data import load_prices, to_monthly, to_returns
from strategies import momentum, equal_weight
from backtest import run_backtest, equity_curve, first_invested_date
from metrics import summary
from universe import load_sp500_history, membership_table

if __name__ == "__main__":
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
    }

    # 4. Weights for each strategy
    all_weights = {name: f(monthly_prices) for name, f in strategies.items()}

    # 5. Common start: the latest first-invested date, so the comparison is fair
    start = max(first_invested_date(w) for w in all_weights.values())

    # 6. Backtest each strategy over the common period: one column of returns each
    strategy_returns = pd.DataFrame({
        name: run_backtest(w, monthly_returns).loc[start:]
        for name, w in all_weights.items()
    })

    # 7. Comparison table: one row per strategy
    table = pd.DataFrame({name: summary(strategy_returns[name])
                          for name in strategy_returns}).T

    formatted = table.copy()
    for col in ["Total return", "Annual return", "Volatility", "Max drawdown"]:
        formatted[col] = table[col].map("{:.1%}".format)
    formatted["Sharpe"] = table["Sharpe"].map("{:.2f}".format)

    print(f"Period: {strategy_returns.index[0].date()} to "
          f"{strategy_returns.index[-1].date()}\n")
    print(formatted.to_string())

    # 8. Equity curves, only for the plot
    equities = (1 + strategy_returns).cumprod()

    ax = equities.plot(logy=True, title="Value of £1 (point-in-time S&P 500)")
    ax.set_yticks([0.5, 1, 2, 4, 8])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"£{y:g}"))
    ax.yaxis.set_minor_formatter(mticker.NullFormatter())
    ax.axhline(1, color="grey", linewidth=0.8, linestyle="--")
    ax.set_ylabel("Value of £1 (log scale)")

    plt.savefig("reports/equity_curves_pit.png", dpi=150, bbox_inches="tight")
    plt.show()