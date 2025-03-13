from dash import html, dcc
import dash_bootstrap_components as dbc
from charts import create_placeholder_chart  # Import placeholder chart

def market_overview_layout():
    """Layout for the market overview page."""
    return dbc.Container([
        html.H2("Market Overview", className="text-center", style={'color': 'white'}),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="market-overview-chart",
                    figure=create_placeholder_chart()  # Use placeholder chart
                )
            ], width=12)
        ]),
    ], fluid=True)