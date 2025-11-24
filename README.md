# Glucose Predictor Pro

Streamlit dashboard that predicts survival years for diabetic patients and simulates post‑meal glucose impact. The app runs entirely in `app.py` and trains both RandomForest and XGBoost models on `IDPdataset_9000.csv`, while the nutrition simulator uses `data/indian_food_gi.csv` plus medication inputs to show projected glucose curves.

## Features
- **Automated EDA** – dataset preview, summary stats, missingness heatmap, correlation matrix, and feature importance.
- **Meal Impact Simulator** – choose foods, servings, personal vitals, and medication. Outputs glucose curve, metrics, and recommendations.
- **Survival Years Prediction** – collects patient profile, scales/encodes fields, blends model output with medical priors, and compares RandomForest vs XGBoost metrics in the sidebar.
- **Responsive UI** – glassmorphism theme with dark-mode overrides, metric cards, Altair visualizations, and expandable explainers.

## Local Setup
```bash
python -m venv .venv
.venv\Scripts\activate  # or source .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
streamlit run app.py
```

## Required Files
- `IDPdataset_9000.csv` – main training dataset (kept at repo root).
- `data/indian_food_gi.csv` – nutrition lookup used by the simulator.
- `static/bg.jpg` – background image referenced in the CSS theme.

## Deploying on Streamlit Cloud
1. Push the repo (already on `main`).
2. In Streamlit Cloud, create a new app pointing to `app.py`.
3. If you store large datasets elsewhere, update the code to download them at startup or configure secrets for private URLs.

## Repo Structure
```
.
├── app.py
├── requirements.txt
├── IDPdataset_9000.csv
├── data/
│   └── indian_food_gi.csv
└── static/
    └── bg.jpg
```

Feel free to open an issue or tweak the models/visuals to suit your deployment.

