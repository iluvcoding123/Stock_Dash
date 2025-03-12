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

# Sidebar Layout
sidebar = dbc.Col([
    # Ticker Search Bar
    html.Label("Search Ticker:", style={'color': 'white'}),
    dcc.Input(
        id="stock-input",
        type="text",
        placeholder="Enter ticker",
        value="SPY",  # Default stock
        style={
            'width': '100%',
            'padding': '10px',
            'backgroundColor': '#222222',
            'color': 'white',
            'border': '1px solid #444444'
        }
    ),
    html.Br(),
    
    # Timeframe Dropdown
    html.Label("Select Timeframe:", style={'color': 'white'}),
    dcc.Dropdown(
        id="timeframe-dropdown",
        options=[
            {"label": "1 Year", "value": "1y"},
            {"label": "6 Months", "value": "6mo"},
            {"label": "3 Months", "value": "3mo"},
            {"label": "1 Month", "value": "1mo"}
        ],
        value="6mo",  # Default timeframe
        clearable=False,
        style={
            'backgroundColor': '#222222',
            'color': 'black'  # Text color
        }
    ),
], width=2, style={"backgroundColor": "#121212", "padding": "20px", "height": "100vh"})

# Main Content Layout
content = dbc.Col([
    html.H1("Stock Market Dashboard", style={'textAlign': 'center', 'color': 'white'}),
    html.Br(),
    dcc.Graph(id="candlestick-chart")
], width=10)

# Full Layout
app.layout = dbc.Container([
    dbc.Row([
        sidebar,   # Sidebar with search bar
        content    # Main content
    ])
], fluid=True)

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