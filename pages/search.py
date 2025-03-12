import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
from utils import get_stock_data
from charts import create_placeholder_chart
from dash.dependencies import Input, Output

def search_layout():
    """
    Layout for the Search page.
    """
    return dbc.Col([
        html.H1("Search", style={'textAlign': 'center', 'color': 'white'}),
        html.Br(),

        # Search Ticker and Timeframe Selection
        dbc.Row([
            dbc.Col([
                html.Label("Search Ticker:", style={'color': 'white'}),
                dcc.Input(
                    id="stock-input",
                    type="text",
                    placeholder="Enter ticker",
                    value="SPY",
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'backgroundColor': '#222222',
                        'color': 'white',
                        'border': '1px solid #444444'
                    }
                )
            ], width=4),  # Adjust width as needed

            dbc.Col([
                html.Label("Select Timeframe:", style={'color': 'white'}),
                dcc.Dropdown(
                    id="timeframe-dropdown",
                    options=[
                        {"label": "1 Year", "value": "1y"},
                        {"label": "6 Months", "value": "6mo"},
                        {"label": "3 Months", "value": "3mo"},
                        {"label": "1 Month", "value": "1mo"}
                    ],
                    value="6mo",
                    clearable=False,
                    style={'backgroundColor': '#222222', 'color': 'black'}
                )
            ], width=4),
        ], justify="center"),  # Center alignment

        html.Br(),

        # Candlestick Chart
        dcc.Graph(id="candlestick-chart")
    ], width=10)


def register_search_callbacks(app):
    @app.callback(
        Output("candlestick-chart", "figure"),
        [Input("stock-input", "value"),
         Input("timeframe-dropdown", "value")]
    )
    def update_chart(selected_stock, selected_timeframe):
        if not selected_stock:  # If input is blank
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