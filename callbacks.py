from dash.dependencies import Input, Output
from pages.search import get_stock_data, search_layout
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
         Input("timeframe-dropdown", "value")]
    )
    def update_chart(selected_stock, selected_timeframe):
        if not selected_stock:  # If no stock is entered
            return create_placeholder_chart()

        selected_stock = selected_stock.upper()  # Ensure uppercase

       
        df = get_stock_data(selected_stock, selected_timeframe)

        # Flatten MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]

        # Generate Candlestick Chart
        fig = go.Figure(data=[
            go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name="Candlesticks"
            )
        ])

        # Apply dark theme to chart
        fig.update_layout(
            title=f"{selected_stock} Price Chart ({selected_timeframe}, 1d)",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
        )

        return fig  
