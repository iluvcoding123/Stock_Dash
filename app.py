import dash
import dash_bootstrap_components as dbc  
from dash import dcc, html
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

# Initialize Dash app with a dark theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Fetch stock data
def get_stock_data(ticker="AAPL"):
    df = yf.download(ticker, period="6mo", interval="1d", progress=False)

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
        value="AAPL",  # Default stock
        style={
            'width': '100%',
            'padding': '10px',
            'backgroundColor': '#222222',
            'color': 'white',
            'border': '1px solid #444444'
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

# Callback to update chart when ticker is entered
@app.callback(
    dash.Output("candlestick-chart", "figure"),
    [dash.Input("stock-input", "value")]
)
def update_chart(selected_stock):
    if not selected_stock:
        return go.Figure()  # Prevent errors if empty input

    selected_stock = selected_stock.upper()  # Ensure uppercase

    df = get_stock_data(selected_stock)

    # Flatten MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    # Debugging
    '''
    print(df.head())
    if df.empty:
        print(f"❌ No data found for {selected_stock}")  # Debugging
        return go.Figure()  # Return an empty figure if no data is found
    '''

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

    # Apply dark theme styling
    fig.update_layout(
        title=f"{selected_stock} Price Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        xaxis_rangeslider_visible=False
    )

    return fig

# Run the app: python app.py
if __name__ == '__main__':
    app.run_server(debug=True)