def run_backtest(weights, returns, cost = 0.0):
    held = weights.shift(1)
    portfolio_returns = (held * returns).sum(axis = 1)
    trading_costs = cost * turnover(weights, returns).shift(1).fillna(0.0)
    return portfolio_returns - trading_costs

def equity_curve(portfolio_returns):
    return (portfolio_returns + 1).cumprod()

def first_invested_date(weights):
    invested = weights.shift(1).sum(axis=1) > 0
    return invested.idxmax()

def turnover(weights, returns):
    previous = weights.shift(1).fillna(0.0)
    grown = previous * (1 + returns.fillna(0.0))
    cash = 1 - previous.sum(axis=1)
    total = grown.sum(axis=1) + cash
    drifted = grown.div(total, axis=0)
    return (weights - drifted).abs().sum(axis=1)