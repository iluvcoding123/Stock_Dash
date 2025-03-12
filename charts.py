import plotly.graph_objs as go

def create_placeholder_chart():
    """
    Creates a placeholder chart with a dark theme.
    """
    fig = go.Figure()
    fig.update_layout(
        title="Enter a valid ticker",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",  # Matches the app's dark theme
        xaxis_rangeslider_visible=False,
    )
    return fig