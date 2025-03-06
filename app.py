import dash
import dash_bootstrap_components as dbc  # Import Bootstrap Components
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

    # Flatten MultiIndex columns if necessary
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]  

    return df

# Layout of the dashboard (Now with a dark background)
app.layout = dbc.Container([
    html.H1("Stock Market Dashboard", style={'textAlign': 'center', 'color': 'white'}),

    dcc.Dropdown(
        id="stock-dropdown",
        options=[
            {"label": "Apple (AAPL)", "value": "AAPL"},
            {"label": "Tesla (TSLA)", "value": "TSLA"},
            {"label": "Amazon (AMZN)", "value": "AMZN"}
        ],
        value="AAPL",
        style={'width': '50%', 'color': 'black'}  # Ensure dropdown text is visible
    ),

    dcc.Graph(id="candlestick-chart")
], fluid=True, style={'backgroundColor': '#121212', 'padding': '20px'})

# Callback to update chart based on dropdown selection
@app.callback(
    dash.Output("candlestick-chart", "figure"),
    [dash.Input("stock-dropdown", "value")]
)
def update_chart(selected_stock):
    df = get_stock_data(selected_stock)

    if df.empty:
        return go.Figure()  # Return empty figure if no data

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
        template="plotly_dark"  # Dark mode for the chart
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)