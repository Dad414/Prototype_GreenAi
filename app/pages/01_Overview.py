import streamlit as st
import plotly.express as px
from src import config
from src.data_loader import load_master_panel
from src.styles import kpi_box
from src.plot_utils import apply_theme

st.title("🗺️ Overview & Regional Status")

df = load_master_panel(processed=True)

yr = st.slider("Select Year", int(df['year'].min()), int(df['year'].max()), int(df['year'].max()))
df_yr = df[df['year'] == yr]

st.markdown("### WSI Distribution by Province")

# Mapping simple coordinates for the 9 provinces
COORDS = {
    'Batken': (40.06, 70.82), 'Jalal-Abad': (40.93, 72.99), 'Osh': (40.52, 72.80),
    'Isfara': (40.12, 70.62), 'Khujand': (40.28, 69.62), 'Konibodom': (40.51, 70.42),
    'Andijan': (40.78, 72.34), 'Fergana': (40.39, 71.78), 'Namangan': (41.00, 71.67),
}

df_yr_geo = df_yr.copy()
df_yr_geo['lat'] = df_yr_geo['province'].map(lambda x: COORDS.get(x, (0,0))[0])
df_yr_geo['lon'] = df_yr_geo['province'].map(lambda x: COORDS.get(x, (0,0))[1])

fig = px.scatter_mapbox(
    df_yr_geo, lat="lat", lon="lon", color="WSI", size="population_total_thousand",
    hover_name="province", hover_data=["country", "WSI_category"],
    color_continuous_scale="Viridis", zoom=6, center={"lat": 40.5, "lon": 71.5},
    mapbox_style="carto-darkmatter", title=f"Water Stress Index ({yr})"
)
fig.update_layout(height=500, margin={"r":0,"t":40,"l":0,"b":0})
st.plotly_chart(apply_theme(fig), use_container_width=True)

st.divider()

st.markdown("### 📊 Country Performance Metrics")
c1, c2, c3 = st.columns(3)

for idx, country in enumerate(['Kyrgyzstan', 'Tajikistan', 'Uzbekistan']):
    col = [c1, c2, c3][idx]
    c_data = df_yr[df_yr['country'] == country]
    color = config.COUNTRY_COLORS[country]
    
    with col:
        st.markdown(f"#### <span style='color:{color}'>{country}</span>", unsafe_allow_html=True)
        kpi_box("Mean WSI", f"{c_data['WSI'].mean():.3f}")
        kpi_box("SDG 6.4.2 Stress", f"{c_data['sdg_642_water_stress_pct'].mean():.1f}%")
        kpi_box("WUA Coverage", f"{c_data['wua_coverage'].mean()*100:.1f}%")
