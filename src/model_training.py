import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from src import config
from src.data_loader import load_master_panel, get_training_features

def train_and_save_models():
    print("[*] Loading data for model training.")
    df = load_master_panel(processed=False)
    
    # Ensure outputs directory exists
    os.makedirs(os.path.dirname(config.MODEL_WSI_PATH), exist_ok=True)
    
    # -- 1. WSI Model --
    features_wsi = get_training_features(df)
    X_wsi = df[features_wsi]
    y_wsi = df[config.OUTCOME_WSI]

    print(f"[*] Training rf_wsi model with {len(features_wsi)} features...")
    # rf config unpacked
    rf_wsi = RandomForestRegressor(**config.RF_CONFIG)
    rf_wsi.fit(X_wsi, y_wsi)
    
    # Save Model AND its expected feature list so we can easily check later
    joblib.dump({'model': rf_wsi, 'features': features_wsi}, config.MODEL_WSI_PATH)
    print(f"[+] Saved rf_wsi to {config.MODEL_WSI_PATH}")
    
    # -- 2. SDG 6.4.2 Model --
    # Predict sdg_642_water_stress_pct using ONLY environmental variables
    features_sdg = [f for f in config.ENV_FEATURES if f in df.columns]
    X_sdg = df[features_sdg]
    y_sdg = df[config.OUTCOME_SDG]
    
    print(f"[*] Training rf_sdg model with {len(features_sdg)} env features...")
    rf_sdg = RandomForestRegressor(**config.RF_CONFIG)
    rf_sdg.fit(X_sdg, y_sdg)
    
    joblib.dump({'model': rf_sdg, 'features': features_sdg}, config.MODEL_SDG_PATH)
    print(f"[+] Saved rf_sdg to {config.MODEL_SDG_PATH}")
    
    # -- Save Processed Dataset --
    # Store predictions in the processed panel
    df['WSI_predicted'] = rf_wsi.predict(X_wsi)
    df.to_csv(config.PROCESSED_PANEL, index=False)
    print(f"[+] Generated processed master panel at {config.PROCESSED_PANEL}")
    
    return rf_wsi, rf_sdg

if __name__ == "__main__":
    train_and_save_models()
