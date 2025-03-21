from dash.dependencies import Input, Output
from pages.search import search_layout
from pages.heatmap import heatmap_layout
from pages.market_overview import market_overview_layout
from callbacks.search_callbacks import register_search_callbacks  
from callbacks.heatmap_callbacks import register_heatmap_callbacks
from callbacks.market_overview_callbacks import register_market_overview_callbacks

def register_callbacks(app):
    """Registers all Dash callbacks."""

    # Register Search Callbacks
    register_search_callbacks(app)  
    register_heatmap_callbacks(app)
    register_market_overview_callbacks(app)

    # Page Navigation Callback
    @app.callback(
        Output("page-content", "children"), 
        [Input("url", "pathname")]
    )
    def display_page(pathname):
        """Handles page navigation between Search, Heatmap, and Market Overview pages."""
        if pathname == "/heatmap":
            return heatmap_layout()
        elif pathname == "/market-overview":
            return market_overview_layout()
        return search_layout()  # Default to Search page