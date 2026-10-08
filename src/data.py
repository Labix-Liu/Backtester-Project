# This is used for downloading and loading data from yahoo finances. 

from datetime import datetime
import yfinance as yf
import pandas as pd
from pathlib import Path

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

def download_prices(tickers, start_date, end_date):
    raw = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        interval="1d",
        auto_adjust=True,
        progress=False
    )
    prices = raw["Close"] # no peeking
    prices.to_csv("data/prices.csv")
    return prices

def load_prices(path="data/prices.csv"):
    return pd.read_csv(path, index_col=0, parse_dates=True)

def to_monthly(prices):
    return prices.resample("ME").last()

def to_returns(prices):
    return prices.pct_change(fill_method=None)

if __name__ == "__main__":
    sp500 = get_sp500_tickers()
    universe = sample_universe(sp500, 50, 37)
    tickers = universe["Symbol"].to_list()

    start_date = datetime(year=2005, month=1, day=1)
    end_date = datetime(year=2026, month=1, day=1)

    prices = download_prices(tickers, start_date, end_date)
    monthly_prices = to_monthly(prices)
    monthly_returns = to_returns(monthly_prices)
