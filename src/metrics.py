import pandas as pd
import numpy as np

def total_return(returns):
    return (1 + returns).prod() - 1

def annual_return(returns, periods_per_year=12):
    years = len(returns) / periods_per_year
    return (1 + total_return(returns)) ** (1 / years) - 1

def annual_volatility(returns, periods_per_year=12):
    return returns.std() * np.sqrt(periods_per_year)

def sharpe_ratio(returns, periods_per_year=12):
    return returns.mean() / returns.std() * np.sqrt(periods_per_year)

def max_drawdown(returns):
    equity = (1 + returns).cumprod()
    peak = equity.cummax().clip(lower=1)
    drawdown = 1 - equity / peak
    return drawdown.max()

def summary(returns, periods_per_year=12):
    return pd.Series({
        "Total return":  total_return(returns),
        "Annual return": annual_return(returns, periods_per_year),
        "Volatility":    annual_volatility(returns, periods_per_year),
        "Sharpe":        sharpe_ratio(returns, periods_per_year),
        "Max drawdown":  max_drawdown(returns),
    })