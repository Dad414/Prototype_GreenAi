import streamlit as st
import plotly.express as px
from src.data_loader import load_master_panel
from src import config

st.title("📈 Time Series Explorer")
st.markdown("Explore trends in environmental and institutional drivers over the 2016–2024 period.")

df = load_master_panel(processed=True)

# Selectors
num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
num_cols = [c for c in num_cols if c not in ['year', 'country_code']]

col_sel = st.selectbox("Select Variable to Explore", num_cols, index=num_cols.index('WSI') if 'WSI' in num_cols else 0)
countries = st.multiselect("Select Countries", ['Kyrgyzstan', 'Tajikistan', 'Uzbekistan'], default=['Kyrgyzstan', 'Tajikistan', 'Uzbekistan'])

if countries:
    df_filt = df[df['country'].isin(countries)]
    
    # Calculate means per country per year
    df_trend = df_filt.groupby(['year', 'country'])[col_sel].mean().reset_index()
    
    fig = px.line(
        df_trend, x="year", y=col_sel, color="country", markers=True,
        color_discrete_map=config.COUNTRY_COLORS,
        title=f"Trend of {col_sel} (2016-2024)"
    )
    
    # Minimalistic theme
    fig.update_layout(template="plotly_white", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("Show raw data"):
        st.dataframe(df_trend)
else:
    st.info("Select at least one country to view trends.")
