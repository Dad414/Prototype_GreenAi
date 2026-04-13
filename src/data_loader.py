import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder
from src import config

def load_master_panel(processed=True):
    """
    Single source of truth for data loading.
    If 'processed' is False, load raw excel to process it. Otherwise load the processed CSV.
    During the pipeline creation, we load raw, process, and save.
    In the Streamlit app, we usually load processed.
    """
    if processed:
        if os.path.exists(config.PROCESSED_PANEL):
            return pd.read_csv(config.PROCESSED_PANEL)
        else:
            print(f"Warning: {config.PROCESSED_PANEL} not found. Loading raw Excel instead.")

    # Load raw excel
    if not os.path.exists(config.MASTER_PANEL):
        raise FileNotFoundError(f"Master panel not found at {config.MASTER_PANEL}")
    
    df = pd.read_excel(config.MASTER_PANEL)
    
    # Ensure country_code exists for SHAP and RF modeling
    if 'country_code' not in df.columns:
        le = LabelEncoder()
        df['country_code'] = le.fit_transform(df['country'])
        
    return df

def get_training_features(df):
    """
    Returns the list of features to use for the WSI model. 
    It takes all numeric columns and removes targets and IDs.
    """
    # Select all numeric types
    num_df = df.select_dtypes(include=['number'])
    
    # Exclude targets, IDs, and leakages
    exclude = config.ID_COLS + config.WSI_COMPONENTS + [config.OUTCOME_WSI, config.OUTCOME_SDG, 'year']
    
    # Optional logic: 'year' might be excluded to prevent temporal leakage, or kept. 
    # Usually we don't regress strictly on 'year' as an integer if we want structural drivers, 
    # but let's keep it out by default unless specified. (Actually, for WSI, it's safer to exclude year to stop memorization).
    
    features = [c for c in num_df.columns if c not in exclude]
    return features
