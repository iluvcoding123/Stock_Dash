import dash
import dash_bootstrap_components as dbc  
from dash import dcc, html
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from utils import get_stock_data
from charts import create_placeholder_chart
from heatmap import heatmap_layout
from market_overview import market_overview_layout
from search import search_layout, register_search_callbacks

# Initialize Dash app with a dark theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


# Sidebar Layout
sidebar = dbc.Col([
    html.H3("Dashboard", className="text-center", style={'color': 'white'}),
    html.Hr(),

    # Navigation Links
    dbc.Nav([
        dbc.NavLink("Search", href="/", active="exact"),
        dbc.NavLink("Heatmap", href="/heatmap", active="exact"),
        dbc.NavLink("Market Overview", href="/market-overview", active="exact"),
    ], vertical=True, pills=True, style={'padding': '10px'}),
    
    html.Hr(),
], width=2, style={"backgroundColor": "#121212", "padding": "20px", "height": "100vh"})

# Main Content Layout
content = search_layout()

# Full Layout
app.layout = dbc.Container([
    dbc.Row([
        sidebar,   # Sidebar with search bar
        content    # Main content
    ])
], fluid=True)

# Callback to update chart when ticker or timeframe is changed
register_search_callbacks(app)


# Run the app: python app.py
if __name__ == '__main__':
    app.run_server(debug=True)