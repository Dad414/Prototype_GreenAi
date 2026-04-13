import os
import sys
import streamlit as st

# Ensure `src` module is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.styles import inject_theme

st.set_page_config(
    page_title="Ferghana Valley WSI Framework",
    page_icon="💧",
    layout="wide"
)

# Inject Global CSS Theme
inject_theme()

# Native Streamlit Multi-Page routing using st.Page
pages = [
    st.Page("pages/01_Overview.py", title="1. Map & Overview", icon="🗺️"),
    st.Page("pages/02_Time_Series.py", title="2. Time Series Explorer", icon="📈"),
    st.Page("pages/03_Validation.py", title="3. Model Validation Tests", icon="✅"),
    st.Page("pages/04_Global_SHAP.py", title="4. Global Explainability", icon="🔍"),
    st.Page("pages/05_Country_SHAP.py", title="5. Country-Specific SHAP", icon="⚖️"),
    st.Page("pages/06_Counterfactual.py", title="6. Counterfactual Demo", icon="🎛️"),
]

pg = st.navigation(pages, position="hidden")

# --- SIDEBAR BRANDING (ABOVE TABS) ---
st.sidebar.image(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "uca_logo.jpg"), use_container_width=True)
st.sidebar.markdown("""
### AI as a Neutral Arbiter
**GDCAU 2026**
""")
st.sidebar.divider()

# --- SIDEBAR NAVIGATION (BELOW BRANDING) ---
st.sidebar.markdown("##### 🧭 Navigation")
for page in pages:
    st.sidebar.page_link(page, label=page.title, icon=page.icon)

st.sidebar.divider()
st.sidebar.markdown("""
*Khaliq Dad, Asif Khan, Saidboqirsho Alimadadshoev*  
*University of Central Asia*
""")

pg.run()
