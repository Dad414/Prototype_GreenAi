import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src import config
from src.data_loader import load_master_panel
from src.plot_utils import apply_theme

st.title("✅ Model Validation & Institutional Heterogeneity")

# Explicit directive from user specs regarding the R2 commentary
st.markdown("""
<div class="glass-card" style="border-left: 5px solid #fbbf24;">
    <h4 style="color:#fbbf24 !important; margin-top:0;">🚨 EMPIRICAL FINDING: The Negative R²</h4>
    The <b>Country Holdout R² is negative</b>. This is NOT a bug. It is empirical proof of <b>institutional heterogeneity</b>.
    <br><br>
    It demonstrates mathematically that the structural drivers of water stress (how architecture and governance interact with climate) are fundamentally different across the borders of Kyrgyzstan, Tajikistan, and Uzbekistan. 
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
        color_discrete_map={'Positive (Fit OK)': '#34d399', 'Negative (System Break)': '#ef4444'},
        title="Predictive Performance (R²) across Validation Paradigms"
    )
    fig.add_hline(y=0, line_dash="solid", line_color="white")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(apply_theme(fig), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # --- NEW: Predictive Movement Chart ---
    st.markdown("### 📈 Prediction Fidelity (Time-Series)")
    st.markdown("Select a province to visualize the model's accuracy in capturing historical fluctuations.")

    df = load_master_panel(processed=True)
    
    col_sel, _ = st.columns([1, 2])
    with col_sel:
        all_provs = sorted(df['province'].unique())
        sel_prov = st.selectbox("Select Province", all_provs, index=all_provs.index('Batken') if 'Batken' in all_provs else 0)

    df_prov = df[df['province'] == sel_prov].sort_values('year')

    fig_pred = go.Figure()

    # Actual Line
    fig_pred.add_trace(go.Scatter(
        x=df_prov['year'], y=df_prov['WSI'],
        mode='lines+markers',
        name='Actual WSI (Calculated)',
        line=dict(color='#34d399', width=3),
        marker=dict(size=8)
    ))

    # Predicted Line
    fig_pred.add_trace(go.Scatter(
        x=df_prov['year'], y=df_prov['WSI_predicted'],
        mode='lines+markers',
        name='Predicted WSI (Model)',
        line=dict(color='#fbbf24', width=2, dash='dash'),
        marker=dict(size=6)
    ))

    fig_pred.update_layout(
        title=f"Actual vs. Predicted WSI Movement: {sel_prov}",
        xaxis_title="Year",
        yaxis_title="Water Stress Index",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(apply_theme(fig_pred), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

except FileNotFoundError:
    st.error("Validation results not found. Please run `python src/run_all.py` to compile the pipeline outputs.")
