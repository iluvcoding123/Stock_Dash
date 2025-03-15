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
    df_list = []  

    for sector, ticker in sector_tickers.items():
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")  

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
        
        if not sector_data.isna().all().all():
            df_list.append(sector_data)

    df = pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame(columns=["Sector"] + metrics)

    return df

def register_heatmap_callbacks(app):
    """Registers callbacks for the heatmap page."""

    @app.callback(
        Output("sector-heatmap", "figure"),
        Input("url", "pathname")  
    )
    def update_heatmap(_):
        """Generates the sector performance heatmap with adjusted color scaling."""
        df = get_sector_performance()

        # Adjusted color scale with whitish-yellow neutral, dark red for lows, and dark green for highs
        custom_colorscale = [
            [0.0, "#8B0000"],   # Dark Red (Strong Negative)
            [0.3, "#FF8C00"],   # Orange (-1.5% to -0.5%)
            [0.5, "#FFFACD"],   # Whitish Yellow (Neutral, ~0%)
            [0.7, "#9ACD32"],   # Yellowish Green (+0.5% to +1.5%)
            [1.0, "#004d00"]    # Darker Green (Strong Positive)
        ]

        fig = px.imshow(
            df.set_index("Sector").T.values,  
            x=df["Sector"],  
            y=["1D Change", "5D Change", "1M Change"],  
            color_continuous_scale=custom_colorscale,
            labels={"x": "Sector", "y": "Metric", "color": "Change %"},
            zmin=-0.025,  # Expanded range for better scaling
            zmax=0.025
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