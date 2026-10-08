def weights(monthly_prices, members=None):
    available = monthly_prices.notna()
    if members is not None:
        available = available & members
    selected = available.astype(float)
    w = selected.div(selected.sum(axis=1), axis=0)
    return w.fillna(0.0)