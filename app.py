import dash
import dash_bootstrap_components as dbc  
from dash import dcc, html
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

# Initialize Dash app with a dark theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Function to fetch stock data
def get_stock_data(ticker="SPY", timeframe="1y"):
    df = yf.download(ticker, period=timeframe, interval="1d", progress=False)

    if df.empty:
        return pd.DataFrame()  # Prevent crashes if no data

    return df

# Sidebar Layout with Navigation
sidebar = dbc.Col([
    html.H2("Dashboard", style={'color': 'white'}),
    html.Hr(),
    
    # Navigation Links
    dbc.Nav([
        dbc.NavLink("Search", href="/", active="exact"),
        dbc.NavLink("Heatmap", href="/heatmap", active="exact"),
        dbc.NavLink("Market Overview", href="/market-overview", active="exact"),
    ], vertical=True, pills=True, style={'padding': '10px'}),

    html.Hr(),

    # Stock Input & Timeframe Selection (Only for Candlestick Page)
    html.Div(id="sidebar-content")  
], width=2, style={"backgroundColor": "#121212", "padding": "20px", "height": "100vh"})

# App Layout with Routing
app.layout = dbc.Container([
    dcc.Location(id="url", refresh=False),  # Tracks URL changes
    dbc.Row([
        sidebar,  # Sidebar with navigation links
        dbc.Col(id="page-content", width=10)  # Main content section
    ])
], fluid=True)

# Callback to update sidebar content dynamically
@app.callback(
    dash.Output("sidebar-content", "children"),
    [dash.Input("url", "pathname")]
)
def update_sidebar(pathname):
    if pathname == "/":
        return dbc.Container([
            html.Label("Search Ticker:", style={'color': 'white'}),
            dcc.Input(
                id="stock-input",
                type="text",
                placeholder="Enter ticker",
                value="SPY",
                style={'width': '100%', 'padding': '10px', 'backgroundColor': '#222222', 'color': 'white'}
            ),
            html.Br(),
            
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
                clearable=False
            )
        ])
    else:
        return None

# Callback to update page content dynamically
@app.callback(
    dash.Output("page-content", "children"),
    [dash.Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/heatmap":
        return create_heatmap_page()
    elif pathname == "/market-overview":
        return create_market_overview_page()
    else:
        return create_search_page()  # Default to Candlestick Chart

# Candlestick Chart Page
def create_search_page():
    return dbc.Container([
        html.H1("Ticker Search", style={'textAlign': 'center', 'color': 'white'}),
        html.Br(),
        dcc.Graph(id="candlestick-chart")
    ])

# Heatmap Page
def create_heatmap_page():
    return dbc.Container([
        html.H1("Market Heatmap", style={'textAlign': 'center', 'color': 'white'}),
        html.Br(),
        dcc.Graph(id="heatmap-chart")
    ])

# Market Overview Page
def create_market_overview_page():
    return dbc.Container([
        html.H1("Market Overview", style={'textAlign': 'center', 'color': 'white'}),
        html.Br(),
        dcc.Graph(id="market-overview-chart")
    ])

# Callback to update chart when ticker or timeframe is changed
@app.callback(
    dash.Output("candlestick-chart", "figure"),
    [dash.Input("stock-input", "value"),
     dash.Input("timeframe-dropdown", "value")]
)
def update_chart(selected_stock, selected_timeframe):
    if not selected_stock:  # If input is blank
        return create_placeholder_chart()

    selected_stock = selected_stock.upper()  # Ensure uppercase

    df = get_stock_data(selected_stock, selected_timeframe)

    # Flatten MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    # Generate Candlestick Chart
    fig = go.Figure(data=[
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name="Candlesticks"
        )
    ])

    # Apply dark theme to chart
    fig.update_layout(
        title=f"{selected_stock} Price Chart ({selected_timeframe}, 1d)",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
    )

    return fig

# Function to create a dark-themed placeholder chart
def create_placeholder_chart():
    fig = go.Figure()
    fig.update_layout(
        title="Enter a valid ticker",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",  # Ensure it matches dark theme
        xaxis_rangeslider_visible=False,
    )
    return fig

# Run the app: python app.py
if __name__ == '__main__':
    app.run_server(debug=True)