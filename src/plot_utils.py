import plotly.graph_objects as go
import plotly.express as px
from src import config

def apply_theme(fig, height=None):
    """
    Applies the general application theme to any plotly figure.
    """
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Arial, sans-serif"),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    if height:
        fig.update_layout(height=height)
    return fig

def create_gauge(val, ref_val=None, title="Value"):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta" if ref_val else "gauge+number",
        value = val,
        delta = {'reference': ref_val, 'valueformat': '.3f'} if ref_val else None,
        title = {'text': title},
        gauge = {
            'axis': {'range': [0, 1]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 0.4], 'color': "lightgreen"},
                {'range': [0.4, 0.7], 'color': "moccasin"},
                {'range': [0.7, 1.0], 'color': "salmon"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 0.7}
        }
    ))
    return apply_theme(fig, 300)
