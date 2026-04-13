import streamlit as st

def inject_theme():
    """
    Injects a premium 'Forest Mint' Light-Dark theme with glassmorphism 
    and high-visibility typography.
    """
    st.markdown("""
    <style>
        /* Main background: Deep Forest Gradient */
        .stApp {
            background: linear-gradient(135deg, #064e3b 0%, #0f172a 100%);
            color: #f8fafc;
        }

        /* Glassmorphism Card Style */
        .glass-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 24px;
            border: 1px solid rgba(52, 211, 153, 0.2);
            margin: 10px 0;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        /* Titles and High Contrast Text */
        h1, h2, h3 {
            color: #34d399 !important; /* Mint Green */
            font-weight: 800 !important;
            letter-spacing: -0.02em !important;
        }
        
        h4, h5, h6, b, strong {
            color: #ffffff !important;
            font-weight: 700 !important;
        }

        p, span, label, div {
            color: #e2e8f0; /* Soft slate white for readability */
        }

        /* Buttons and Interactive Elements */
        .stButton>button {
            background-color: #10b981 !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }

        .stButton>button:hover {
            background-color: #059669 !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
        }

        /* High Visibility Metric boxes */
        [data-testid="stMetricValue"] {
            color: #34d399 !important;
            font-weight: 800 !important;
        }
        [data-testid="stMetricDelta"] {
            color: #fbbf24 !important;
        }

        /* Sidebar override: Keep standard dark grey as requested */
        [data-testid="stSidebar"] {
            background-color: #1f2937 !important;
        }
        [data-testid="stSidebar"] * {
            color: #94a3b8 !important;
        }

        /* Slider color */
        .stSlider [data-baseweb="slider"] {
            color: #10b981;
        }
    </style>
    """, unsafe_allow_html=True)

def kpi_box(label, value, delta=None):
    """
    Renders a glassmorphism KPI card.
    """
    delta_html = f'<div style="color:#fbbf24; font-size:0.9rem; font-weight:600;">{delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="glass-card">
        <div style="color:#94a3b8; font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">{label}</div>
        <div style="color:#34d399; font-size:2.2rem; font-weight:800; line-height:1;">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)
