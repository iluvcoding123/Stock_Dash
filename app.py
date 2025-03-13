import dash
import dash_bootstrap_components as dbc  
from dash import dcc, html
from pages.heatmap import heatmap_layout, register_heatmap_callbacks
from pages.market_overview import market_overview_layout
from pages.search import search_layout, register_search_callbacks
from dash.dependencies import Input, Output

# Initialize Dash app with a dark theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Stock Market Dashboard"

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

# Page Content Layout
content = dbc.Col(id="page-content", width=10, style={"padding": "20px"})

# Full Layout
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),  # Allows dynamic page routing
    dbc.Row([
        sidebar,  # Sidebar navigation
        content   # Page content that changes dynamically
    ])
], fluid=True)

# Register Callbacks for Each Page
register_search_callbacks(app)
register_heatmap_callbacks(app)

# Page Navigation Callback
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/heatmap":
        return heatmap_layout()
    elif pathname == "/market-overview":
        return market_overview_layout()
    return search_layout()  # Default to Search page

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)