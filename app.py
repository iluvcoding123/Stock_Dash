import dash
from dash import dcc, html
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

# Initialize Dash app
app = dash.Dash(__name__)

# Fetch stock data (Example: AAPL)
def get_stock_data(ticker="AAPL"):
    df = yf.download(ticker, period="6mo", interval="1d")
    return df

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Stock Market Dashboard", style={'textAlign': 'center'}),
    
    # Dropdown for stock selection
    dcc.Dropdown(
        id="stock-dropdown",
        options=[
            {"label": "Apple (AAPL)", "value": "AAPL"},
            {"label": "Tesla (TSLA)", "value": "TSLA"},
            {"label": "Amazon (AMZN)", "value": "AMZN"}
        ],
        value="AAPL",  # Default selection
        style={'width': '50%'}
    ),
    
    # Candlestick Chart
    dcc.Graph(id="candlestick-chart"),
])

# Callback to update chart based on dropdown selection
@app.callback(
    dash.Output("candlestick-chart", "figure"),
    [dash.Input("stock-dropdown", "value")]
)
def update_chart(selected_stock):
    df = get_stock_data(selected_stock)
    
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
    
    fig.update_layout(title=f"{selected_stock} Price Chart", xaxis_title="Date", yaxis_title="Price")
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)