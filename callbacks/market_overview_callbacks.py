import yfinance as yf
import pandas as pd
import plotly.express as px
from dash import Output, Input
from utils import get_vix_data

df_vix = get_vix_data()

def register_market_overview_callbacks(app):
    """Register callbacks for Market Overview page."""

    @app.callback(
        Output("market-overview-chart", "figure"),
        Input("interval-update", "n_intervals"),  # Auto-updates at intervals
    )
    def update_vix_chart(n):
        df = get_vix_data()
        
        if df.empty:
            return px.line(title="VIX - Market Volatility Index", template="plotly_dark")

        # Reset MultiIndex if necessary
        df.columns = df.columns.droplevel(0) if isinstance(df.columns, pd.MultiIndex) else df.columns
        df = df.rename(columns={"Close": "VIX"})  # Rename for clarity

        fig = px.line(
            df,
            x=df.index,
            y="VIX",  # Use the renamed column
            title="VIX - Market Volatility Index",
            labels={"VIX": "VIX Value", "index": "Date"},
            template="plotly_dark",
        )
        fig.update_layout(yaxis=dict(fixedrange=False))  # Enable zooming
        return fig