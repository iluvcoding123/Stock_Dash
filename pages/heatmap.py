import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output

def heatmap_layout():
    """
    Layout for the Heatmap page.
    """
    return dbc.Col([
        html.H1("Heatmap", style={'textAlign': 'center', 'color': 'white'}),
        html.Br(),

        # Heatmap placeholder graph
        dcc.Graph(id="sector-heatmap")
    ], width=10)


def register_heatmap_callbacks(app):
    @app.callback(
        Output("sector-heatmap", "figure"),
        [Input("sector-heatmap", "id")]  # Placeholder input to trigger callback
    )
    def update_heatmap(_):
        # Dummy sector performance data
        sectors = ["Technology", "Healthcare", "Financials", "Energy", "Consumer Goods"]
        periods = ["1D", "1W", "1M", "3M", "6M", "1Y"]
        performance = [[0.5, -1.2, 2.3, -0.8, 1.5, 0.2],
                       [-0.3, 0.9, -2.1, 1.2, -1.0, 0.4],
                       [1.0, 1.5, -0.5, -1.2, 0.8, -0.6],
                       [-0.8, 0.3, 1.2, 0.5, -1.3, 2.1],
                       [0.4, -0.6, 0.8, -1.5, 1.2, 0.9]]

        df = pd.DataFrame(performance, index=sectors, columns=periods)

        # Create heatmap figure
        fig = go.Figure(data=go.Heatmap(
            z=df.values,
            x=df.columns,
            y=df.index,
            colorscale="RdYlGn",  # Red-Yellow-Green color scheme
            colorbar_title="Performance (%)"
        ))

        fig.update_layout(
            title="Sector Performance Heatmap",
            xaxis_title="Time Period",
            yaxis_title="Sector",
            template="plotly_dark"
        )

        return fig