"""
Centralized Configuration for Ferghana Valley WSI Prototype
Contains paths, feature definitions, and global hyperparameters.
"""
import os

# ─── PATHS ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# Raw and processed datasets
MASTER_PANEL = os.path.join(DATA_DIR, "raw", "ferghana_master_panel.xlsx")
PROCESSED_PANEL = os.path.join(DATA_DIR, "processed", "ferghana_master_panel_processed.csv")

# Asset dumps
MODEL_WSI_PATH = os.path.join(OUTPUT_DIR, "models", "rf_wsi.pkl")
MODEL_SDG_PATH = os.path.join(OUTPUT_DIR, "models", "rf_sdg.pkl")
VALIDATION_RESULTS_PATH = os.path.join(OUTPUT_DIR, "results", "validation_results.csv")
SHAP_GLOBAL_PATH = os.path.join(OUTPUT_DIR, "shap", "shap_global.npz")
SHAP_COUNTRY_PATH = os.path.join(OUTPUT_DIR, "shap", "shap_by_country.npz")


# ─── DISCOVERY & FEATURE SETS ──────────────────────────────────────────
ID_COLS = ['country', 'province', 'year', 'WSI_category', 'country_code']

# Prevent data leakage: Do not train on components or WSI predictions
WSI_COMPONENTS = ['WSI_demand', 'WSI_supply', 'WSI_governance', 'WSI_predicted']

OUTCOME_WSI = 'WSI'
OUTCOME_SDG = 'sdg_642_water_stress_pct'

# Purely environmental drivers (Used for SDG 6.4.2 model baseline)
ENV_FEATURES = [
    'annual_mean_temp_c', 'annual_total_precip_mm', 'NDVI', 'NDSI', 'PET_mean',
    'lc_forest_pct', 'lc_grassland_pct', 'lc_cropland_pct', 'lc_urban_pct',
    'lc_barren_pct', 'lc_water_pct', 'soil_moisture_mean'
]

# Random Forest Configuration (Regularized to prevent overfitting on 81 obs)
RF_CONFIG = {
    'n_estimators': 200, 
    'max_depth': 6, 
    'random_state': 42, 
    'n_jobs': -1
}

# ─── VISUAL STYLING ────────────────────────────────────────────────────
COUNTRY_COLORS = {
    'Kyrgyzstan': '#1abc9c',
    'Tajikistan': '#e67e22',
    'Uzbekistan': '#3498db',
}
