from dash import dcc, html
import dash_bootstrap_components as dbc

def search_layout():
    """
    Layout for the Search page.
    """
    return dbc.Col([
        html.H2("Search", className="text-center", style={'color': 'white'}),
        html.Hr(),

        # Search Input and Timeframe Selection
        dbc.Row([
            dbc.Col([
                html.Label("Search Ticker:", style={'color': 'white'}),
                dcc.Input(
                    id="stock-input",
                    type="text",
                    placeholder="Enter ticker",
                    value="SPY",
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'backgroundColor': '#222222',
                        'color': 'white',
                        'border': '1px solid #444444'
                    }
                )
            ], width=4),  

            dbc.Col([
                html.Label("Select Timeframe:", style={'color': 'white'}),
                dcc.Dropdown(
                    id="timeframe-dropdown",
                    options=[
                        {"label": "1 Year", "value": "1y"},
                        {"label": "6 Months", "value": "6mo"},
                        {"label": "3 Months", "value": "3mo"},
                        {"label": "1 Month", "value": "1mo"}
                    ],
                    value="6mo",
                    clearable=False,
                    style={'backgroundColor': '#222222', 'color': 'black'}
                )
            ], width=4),
        ], justify="center"),  

        html.Br(),

        # Candlestick Chart
        dcc.Graph(id="candlestick-chart"),

        html.Br(),

        # SMA Selection Checkboxes
        html.Label("Show Moving Averages:", style={'color': 'white'}),
        dcc.Checklist(
            id="sma-checkbox",
            options=[
                {"label": "50-day SMA", "value": "SMA50"},
                {"label": "100-day SMA", "value": "SMA100"},
                {"label": "200-day SMA", "value": "SMA200"}
            ],
            value=[],  # Default: No SMAs selected
            inline=True,
            style={'color': 'white'}
        )
    ], width=10)