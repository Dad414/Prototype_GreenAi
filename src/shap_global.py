import os
import joblib
import pandas as pd
import shap
import numpy as np
from src import config
from src.data_loader import load_master_panel

def generate_global_shap():
    print("[*] Generating Global SHAP values...")
    df = load_master_panel(processed=True)
    
    # Load model configuration
    wsi_model_data = joblib.load(config.MODEL_WSI_PATH)
    rfr = wsi_model_data['model']
    features = wsi_model_data['features']
    
    X = df[features]
    
    # SHAP TreeExplainer
    explainer = shap.TreeExplainer(rfr)
    shap_values = explainer.shap_values(X)
    
    # Save arrays
    os.makedirs(os.path.dirname(config.SHAP_GLOBAL_PATH), exist_ok=True)
    np.savez_compressed(
        config.SHAP_GLOBAL_PATH, 
        shap_values=shap_values, 
        X_values=X.values, 
        base_value=explainer.expected_value,
        features=features
    )
    print(f"[+] Saved global SHAP to {config.SHAP_GLOBAL_PATH}")

if __name__ == "__main__":
    generate_global_shap()
