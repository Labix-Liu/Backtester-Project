def momentum_signal(monthly_prices, lookback = 12):
    return monthly_prices / monthly_prices.shift(lookback) - 1

def momentum_weights(signal, top_frac = 0.1):
    ranks = signal.rank(axis = 1, pct = True)
    winners = ranks > 1 - top_frac
    selected = winners.astype(float)
    weights = selected.div(selected.sum(axis = 1), axis = 0)
    weights = weights.fillna(0.0)
    return weights

def weights(monthly_prices, lookback = 12, top_frac = 0.1):
    signal = momentum_signal(monthly_prices, lookback)
    return momentum_weights(signal, top_frac)