import pandas as pd

def total_return(equity):
    return equity.iloc[-1] - 1

def annual_return(equity, periods_per_year = 12):
    years = len(equity) / periods_per_year
    return equity.iloc[-1] ** (1/years) - 1

def summary(equity, periods_per_year=12):
    return pd.Series({
        "Total return":  total_return(equity),
        "Annual return": annual_return(equity, periods_per_year),
    })