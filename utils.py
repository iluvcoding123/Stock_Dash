import yfinance as yf
import pandas as pd

def get_stock_data(ticker="SPY", timeframe="2y"):
    """
    Fetches stock data from Yahoo Finance for a given timeframe.
    """
    df = yf.download(ticker, period=timeframe, interval="1d", progress=False)

    if df.empty:
        return pd.DataFrame()  # Prevent crashes if no data

    return df

def get_vix_data(timeframe="6mo"):
    """
    Fetches VIX index data from Yahoo Finance and ensures proper formatting.
    """

    df = yf.download("^VIX", period=timeframe, interval="1d", progress=False)

    if df.empty:
        return pd.DataFrame()  # Prevent crashes if no data

    # Flatten MultiIndex columns if they exist
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]  # Extract only first level (Price)

    # Rename 'Close' to 'VIX' for clarity
    if "Close" in df.columns:
        df.rename(columns={"Close": "VIX"}, inplace=True)
    

    return df