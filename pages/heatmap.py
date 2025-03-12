import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

def heatmap_layout():
    """
    Layout for the Heatmap page.
    """
    return html.Div([
        html.H1("Heatmap", style={'textAlign': 'center', 'color': 'white'}),
        html.Br(),
        dcc.Graph(id="heatmap-graph")
    ], style={'padding': '20px'})