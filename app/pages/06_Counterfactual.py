import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from src import config
from src.data_loader import load_master_panel
from src.counterfactual import predict_counterfactual
from src.plot_utils import create_gauge, apply_theme
from src.styles import kpi_box, inject_theme

st.title("🎛️ Counterfactual Scenario Engine")
st.markdown("Adjust institutional drivers to simulate future water stress policy outcomes.")

try:
    df = load_master_panel(processed=True)
    wsi_model_data = joblib.load(config.MODEL_WSI_PATH)
    rfr = wsi_model_data['model']
    features = wsi_model_data['features']
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("### 1. Select Baseline")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        sel_country = st.selectbox("Country", df['country'].unique(), index=1) # Default TJ
        provs = df[df['country'] == sel_country]['province'].unique()
        sel_prov = st.selectbox("Province", provs)
        sel_year = st.selectbox("Year", sorted(df['year'].unique(), reverse=True))
        st.markdown('</div>', unsafe_allow_html=True)
            
        # Extract baseline row
        base_mask = (df['country'] == sel_country) & (df['province'] == sel_prov) & (df['year'] == sel_year)
        if base_mask.any():
            base_row = df[base_mask].iloc[0]
            base_X = base_row[features]
            base_pred = float(rfr.predict(base_X.to_frame().T)[0])
            
            st.markdown("### 2. Institutional Levers")
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            # Deltas
            gov_chg = st.slider("Governance Index (Δ)", -0.4, 0.4, 0.0, step=0.01)
            tariff_chg = st.slider("Tariff Index (Δ)", -0.4, 0.4, 0.0, step=0.01)
            wua_chg = st.slider("WUA Coverage (Δ)", -0.5, 0.5, 0.0, step=0.01)
            emp_chg = st.slider("Agri Employment Share (Δ)", -0.2, 0.2, 0.0, step=0.01)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("### 3. Environmental Drivers")
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            temp_chg = st.slider("Temperature (Δ °C)", -4.0, 4.0, 0.0, step=0.1)
            precip_chg = st.slider("Precipitation (Δ mm)", -200, 200, 0, step=10)
            moist_chg = st.slider("Soil Moisture (Δ)", -0.1, 0.1, 0.0, step=0.01)
            st.markdown('</div>', unsafe_allow_html=True)
            
            deltas = {}
            if gov_chg != 0: deltas['water_governance_index'] = gov_chg
            if tariff_chg != 0: deltas['water_tariff_index'] = tariff_chg
            if wua_chg != 0: deltas['wua_coverage'] = wua_chg
            if emp_chg != 0: deltas['agri_employment_share'] = emp_chg
            if temp_chg != 0: deltas['annual_mean_temp_c'] = temp_chg
            if precip_chg != 0: deltas['annual_total_precip_mm'] = precip_chg
            if moist_chg != 0: deltas['soil_moisture_mean'] = moist_chg
        
    with col2:
        st.markdown("### 4. Projected Outcome")
        
        if not deltas:
            st.plotly_chart(create_gauge(base_pred, title="Baseline Predicted WSI"), use_container_width=True)
            kpi_box("Baseline WSI", f"{base_pred:.3f}")
        else:
            new_pred, new_shaps, new_X = predict_counterfactual(rfr, base_X, deltas)
            
            st.plotly_chart(create_gauge(new_pred, ref_val=base_pred, title="Counterfactual WSI"), use_container_width=True)
            
            diff = new_pred - base_pred
            direction = "DECREASE" if diff < 0 else "INCREASE"
            
            kpi_box("New Predicted WSI", f"{new_pred:.3f}", delta=f"{diff:+.3f} Δ Change")
            
            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid #10b981;">
                <b>Simulation Narrative:</b><br>
                Applying adjustments to <b>{sel_prov}</b> would <b>{direction}</b> predicted WSI by {abs(diff):.3f}.
            </div>
            """, unsafe_allow_html=True)
            
            # Waterfall for new state
            st.markdown("#### Adjusted SHAP Profile (Post-Intervention)")
            shap_series = pd.Series(new_shaps)
            top_shaps = shap_series.abs().sort_values(ascending=False).head(8)
            actual_shaps = shap_series[top_shaps.index]
            
            fig = go.Figure(go.Bar(
                x=actual_shaps.values,
                y=actual_shaps.index,
                orientation='h',
                marker_color=['#ef4444' if v > 0 else '#34d399' for v in actual_shaps.values]
            ))
            st.plotly_chart(apply_theme(fig, height=350), use_container_width=True)

except Exception as e:
    st.error(f"Error loading counterfactual engine: {e}")
