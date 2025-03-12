import yfinance as yf
import pandas as pd

def get_stock_data(ticker="SPY", timeframe="1y"):
    """
    Fetches stock data from Yahoo Finance.
    """
    df = yf.download(ticker, period=timeframe, interval="1d", progress=False)

    if df.empty:
        return pd.DataFrame()  # Prevent crashes if no data

    return df