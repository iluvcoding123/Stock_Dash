from dash import html, dcc
import dash_bootstrap_components as dbc
from charts import create_placeholder_chart  # Import the placeholder chart function

def heatmap_layout():
    """Layout for the heatmap page."""
    return dbc.Container([
        html.H2("Heatmap", className="text-center", style={'color': 'white'}),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="sector-heatmap",
                    figure=create_placeholder_chart()  # Use the placeholder chart
                )
            ], width=12)
        ]),
    ], fluid=True)