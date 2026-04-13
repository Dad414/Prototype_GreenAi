import os
import sys
import streamlit as st

# Ensure `src` module is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Ferghana Valley WSI Framework",
    page_icon="💧",
    layout="wide"
)

# Native Streamlit Multi-Page routing using st.Page
pages = [
    st.Page("pages/01_Overview.py", title="1. Map & Overview", icon="🗺️"),
    st.Page("pages/02_Time_Series.py", title="2. Time Series Explorer", icon="📈"),
    st.Page("pages/03_Validation.py", title="3. Model Validation Tests", icon="✅"),
    st.Page("pages/04_Global_SHAP.py", title="4. Global Explainability", icon="🔍"),
    st.Page("pages/05_Country_SHAP.py", title="5. Country-Specific SHAP", icon="⚖️"),
    st.Page("pages/06_Counterfactual.py", title="6. Counterfactual Demo", icon="🎛️"),
]

pg = st.navigation(pages)

# Sidebar persistent content
st.sidebar.markdown("""
### AI as a Neutral Arbiter
Explainable ML Framework for Transboundary Water Stress in the Ferghana Valley

**GDCAU 2026 Finals**
*Khaliq Dad, Asif Khan, Saidboqirsho Alimadadshoev*  
*University of Central Asia*
""")
st.sidebar.divider()

pg.run()
