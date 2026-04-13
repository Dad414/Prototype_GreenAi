# Ferghana Valley WSI Framework (GDCAU 2026 Finals)

**Project:** "AI as a Neutral Arbiter: Explainable ML Framework for Transboundary Water Stress in the Ferghana Valley"
**Team:** Khaliq Dad, Asif Khan, Saidboqirsho Alimadadshoev
**Institution:** University of Central Asia

This repository contains the deterministic, offline-capable machine learning pipeline and interactive Streamlit web application.

## Project Structure

- `data/`: Contains the master panel datasets (raw & processed) and pre-computed artifacts.
- `src/`: The Machine Learning Pipeline.
    - `run_all.py`: Orchestrates the entire data loading, model training, validation, and SHAP calculation process. Deterministic (`random_state=42`).
- `app/`: The Interactive Streamlit Prototype.
    - `streamlit_app.py`: Main entry point utilizing native multi-page routing.
- `outputs/`: 100% reproducible programmatic assets (Pickle models, NPZ SHAP objects, CSV validation results).

## How to Run the Pipeline (ML Training)

To regenerate all machine learning artifacts (Training RF WSI and RF SDG models, calculating the 4 validation batteries including Country Holdout, and generating Global/Local SHAP values):

```bash
python src/run_all.py
```

## How to Run the Prototype App (UI)

To launch the multi-page interactive web prototype locally:

```bash
streamlit run app/streamlit_app.py
```

## Methodological Findings

**The Country Holdout Negative R²**
The pipeline explicitly forces the Random Forest model to train on 2 countries (e.g. Kyrgyzstan, Tajikistan) and test on the 3rd (Uzbekistan). This resulting R² is strongly negative. This is empirical, mathematical proof of *institutional heterogeneity*—demonstrating that the structural drivers of water stress differ across transboundary lines. This is the foundation of our framing of AI as a Neutral Arbiter.
