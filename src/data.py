# This is used for downloading and loading data from yahoo finances. 

from datetime import datetime
import yfinance as yf
import pandas as pd
from pathlib import Path
from universe import load_sp500_history, all_tickers
import time   # at the top of the file

def download_prices(tickers, start_date, end_date, path="data/prices.csv"):
    raw = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        interval="1d",
        auto_adjust=True,
        progress=False
    )
    prices = raw["Close"] # no peeking
    prices.to_csv(path)
    return prices

def fill_missing(prices, start_date, end_date, batch_size=50, pause=5):
    """Re-download tickers whose columns are entirely empty, in small batches."""
    missing = list(prices.columns[prices.isna().all()])
    print(f"Retrying {len(missing)} tickers")

    for i in range(0, len(missing), batch_size):
        batch = missing[i:i + batch_size]
        raw = yf.download(batch, start=start_date, end=end_date,
                          auto_adjust=True, progress=False)
        prices.update(raw["Close"])
        time.sleep(pause)

    still_missing = prices.columns[prices.isna().all()]
    print(f"Recovered {len(missing) - len(still_missing)}, "
          f"still missing {len(still_missing)}")
    return prices

def load_prices(path="data/prices.csv"):
    return pd.read_csv(path, index_col=0, parse_dates=True)

def to_monthly(prices):
    return prices.resample("ME").last()

def to_returns(prices):
    return prices.pct_change(fill_method=None)

if __name__ == "__main__":
    start_date = datetime(year=2005, month=1, day=1)
    end_date = datetime(year=2026, month=1, day=1)

    tickers = all_tickers(load_sp500_history())
    #prices = download_prices(tickers, start_date, end_date, path="data/prices_sp500_hist.csv")
    prices = load_prices("data/prices_sp500_hist.csv")

    empty = prices.columns[prices.isna().all()]
    print(f"Saved {prices.shape[1]} tickers, {prices.shape[0]} days")
    print(f"{len(empty)} tickers have no price data")

    prices = load_prices("data/prices_sp500_hist.csv")
    prices = fill_missing(prices, start_date, end_date)
    prices.to_csv("data/prices_sp500_hist.csv")
