import sys
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, "src")

from data import load_prices, to_monthly, to_returns
from strategies import momentum
from backtest import run_backtest, equity_curve, first_invested_date
from metrics import summary

if __name__ == "__main__":
    # 1. Data
    monthly_prices = to_monthly(load_prices())
    monthly_returns = to_returns(monthly_prices)

    # 2. Strategies to compare: name -> function (prices in, weights out)
    strategies = {
        "Momentum 12m": lambda p: momentum.weights(p, lookback=12),
        "Momentum 6m":  lambda p: momentum.weights(p, lookback=6),
    }

    # 3. Weights for each strategy
    all_weights = {name: f(monthly_prices) for name, f in strategies.items()}

    # 4. Common start: the latest first-invested date, so the comparison is fair
    start = max(first_invested_date(w) for w in all_weights.values())

    # 5. Backtest each strategy over the common period
    equities = pd.DataFrame({
        name: equity_curve(run_backtest(w, monthly_returns).loc[start:])
        for name, w in all_weights.items()
    })

    # 6. Comparison table: one row per strategy
    table = pd.DataFrame({name: summary(equities[name]) for name in equities}).T
    print(f"Period: {equities.index[0].date()} to {equities.index[-1].date()}\n")
    print(table.to_string(float_format="{:.1%}".format))

    # 7. All equity curves on one chart
    equities.plot(logy=True, title="Value of £1")
    plt.savefig("reports/equity_curves.png", dpi=150, bbox_inches="tight")
    plt.show()