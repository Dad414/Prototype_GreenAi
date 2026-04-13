import os
import joblib
import pandas as pd
import shap
import numpy as np
from src import config
from src.data_loader import load_master_panel

def generate_country_shap():
    print("[*] Generating Country-Specific SHAP values...")
    df = load_master_panel(processed=True)
    
    # Load model configuration
    wsi_model_data = joblib.load(config.MODEL_WSI_PATH)
    rfr = wsi_model_data['model']
    features = wsi_model_data['features']
    
    # We will compute SHAP values using the general model, but extracting local SHAP 
    # matrices specifically for the subsets of each country.
    explainer = shap.TreeExplainer(rfr)
    
    npz_dict = {
        'features': features,
        'base_value': explainer.expected_value
    }
    
    for country in df['country'].unique():
        # Get country specific slice
        c_mask = df['country'] == country
        X_c = df[c_mask][features]
        
        # Calculate SHAP for this country's 27 observations
        shap_values_c = explainer.shap_values(X_c)
        
        # We save strings into keys using country name prefixes
        prefix = f"{country[:2].upper()}"  # KY, TA, UZ
        npz_dict[f"{prefix}_shap"] = shap_values_c
        npz_dict[f"{prefix}_X"] = X_c.values

    # Save compilation dictionary
    os.makedirs(os.path.dirname(config.SHAP_COUNTRY_PATH), exist_ok=True)
    np.savez_compressed(config.SHAP_COUNTRY_PATH, **npz_dict)
    
    print(f"[+] Saved country-specific SHAP to {config.SHAP_COUNTRY_PATH}")

if __name__ == "__main__":
    generate_country_shap()
