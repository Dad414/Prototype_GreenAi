import sys
import os

# Add root to python path so 'src' can be imported easily
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import model_training
from src import validation_tests
from src import shap_global
from src import shap_by_country

def main():
    print("============================================================")
    print(" FERGHANA VALLEY WSI PIPELINE (GDCAU 2026)")
    print("============================================================")
    
    print("\n[STEP 1] Model Training & Preprocessing")
    model_training.train_and_save_models()
    
    print("\n[STEP 2] Validation Battery (4 Tests)")
    validation_tests.run_validation_battery()
    
    print("\n[STEP 3] Global SHAP Computation")
    shap_global.generate_global_shap()
    
    print("\n[STEP 4] Country-Specific SHAP Computation")
    shap_by_country.generate_country_shap()
    
    print("\n============================================================")
    print(" PIPELINE COMPLETE.")
    print(" Outputs saved to: outputs/")
    print("============================================================")

if __name__ == "__main__":
    main()
