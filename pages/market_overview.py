import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

def market_overview_layout():
    """
    Layout for the Market Overview page.
    """
    return html.Div([
        html.H1("Market Overview", style={'textAlign': 'center', 'color': 'white'}),
        html.Br(),
        dcc.Graph(id="market-overview-graph")
    ], style={'padding': '20px'})