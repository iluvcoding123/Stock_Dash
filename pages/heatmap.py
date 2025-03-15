from dash import html, dcc
import dash_bootstrap_components as dbc

def heatmap_layout():
    """Layout for the heatmap page."""
    return dbc.Container([
        html.H2("Sector Performance Heatmap", className="text-center", style={'color': 'white'}),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="sector-heatmap"  # The heatmap will be updated dynamically via callbacks
                )
            ], width=12)
        ]),
    ], fluid=True)