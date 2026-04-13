import plotly.graph_objects as go
import plotly.express as px
from src import config

def apply_theme(fig, height=None):
    """
    Applies the general application theme to any plotly figure.
    """
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", color="white"),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    if height:
        fig.update_layout(height=height)
    return fig

def create_gauge(val, ref_val=None, title="Value"):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta" if ref_val else "gauge+number",
        value = val,
        delta = {'reference': ref_val, 'valueformat': '.3f', 'increasing': {'color': "#fbbf24"}} if ref_val else None,
        title = {'text': title, 'font': {'size': 20, 'color': '#34d399'}},
        gauge = {
            'axis': {'range': [0, 1], 'tickcolor': "white"},
            'bar': {'color': "#10b981"},
            'steps': [
                {'range': [0, 0.4], 'color': "rgba(16, 185, 129, 0.3)"},
                {'range': [0.4, 0.7], 'color': "rgba(251, 191, 36, 0.3)"},
                {'range': [0.7, 1.0], 'color': "rgba(239, 68, 68, 0.3)"}
            ],
            'threshold': {'line': {'color': "#ef4444", 'width': 4}, 'thickness': 0.75, 'value': 0.7}
        }
    ))
    return apply_theme(fig, 300)
