from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
from utils import get_stock_data
from charts import create_placeholder_chart

def register_search_callbacks(app):
    """Registers callbacks for the Search page."""

    @app.callback(
        Output("candlestick-chart", "figure"),
        [Input("stock-input", "value"),
         Input("timeframe-dropdown", "value"),
         Input("sma-checkbox", "value")]
    )
    def update_chart(selected_stock, selected_timeframe, selected_smas):
        """Updates the candlestick chart based on the selected stock, timeframe, and SMA selection."""
        if not selected_stock:
            return create_placeholder_chart()

        selected_stock = selected_stock.upper()  # Ensure uppercase
        df = get_stock_data(selected_stock, "2y")  # Load full 2 years of data

        if df.empty:
            return create_placeholder_chart()

        # Flatten MultiIndex columns if necessary
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]

        # Calculate SMAs
        df["SMA50"] = df["Close"].rolling(window=50).mean()
        df["SMA100"] = df["Close"].rolling(window=100).mean()
        df["SMA200"] = df["Close"].rolling(window=200).mean()

        fig = go.Figure()

        # Determine x-axis range
        max_date = df.index.max()
        buffer_days = pd.DateOffset(days=1)

        if selected_timeframe == "1y":
            min_date = max_date - pd.DateOffset(years=1)
        elif selected_timeframe == "6mo":
            min_date = max_date - pd.DateOffset(months=6)
        elif selected_timeframe == "3mo":
            min_date = max_date - pd.DateOffset(months=3)
        elif selected_timeframe == "1mo":
            min_date = max_date - pd.DateOffset(months=1)
        else:
            min_date = max_date - pd.DateOffset(months=6)

        adjusted_max_date = max_date + buffer_days

        # Generate Candlestick Chart
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name="Candlesticks",
                showlegend=False
            )
        )

        # Ensure `selected_smas` is a list
        selected_smas = selected_smas or []

        # Add SMAs
        if "SMA50" in selected_smas and "SMA50" in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df["SMA50"], mode="lines", name="50-day SMA", line=dict(color="blue")))

        if "SMA100" in selected_smas and "SMA100" in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df["SMA100"], mode="lines", name="100-day SMA", line=dict(color="orange")))

        if "SMA200" in selected_smas and "SMA200" in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df["SMA200"], mode="lines", name="200-day SMA", line=dict(color="red")))

        # Filter data for selected timeframe
        df_filtered = df.loc[min_date:adjusted_max_date]

        # Calculate min/max for visible y-axis
        y_min = df_filtered[['Low', 'SMA50', 'SMA100', 'SMA200']].min().min()
        y_max = df_filtered[['High', 'SMA50', 'SMA100', 'SMA200']].max().max()

        # Update Layout
        fig.update_layout(
            title=f"{selected_stock} Price Chart ({selected_timeframe}, 1d)",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
            xaxis=dict(range=[min_date, adjusted_max_date]),
            yaxis=dict(range=[y_min * 0.98, y_max * 1.02], fixedrange=False)
        )

        return fig