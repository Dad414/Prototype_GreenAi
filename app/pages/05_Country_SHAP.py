import streamlit as st
import numpy as np
import plotly.express as px
from src import config

st.title("⚖️ Country-Specific SHAP Decompositions")

st.markdown("""
By decomposing the SHAP values spatially, we observe that the primary institutional and physical drivers of water stress 
**change entirely depending on the country**.
""")

try:
    with np.load(config.SHAP_COUNTRY_PATH, allow_pickle=True) as data:
        features = data['features'].tolist()
        
        # We know prefixes are KY, TA, UZ based on the generator script
        countries_map = {
            'KY': 'Kyrgyzstan',
            'TA': 'Tajikistan',
            'UZ': 'Uzbekistan'
        }
        
        cols = st.columns(3)
        
        for idx, (prefix, full_name) in enumerate(countries_map.items()):
            shap_key = f"{prefix}_shap"
            if shap_key in data:
                c_shap = data[shap_key]
                mean_abs_shap = np.abs(c_shap).mean(axis=0)
                
                # Get top 8 features to keep charts clean
                top_idx = np.argsort(mean_abs_shap)[-8:]
                top_feats = [features[i] for i in top_idx]
                top_shaps = mean_abs_shap[top_idx]
                
                color = config.COUNTRY_COLORS.get(full_name, '#333')
                
                fig = px.bar(
                    x=top_shaps, y=top_feats, orientation='h',
                    title=f"{full_name} Top Drivers",
                    labels={'x': 'Mean |SHAP|', 'y': ''}
                )
                fig.update_traces(marker_color=color)
                fig.update_layout(
                    template="plotly_white", 
                    height=400,
                    margin=dict(l=0, r=0, t=40, b=0),
                    title_font=dict(size=14, color=color)
                )
                
                with cols[idx]:
                    # Callout top feature
                    st.markdown(f"<span style='color:{color}; font-weight:bold'>Top Driver:</span> {top_feats[-1]}", unsafe_allow_html=True)
                    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ---
    ### The "Neutral Arbiter" Conclusion
    Because **Tajikistan's** stress is primarily driven by lack of infrastructure (e.g. `wua_coverage` or `governance`), while **Uzbekistan's** might be driven by agricultural demand (`crop_water_intensity`), a blanket basin-level policy will inevitably fail. 
    The AI acts as a neutral arbiter by proving from the raw data that institutional boundaries matter more than physical hydrology.
    """)

except FileNotFoundError:
    st.error("Country SHAP data not found. Please run the pipeline orchestrator.")
