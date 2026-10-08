def run_backtest(weights, returns):
    held = weights.shift(1)
    portfolio_returns = (held * returns).sum(axis = 1)
    return portfolio_returns

def equity_curve(portfolio_returns):
    return (portfolio_returns + 1).cumprod()

def first_invested_date(weights):
    invested = weights.shift(1).sum(axis=1) > 0
    return invested.idxmax()