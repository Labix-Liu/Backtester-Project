def weights(monthly_prices, members=None, lookback=1, bottom_frac=0.1):
    signal = monthly_prices / monthly_prices.shift(lookback) - 1
    if members is not None:
        signal = signal.where(members)
    ranks = signal.rank(axis = 1, pct = True)
    losers = ranks <= bottom_frac
    selected = losers.astype(float)
    w = selected.div(selected.sum(axis = 1), axis = 0)
    w = w.fillna(0.0)
    return w