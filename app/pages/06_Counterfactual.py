import streamlit as st
import joblib
import plotly.graph_objects as go
from src.data_loader import load_master_panel
from src import config
from src.counterfactual import predict_counterfactual
from src.plot_utils import create_gauge

st.title("🎛️ Counterfactual Scenario Engine")
st.markdown("Adjust institutional drivers to simulate future water stress policy outcomes.")

try:
    df = load_master_panel(processed=True)
    wsi_model_data = joblib.load(config.MODEL_WSI_PATH)
    rfr = wsi_model_data['model']
    features = wsi_model_data['features']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 1. Select Baseline")
        sel_country = st.selectbox("Country", df['country'].unique(), index=1) # Default TJ
        provs = df[df['country'] == sel_country]['province'].unique()
        sel_prov = st.selectbox("Province", provs)
        sel_year = st.selectbox("Year", sorted(df['year'].unique(), reverse=True))
        
        # Extract baseline row
        base_mask = (df['country'] == sel_country) & (df['province'] == sel_prov) & (df['year'] == sel_year)
        if not base_mask.any():
            st.error("No data for this combination.")
            st.stop()
            
        base_row = df[base_mask].iloc[0]
        base_X = base_row[features]
        # Baseline prediction
        base_pred = float(rfr.predict(base_X.to_frame().T)[0])
        
        st.markdown(f"**Current predicted WSI:** `{base_pred:.3f}`")
        st.caption(f"Actual calculated WSI: {base_row['WSI']:.3f} | {base_row['WSI_category']}")
        
        st.markdown("### 2. Institutional Levers")
        
        # Defaults based on current values
        gov_base = float(base_X.get('water_governance_index', 0.5))
        tariff_base = float(base_X.get('water_tariff_index', 0.5))
        wua_base = float(base_X.get('wua_coverage', 0.5))
        emp_base = float(base_X.get('agri_employment_share', 0.5))
        
        # Deltas
        gov_chg = st.slider("Governance Index (Δ)", -0.4, 0.4, 0.0, step=0.01)
        tariff_chg = st.slider("Tariff Index (Δ)", -0.4, 0.4, 0.0, step=0.01)
        wua_chg = st.slider("WUA Coverage (Δ)", -0.5, 0.5, 0.0, step=0.01)
        emp_chg = st.slider("Agri Employment Share (Δ)", -0.2, 0.2, 0.0, step=0.01)
        
        deltas = {}
        if gov_chg != 0: deltas['water_governance_index'] = gov_chg
        if tariff_chg != 0: deltas['water_tariff_index'] = tariff_chg
        if wua_chg != 0: deltas['wua_coverage'] = wua_chg
        if emp_chg != 0: deltas['agri_employment_share'] = emp_chg
        
    with col2:
        st.markdown("### 3. Projected Outcome")
        
        if not deltas:
            st.info("Adjust levers on the left to see counterfactual results.")
            st.plotly_chart(create_gauge(base_pred, title="Current WSI Prediction"), use_container_width=True)
        else:
            new_pred, new_shaps, new_X = predict_counterfactual(rfr, base_X, deltas)
            
            st.plotly_chart(create_gauge(new_pred, ref_val=base_pred, title="Counterfactual WSI"), use_container_width=True)
            
            # Narrative calculation
            diff = new_pred - base_pred
            direction = "decrease" if diff < 0 else "increase"
            
            # Find the modified feature with the highest absolute SHAP in the new state to build narrative
            top_modified_feat = ""
            top_shap_val = 0
            for f in deltas.keys():
                if abs(new_shaps.get(f, 0)) > abs(top_shap_val):
                    top_shap_val = new_shaps.get(f, 0)
                    top_modified_feat = f
                    
            st.markdown(f"""
            <div style='background-color:#e8f4f8; border-left: 5px solid #3498db; padding: 15px;'>
                <b>Simulation Narrative:</b><br><br>
                Applying these institutional adjustments to {sel_prov} in {sel_year} would <b>{direction}</b> predicted WSI by {abs(diff):.3f}.
                This change is primarily influenced by the shift in <code>{top_modified_feat}</code>, which now exerts a SHAP contribution of {top_shap_val:.3f} to the model.
            </div>
            """, unsafe_allow_html=True)
            
            # Waterfall for new state (simulated via bar chart since waterfall requires specific objects)
            st.markdown("#### Adjusted SHAP Profile (Post-Intervention)")
            # Top 6 shaps in new state
            shap_series = pd.Series(new_shaps)
            top_shaps = shap_series.abs().sort_values(ascending=False).head(8)
            actual_shaps = shap_series[top_shaps.index]
            
            fig = go.Figure(go.Bar(
                x=actual_shaps.values,
                y=actual_shaps.index,
                orientation='h',
                marker_color=['red' if v > 0 else 'green' for v in actual_shaps.values]
            ))
            fig.update_layout(title="Top Driving Features in Counterfactual State", template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error loading counterfactual engine: {e}")
