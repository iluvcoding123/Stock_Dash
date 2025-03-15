from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import yfinance as yf

# Fetch real-time sector performance
def get_sector_performance():
    sector_tickers = {
        "Technology": "XLK",
        "Healthcare": "XLV",
        "Finance": "XLF",
        "Energy": "XLE",
        "Consumer Goods": "XLP",
        "Industrials": "XLI",
        "Real Estate": "XLRE",
        "Utilities": "XLU"
    }

    metrics = ["1D Change", "5D Change", "1M Change"]
    df_list = []  # Use a list instead of direct concatenation

    for sector, ticker in sector_tickers.items():
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")  # Get past month of data

        if hist.empty:
            continue

        last_close = hist["Close"].iloc[-1]
        prev_1d = hist["Close"].iloc[-2] if len(hist) > 1 else last_close
        prev_5d = hist["Close"].iloc[-6] if len(hist) > 5 else last_close
        prev_1m = hist["Close"].iloc[0]

        sector_data = pd.DataFrame({
            "Sector": [sector],
            "1D Change": [(last_close - prev_1d) / prev_1d],
            "5D Change": [(last_close - prev_5d) / prev_5d],
            "1M Change": [(last_close - prev_1m) / prev_1m]
        })
        
        # Ensure that sector_data is valid before appending
        if not sector_data.isna().all().all():
            df_list.append(sector_data)


    # Concatenate only if there's valid data
    if df_list:
        df = pd.concat(df_list, ignore_index=True)
    else:
        df = pd.DataFrame(columns=["Sector"] + metrics)  # Return an empty but structured DataFrame

    return df

def register_heatmap_callbacks(app):
    """Registers callbacks for the heatmap page."""

    @app.callback(
        Output("sector-heatmap", "figure"),
        Input("url", "pathname")  # Trigger update when the page loads
    )
    def update_heatmap(_):
        """Generates the sector performance heatmap with real data."""
        df = get_sector_performance()

        fig = px.imshow(
            df.set_index("Sector").T.values,  # Transpose so sectors are x-axis
            x=df["Sector"],  # X-axis: Sectors
            y=["1D Change", "5D Change", "1M Change"],  # Y-axis: Metrics
            color_continuous_scale=[(0, "red"), (0.5, "#2E2E2E"), (1, "green")],  # Custom color scale
            labels={"x": "Sector", "y": "Metric", "color": "Change %"},
            zmin=-0.05,  # Adjust as needed
            zmax=0.08
        )

        fig.update_layout(
            title="Sector Performance Heatmap",
            xaxis_title="Sector",
            yaxis_title="Metric",
            coloraxis_colorbar=dict(title="Change %"),
            plot_bgcolor="#121212",
            paper_bgcolor="#121212",
            font=dict(color="white")
        )

        return fig