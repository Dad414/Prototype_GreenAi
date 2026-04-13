import streamlit as st
import numpy as np
import plotly.express as px
from src import config
from src.data_loader import load_master_panel
from src.plot_utils import apply_theme

st.title("🔍 Global SHAP Explainability")

st.markdown("""
### The "Neutral Arbiter" View
SHAP (SHapley Additive exPlanations) isolates the exact contribution of each feature to the overall Water Stress Index. 
This global view aggregates the drivers across all 81 observations in the Ferghana Valley.
""")

try:
    with np.load(config.SHAP_GLOBAL_PATH, allow_pickle=True) as data:
        shap_values = data['shap_values']
        features = data['features'].tolist()
        
    # Calculate Mean |SHAP| for bar chart
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    
    # Sort for plotting
    sorted_idx = np.argsort(mean_abs_shap)
    sorted_features = [features[i] for i in sorted_idx][-15:]
    sorted_shaps = mean_abs_shap[sorted_idx][-15:]
    
    fig = px.bar(
        x=sorted_shaps, y=sorted_features, orientation='h',
        labels={'x': 'Mean |SHAP value| (Impact on WSI)', 'y': ''},
        title="Top 15 Global Drivers of Water Stress",
        color=sorted_shaps, color_continuous_scale="Viridis"
    )
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(apply_theme(fig), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    **Interpretation**:
    The length of the bars represents the average impact (positive or negative) of the feature across all data points.
    Typically, we see institutional variables (`water_governance_index`, `wua_coverage`) and agricultural variables (`crop_water_intensity`, `agri_employment_share`) acting as primary drivers in this overarching model.
    """)
    
except FileNotFoundError:
    st.error("Global SHAP data not found. Please run the pipeline orchestrator.")
