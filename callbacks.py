from dash.dependencies import Input, Output
from utils import get_stock_data 
from pages.search import search_layout
from pages.heatmap import heatmap_layout
from pages.market_overview import market_overview_layout
import plotly.graph_objects as go
import pandas as pd
from charts import create_placeholder_chart

def register_callbacks(app):
    """Registers all Dash callbacks."""

    # Page Navigation Callback
    @app.callback(
        Output("page-content", "children"), 
        [Input("url", "pathname")]
    )
    def display_page(pathname):
        """Handles page navigation between Search, Heatmap, and Market Overview pages."""
        if pathname == "/heatmap":
            return heatmap_layout()
        elif pathname == "/market-overview":
            return market_overview_layout()
        return search_layout()  # Default to Search page

    # Search Page: Update Stock Chart Callback
    @app.callback(
        Output("candlestick-chart", "figure"),
        [Input("stock-input", "value"),
         Input("timeframe-dropdown", "value"),
         Input("sma-checkbox", "value")]
    )
    def update_chart(selected_stock, selected_timeframe, selected_smas):
        """Updates the candlestick chart based on the selected stock, timeframe, and SMA selection."""
        if not selected_stock:  # If no stock is entered
            return create_placeholder_chart()

        selected_stock = selected_stock.upper()  # Ensure uppercase

        df = get_stock_data(selected_stock, "2y")  # Always load 2 years of data

        # Flatten MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]

        # **Calculate SMAs before filtering**
        df["SMA50"] = df["Close"].rolling(window=50).mean()
        df["SMA100"] = df["Close"].rolling(window=100).mean()
        df["SMA200"] = df["Close"].rolling(window=200).mean()

        # Default to the last 6 months
        six_months_ago = df.index.max() - pd.DateOffset(months=6)
        df_filtered = df[df.index >= six_months_ago]

        # Generate Candlestick Chart
        fig = go.Figure(data=[
            go.Candlestick(
                x=df_filtered.index,
                open=df_filtered['Open'],
                high=df_filtered['High'],
                low=df_filtered['Low'],
                close=df_filtered['Close'],
                name="Candlesticks"
            )
        ])

        # Ensure `selected_smas` is a list to prevent errors
        selected_smas = selected_smas or []

        # **Check if SMA columns exist before adding them to the plot**
        if "SMA50" in selected_smas and "SMA50" in df_filtered.columns:
            fig.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered["SMA50"], mode="lines", name="50-day SMA", line=dict(color="blue")))

        if "SMA100" in selected_smas and "SMA100" in df_filtered.columns:
            fig.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered["SMA100"], mode="lines", name="100-day SMA", line=dict(color="orange")))

        if "SMA200" in selected_smas and "SMA200" in df_filtered.columns:
            fig.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered["SMA200"], mode="lines", name="200-day SMA", line=dict(color="red")))

        # Apply dark theme to chart
        fig.update_layout(
            title=f"{selected_stock} Price Chart ({selected_timeframe}, 1d)",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
            xaxis=dict(range=[six_months_ago, df.index.max()])  # Default view to last 6 months
        )

        return fig  