import pandas as pd
import shap
from src import config

def predict_counterfactual(model, X_base, feature_changes):
    """
    Takes a baseline row and applies a dictionary of delta adjustments.
    Returns: 
    - The new predicted WSI
    - A dictionary of specific SHAP contributions for the new prediction
    """
    if isinstance(X_base, pd.Series):
        X_df = pd.DataFrame([X_base])
    else:
        X_df = X_base.copy()
        
    # Apply changes (deltas)
    for feat, delta in feature_changes.items():
        if feat in X_df.columns:
            # We clip values to logical bounds (e.g., indices to 0-1)
            new_val = X_df[feat].iloc[0] + delta
            if 'index' in feat or 'pct' in feat or 'share' in feat or feat == 'wua_coverage':
                # General assumption: percentages and indices don't exceed 1.0 (or 100 depending on scale)
                # In this dataset, pct is 0-1.
                new_val = max(0.0, min(1.0, new_val))
            X_df[feat] = new_val
            
    # Re-predict
    new_pred = float(model.predict(X_df)[0])
    
    # Calculate SHAP contribution for this specific new row
    explainer = shap.TreeExplainer(model)
    shaps = explainer.shap_values(X_df)[0]
    
    shap_dict = {feat: shaps[i] for i, feat in enumerate(X_df.columns)}
    
    return new_pred, shap_dict, X_df
