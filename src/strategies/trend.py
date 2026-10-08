def weights(monthly_prices, members=None, window=10):

    # 1. The moving average for every stock and month
    average = monthly_prices.rolling(window).mean()

    # 2. Eligible: has a moving average (and is a member, if members is given)
    eligible = average.notna()
    if members is not None:
        eligible = eligible & members

    # 3. In an uptrend: price above its average, and eligible
    uptrend = ((monthly_prices > average) & eligible).astype(float)

    # 4. Each uptrending stock gets 1 / (number of eligible stocks); the rest is cash
    w = uptrend.div(eligible.sum(axis = 1), axis = 0)
    return w.fillna(0.0)