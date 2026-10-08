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

def sortino_ratio(returns, periods_per_year=12):
    downside = np.sqrt((returns.clip(upper=0) ** 2).mean())
    return returns.mean() / downside * np.sqrt(periods_per_year)

def calmar_ratio(returns, periods_per_year=12):
    return annual_return(returns, periods_per_year) / max_drawdown(returns)

def beta(returns, market):
    return returns.cov(market) / market.var()

def alpha(returns, market, periods_per_year=12):
    return (returns.mean() - beta(returns, market) * market.mean()) * periods_per_year

def summary(returns, market=None, periods_per_year=12):
    """All metrics for one strategy's period returns, as a pandas Series."""
    stats = {
        "Total return":  total_return(returns),
        "Annual return": annual_return(returns, periods_per_year),
        "Volatility":    annual_volatility(returns, periods_per_year),
        "Sharpe":        sharpe_ratio(returns, periods_per_year),
        "Sortino":       sortino_ratio(returns, periods_per_year),
        "Max drawdown":  max_drawdown(returns),
        "Calmar":        calmar_ratio(returns, periods_per_year),
    }
    if market is not None:
        stats["Beta"] = beta(returns, market)
        stats["Alpha"] = alpha(returns, market, periods_per_year)
    return pd.Series(stats)