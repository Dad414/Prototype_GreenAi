import streamlit as st
import pandas as pd
import plotly.express as px
from src import config

st.title("✅ Model Validation & Institutional Heterogeneity")

# Explicit directive from user specs regarding the R2 commentary
st.markdown("""
<div style='background-color:#fff3cd; border-left: 5px solid #ffc107; padding: 15px; margin-bottom:20px'>
    <h4 style="margin-top:0">🚨 EMPIRICAL FINDING: The Negative R²</h4>
    The <b>Country Holdout R² is negative</b>. This is NOT a bug. It is empirical proof of institutional heterogeneity.
    It demonstrates mathematically that the structural drivers of water stress (how agriculture and governance interact with climate) are fundamentally different across the borders of Kyrgyzstan, Tajikistan, and Uzbekistan. 
    A model trained on two countries structurally fails to map onto the third because the rules of the system change. This is the foundation of our "neutral arbiter" framing.
</div>
""", unsafe_allow_html=True)

try:
    results_df = pd.read_csv(config.VALIDATION_RESULTS_PATH)
    
    st.markdown("### Validation Battery Results (WSI Predictor)")
    st.dataframe(results_df, use_container_width=True)

    # Plot R2 scores
    # Colors for negative vs positive
    results_df['Color'] = results_df['Mean_R2'].apply(lambda x: 'Positive (Fit OK)' if x > 0 else 'Negative (System Break)')
    
    fig = px.bar(
        results_df, x="Test", y="Mean_R2", color="Color",
        color_discrete_map={'Positive (Fit OK)': '#2ecc71', 'Negative (System Break)': '#e74c3c'},
        title="Predictive Performance (R²) across Validation Paradigms"
    )
    fig.add_hline(y=0, line_dash="solid", line_color="black")
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("Validation results not found. Please run `python src/run_all.py` to compile the pipeline outputs.")
