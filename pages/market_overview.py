from dash import html, dcc
import dash_bootstrap_components as dbc
from callbacks.market_overview_callbacks import register_market_overview_callbacks

def market_overview_layout():
    """Layout for the market overview page."""
    return dbc.Container([
        html.H2("Market Overview", className="text-center", style={'color': 'white'}),
        html.Hr(),
        
        # VIX Chart
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="market-overview-chart")
            ], width=12)
        ]),
        
        # Interval component to auto-refresh data
        dcc.Interval(
            id="interval-update",
            interval=60000,  # Update every 60 seconds
            n_intervals=0
        )
    ], fluid=True)