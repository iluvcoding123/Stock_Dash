from dash.dependencies import Input, Output
import plotly.express as px
from charts import create_placeholder_chart

def register_market_overview_callbacks(app):
    """Registers callbacks for the Market Overview page."""

    @app.callback(
        Output("market-overview-chart", "figure"),
        Input("url", "pathname")  
    )
    def update_market_overview(_):
        """Currently returns a placeholder chart."""
        return create_placeholder_chart()