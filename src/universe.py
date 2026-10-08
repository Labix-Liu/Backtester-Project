from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# retrieves the current companies in S&P500 (as of 8/10/2026)
# sampling from the current list introduces a bias: 
# these are the companies that survived over the years
def get_sp500_tickers(path="data/sp500_tickers.csv", refresh=False):
    path = Path(path)
    if path.exists() and not refresh:
        return pd.read_csv(path)
    
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url, storage_options={"User-Agent": "Mozilla/5.0"})
    sp500 = tables[0]
    sp500["Symbol"] = sp500["Symbol"].str.replace(".", "-", regex = False)
    sp500.to_csv(path, index=False)
    return sp500

# samples 50 random companies for first test
def sample_universe(sp500, n, seed):
    universe = sp500.sample(n, random_state = seed, axis = 0)
    universe.to_csv("data/universe.csv", index = True)
    return universe

def load_sp500_history(path="data/sp500_historical.csv", start="2005-01-01", end="2025-12-31"):
    hist = pd.read_csv(path, index_col="date", parse_dates=True)
    hist = hist.loc[start:end]
    hist["tickers"] = (hist["tickers"]
                       .str.replace(".", "-", regex=False)
                       .str.split(","))
    return hist

def all_tickers(hist):
    return sorted(hist["tickers"].explode().unique())

def membership_table(hist, dates, tickers):
    exploded = hist["tickers"].explode()
    members = pd.crosstab(exploded.index, exploded).astype(bool)
    members = members.reindex(dates, method="ffill")
    members = members.reindex(columns=tickers, fill_value=False)
    return members.fillna(False)

if __name__ == "__main__":
    import sys; sys.path.insert(0, "src")
    from data import load_prices, to_monthly

    # 1. Load the membership history
    hist = load_sp500_history()
    print(hist.shape)
    print(hist.index[0], hist.index[-1])
    print(len(hist["tickers"].iloc[0]))

    # 2. Every company that was ever a member
    tickers = all_tickers(hist)
    print(len(tickers))
    print(tickers[:20])

    # 3. Membership table on month-end dates, for all historical members
    monthly_prices = to_monthly(load_prices("data/prices_sp500_hist.csv"))
    members = membership_table(hist, monthly_prices.index, tickers)

    has_price = monthly_prices.reindex(columns=tickers).notna()
    coverage = (members & has_price).sum(axis=1) / members.sum(axis=1)

    print(coverage.describe())
    coverage.plot(title="Share of S&P 500 members with price data", ylim=(0, 1))
    plt.show()