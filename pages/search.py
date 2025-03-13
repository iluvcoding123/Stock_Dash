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

