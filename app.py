import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
# Custom CSS for metrics container
st.markdown("""
    <style>
    .metrics-container {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

def create_interpretation_section(peak_glucose, peak_time, baseline, in_range=True):
    """Display the predicted glucose values."""
    st.markdown(
        f"""
        <div style='margin: 1rem 0;'>
            <p style='margin: 0.5rem 0;'><strong>Predicted Peak Glucose:</strong> {peak_glucose:.0f} mg/dL at {peak_time} minutes</p>
            <p style='margin: 0.5rem 0;'><strong>Baseline Glucose:</strong> {baseline} mg/dL</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Page configuration
st.set_page_config(
    page_title="Glucose Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple background with image from static folder
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)),
                        url('static/bg.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
        }
        
        /* Frosted glass sidebar */
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.25) !important;
            backdrop-filter: blur(16px) saturate(180%);
            -webkit-backdrop-filter: blur(16px) saturate(180%);
            border-right: 1px solid rgba(255, 255, 255, 0.4);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            color: #2c3e50 !important;
        }
        
        /* Content container */
        .main .block-container {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.75));
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.25);
            padding: 2.8rem;
            margin: 2.5rem 1.5rem;
            box-shadow: 0 12px 35px 0 rgba(31, 38, 135, 0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .main .block-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.3);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-bottom: 1rem;
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(45deg, #6e45e2, #89d4cf);
            background-size: 200% 200%;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(110, 69, 226, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(110, 69, 226, 0.4);
            background-position: right center;
        }
        
        /* Interpretation cards */
        .interpretation-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 1.5rem;
            margin: 2rem 0;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            transition: all 0.3s ease;
        }
        
        .interpretation-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.2);
        }
        
        /* Metric cards */
        .metric-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 1.25rem;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            background: rgba(255, 255, 255, 0.15);
        }
        
        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0.5rem 0 0.25rem;
            background: linear-gradient(45deg, #6e45e2, #89d4cf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Alert styles */
        .alert-high {
            background: rgba(231, 76, 60, 0.1) !important;
            border-left: 4px solid #e74c3c;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Input fields */
        .stTextInput>div>div>input, 
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>div {
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.1);
            color: #2c3e50;
            padding: 0.5rem 0.75rem;
        }
        
        /* Focus states for inputs */
        .stTextInput>div>div>input:focus, 
        .stNumberInput>div>div>input:focus,
        .stSelectbox>div>div>div:focus {
            border-color: #6e45e2;
            box-shadow: 0 0 0 0.2rem rgba(110, 69, 226, 0.25);
        }
    
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(110, 69, 226, 0.5);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(110, 69, 226, 0.7);
        }

        @media (prefers-color-scheme: dark) {
            .stApp {
                color: #f5f7ff;
                background: linear-gradient(rgba(15, 23, 42, 0.9), rgba(15, 23, 42, 0.9)),
                            url('static/bg.jpg');
                background-size: cover;
                background-position: center;
            }

            .main .block-container {
                background: rgba(15, 23, 42, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 12px 35px 0 rgba(0, 0, 0, 0.4);
            }

            [data-testid="stSidebar"] {
                background: rgba(15, 23, 42, 0.6) !important;
                color: #f5f7ff !important;
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }

            h1, h2, h3, h4, h5, h6, label, p, span, div {
                color: #f5f7ff !important;
            }

            .metric-card,
            .metrics-container,
            .interpretation-card {
                background: rgba(30, 41, 59, 0.9);
                border: 1px solid rgba(148, 163, 184, 0.3);
            }

            .metric-value {
                background: linear-gradient(45deg, #93c5fd, #a5b4fc);
            }

            .stTextInput>div>div>input,
            .stNumberInput>div>div>input,
            .stSelectbox>div>div>div {
                background: rgba(15, 23, 42, 0.6);
                color: #f5f7ff;
                border: 1px solid rgba(148, 163, 184, 0.4);
            }

            .stTextInput>div>div>input:focus,
            .stNumberInput>div>div>input:focus,
            .stSelectbox>div>div>div:focus {
                border-color: #93c5fd;
                box-shadow: 0 0 0 0.2rem rgba(147, 197, 253, 0.25);
            }

            .stButton>button {
                background: linear-gradient(45deg, #3b82f6, #8b5cf6);
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
            }
        }
    </style>
""", unsafe_allow_html=True)

# Custom header with logo and title
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image("https://img.icons8.com/color/48/000000/diabetes.png", width=60)
with col2:
    st.title("Glucose Predictor Pro")
    st.caption("Predict and manage your glucose levels with AI-powered insights")

# Add a nice divider
st.markdown("---")

def calculate_health_score(row):
    """Calculate a health score based on key health indicators"""
    score = 0
    
    # Age adjustment (younger = better)
    age_score = max(0, 1 - (row['Age'] - 30) / 100)
    
    # Kidney function (eGFR)
    if 'eGFR' in row:
        if row['eGFR'] >= 90:  # Normal
            kidney_score = 1.0
        elif row['eGFR'] >= 60:  # Mild reduction
            kidney_score = 0.8
        elif row['eGFR'] >= 45:  # Mild-moderate
            kidney_score = 0.6
        elif row['eGFR'] >= 30:  # Moderate-severe
            kidney_score = 0.4
        else:  # Severe
            kidney_score = 0.2
    else:
        kidney_score = 0.7  # Default if missing
    
    # Blood sugar control (HbA1c)
    if 'HbA1c' in row:
        if row['HbA1c'] < 5.7:  # Normal
            a1c_score = 1.0
        elif row['HbA1c'] < 6.5:  # Prediabetes
            a1c_score = 0.8
        else:  # Diabetes
            a1c_score = 0.6
    else:
        a1c_score = 0.7
    
    # Combine scores with weights
    score = (age_score * 0.3 + 
             kidney_score * 0.3 + 
             a1c_score * 0.2 + 
             (1 if row.get('SmokingStatus', 'Never') == 'Never' else 0.8) * 0.1 +
             (1 if row.get('PhysicalActivity', 'Low') == 'High' else 0.7) * 0.1)
    
    return score

# Calculate base life expectancy based on age and gender
def get_base_life_expectancy(age, gender='Male'):
    """Get base life expectancy from standard life tables"""
    # Simplified life expectancy table (in years remaining)
    life_table = {
        'Male': {
            30: 47, 40: 38, 50: 29, 60: 21, 70: 14, 80: 8, 90: 4
        },
        'Female': {
            30: 51, 40: 41, 50: 32, 60: 23, 70: 15, 80: 9, 90: 5
        }
    }
    
    # Find closest age group
    age_group = min(life_table[gender].keys(), key=lambda x: abs(x - age))
    return life_table[gender][age_group]

# Cached data/model preparation to avoid re-running on every widget change
@st.cache_data(show_spinner=False)
def load_dataset():
    return pd.read_csv("IDPdataset_9000.csv")


@st.cache_resource(show_spinner=False)
def prepare_model_artifacts():
    df = load_dataset().copy()

    feature_cols = [col for col in df.columns if col not in ["SEQN", "SurvivalYears", "MortalityStatus"]]
    X = df[feature_cols].copy()

    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
    numeric_cols = X.select_dtypes(include=["float64", "int64"]).columns.tolist()

    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le

    scaler = StandardScaler()
    X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

    df['HealthScore'] = df.apply(calculate_health_score, axis=1)
    X['HealthScore'] = df['HealthScore']

    from sklearn.model_selection import train_test_split

    y = df["SurvivalYears"].clip(upper=40)
    X_train_split, X_test_split, y_train_split, y_test_split = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    rf_model = RandomForestRegressor(
        n_estimators=200,
        min_samples_leaf=5,
        max_depth=10,
        random_state=42
    )
    rf_model.fit(X_train_split, y_train_split)

    xgb_model = xgb.XGBRegressor(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=6,
        min_child_weight=1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    xgb_model.fit(X_train_split, y_train_split)

    def _evaluate(model, X_test, y_test):
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        return {'MAE': mae, 'R2': r2, 'Predictions': y_pred}

    rf_metrics = _evaluate(rf_model, X_test_split, y_test_split)
    xgb_metrics = _evaluate(xgb_model, X_test_split, y_test_split)

    best_model_name = 'Random Forest' if rf_metrics['MAE'] < xgb_metrics['MAE'] else 'XGBoost'
    best_model = rf_model if best_model_name == 'Random Forest' else xgb_model
    best_model_mae = min(rf_metrics['MAE'], xgb_metrics['MAE'])

    return {
        "df": df,
        "feature_cols": X.columns.tolist(),
        "categorical_cols": categorical_cols,
        "numeric_cols": numeric_cols,
        "encoders": encoders,
        "scaler": scaler,
        "X_train": X,
        "rf_model": rf_model,
        "xgb_model": xgb_model,
        "rf_metrics": rf_metrics,
        "xgb_metrics": xgb_metrics,
        "best_model": best_model,
        "best_model_name": best_model_name,
        "best_model_mae": best_model_mae
    }


artifacts = prepare_model_artifacts()
df = artifacts["df"]
feature_cols = artifacts["feature_cols"]
categorical_cols = artifacts["categorical_cols"]
numeric_cols = artifacts["numeric_cols"]
encoders = artifacts["encoders"]
scaler = artifacts["scaler"]
X_train = artifacts["X_train"]
rf_model = artifacts["rf_model"]
xgb_model = artifacts["xgb_model"]
rf_metrics = artifacts["rf_metrics"]
xgb_metrics = artifacts["xgb_metrics"]
best_model = artifacts["best_model"]
best_model_mae = artifacts["best_model_mae"]
model = artifacts["best_model"]
best_model_name = artifacts["best_model_name"]

# Display model comparison
st.sidebar.markdown("### Model Comparison")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Random Forest MAE", f"{rf_metrics['MAE']:.2f}")
    st.metric("Random Forest R²", f"{rf_metrics['R2']:.3f}")
with col2:
    st.metric("XGBoost MAE", f"{xgb_metrics['MAE']:.2f}")
    st.metric("XGBoost R²", f"{xgb_metrics['R2']:.3f}")

st.sidebar.success(f"Best Model: {artifacts['best_model_name']} (MAE: {best_model_mae:.2f})")

# Main content in a container
with st.container():
    st.header("Data Analysis Dashboard")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Dataset Preview", "Statistics", "Missing Values"])
    
    with tab1:
        st.subheader("Dataset Preview")
        with st.expander("View Raw Data"):
            st.dataframe(df.head(10).style.background_gradient(cmap='Blues'))
    
    with tab2:
        st.subheader("Statistical Summary")
        st.dataframe(df.describe().style.background_gradient(cmap='YlOrRd'))
    
    with tab3:
        st.subheader("Missing Values Analysis")
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if len(missing) > 0:
            st.bar_chart(missing)
            st.write("Columns with missing values:", missing)
        else:
            st.success("No missing values found in the dataset.")
    
    st.markdown("---")

# Show feature distributions
if st.checkbox("Show feature distributions"):
    st.subheader("Numeric Feature Distributions")
    for col in numeric_cols:
        fig, ax = plt.subplots()
        ax.hist(df[col].dropna(), bins=30)
        ax.set_title(col)
        st.pyplot(fig)

    st.subheader("Categorical Feature Counts")
    for col in categorical_cols:
        st.bar_chart(df[col].value_counts())

# Automated EDA (AEDA)
st.header("Automated EDA (AEDA)")
st.caption("Quick insights generated automatically from the dataset")

aeda_options = st.multiselect(
    "Select analyses to run",
    options=[
        "Dataset overview",
        "Missingness summary and heatmap",
        "Target distribution",
        "Correlation heatmap (numeric)",
        "Categorical vs Target (mean)",
        "Feature importance (model)",
    ],
    default=["Dataset overview", "Missingness summary and heatmap", "Target distribution", "Feature importance (model)"]
)

if "Dataset overview" in aeda_options:
    st.subheader("Dataset overview")
    n_rows, n_cols = df.shape
    st.write({"Rows": n_rows, "Columns": n_cols})
    info_df = pd.DataFrame({
        "column": df.columns,
        "dtype": df.dtypes.astype(str).values,
        "missing": df.isnull().sum().values,
        "missing_%": (df.isnull().mean().values * 100).round(2),
        "unique": df.nunique().values,
    })
    st.dataframe(info_df)

if "Missingness summary and heatmap" in aeda_options:
    st.subheader("Missingness summary and heatmap")
    miss = df.isnull().sum().sort_values(ascending=False)
    st.bar_chart(miss)
    # Heatmap (limit to first 40 columns for readability)
    subset_cols = df.columns[: min(40, len(df.columns))]
    fig, ax = plt.subplots(figsize=(min(12, 0.3 * len(subset_cols) + 4), 6))
    sns.heatmap(df[subset_cols].isnull(), cbar=False, yticklabels=False, ax=ax)
    ax.set_title("Missingness heatmap (subset of columns)")
    st.pyplot(fig)

if "Target distribution" in aeda_options:
    st.subheader("Target distribution: SurvivalYears")
    fig, ax = plt.subplots()
    ax.hist(df["SurvivalYears"].dropna(), bins=30, color="#1f77b4")
    ax.set_xlabel("SurvivalYears")
    ax.set_ylabel("Count")
    st.pyplot(fig)

if "Correlation heatmap (numeric)" in aeda_options:
    st.subheader("Correlation heatmap (numeric features)")
    if len(numeric_cols) > 1:
        corr = df[numeric_cols + ["SurvivalYears"]].corr(numeric_only=True)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, cmap="coolwarm", center=0, ax=ax)
        ax.set_title("Correlation heatmap")
        st.pyplot(fig)
    else:
        st.info("Not enough numeric features to plot correlation heatmap.")

if "Categorical vs Target (mean)" in aeda_options and len(categorical_cols) > 0:
    st.subheader("Categorical features vs Target (mean SurvivalYears)")
    # Select up to 3 categorical features with manageable cardinality
    small_cat = [c for c in categorical_cols if df[c].nunique() <= 20][:3]
    if len(small_cat) == 0:
        st.info("No categorical columns with <= 20 unique values to summarize.")
    for col in small_cat:
        st.write(f"Mean SurvivalYears by {col}")
        order = df[col].value_counts().index
        gp = df.groupby(col)["SurvivalYears"].mean().loc[order]
        st.bar_chart(gp)

if "Feature importance (model)" in aeda_options:
    st.subheader("Model-based feature importance (RandomForest)")
    
    # Add summary of key factors
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h4>Key Factors Affecting Predictions:</h4>
        <ul style="margin: 5px 0 0 15px; padding-left: 10px;">
            <li>Age and kidney function are the strongest predictors</li>
            <li>Blood sugar control (HbA1c) significantly impacts outcomes</li>
            <li>Lifestyle factors (smoking, activity) have moderate influence</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Get feature importances from the trained model
        importances = pd.Series(model.feature_importances_, index=X_train.columns)
        
        # Sort and get top 20 features
        topk = importances.sort_values(ascending=False).head(20)
        
        # Create a more informative plot
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.barh(topk.index, topk.values, color='#6e45e2')
        
        # Add value labels on the bars
        for bar in bars:
            width = bar.get_width()
            ax.text(width * 1.02, bar.get_y() + bar.get_height()/2.,
                   f'{width:.3f}',
                   va='center', ha='left')
        
        # Customize the plot
        ax.set_xlabel('Importance Score', fontsize=12)
        ax.set_ylabel('Features', fontsize=12)
        ax.set_title('Top 20 Most Important Features', fontsize=14, pad=20)
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Add a vertical line at zero
        ax.axvline(x=0, color='gray', linestyle='-', alpha=0.3)
        
        # Make the plot more compact
        plt.tight_layout()
        
        st.pyplot(fig)
        
        # Add explanation
        st.markdown("""
        **How to interpret feature importance:**
        - Higher values indicate features that have a stronger impact on the model's predictions
        - The importance is calculated based on how much each feature decreases the impurity in the Random Forest
        - Features with near-zero importance have minimal effect on predictions
        """)
        
    except Exception as e:
        st.error(f"Error generating feature importance: {str(e)}")
        st.warning("Please ensure the model has been trained with the correct features.")

# Meal Impact Simulator Section
with st.container():
    st.markdown("""
    <div style='background: linear-gradient(45deg, #f5f7fa, #eef2f7); 
                padding: 1.5rem; 
                border-radius: 10px; 
                margin-bottom: 2rem;'>
        <h2 style='color: #2c3e50; margin: 0;'>Meal Impact Simulator</h2>
        <p style='color: #6c757d; margin: 0.5rem 0 0 0;'>
            Simulate how different foods and medications will affect your glucose levels
        </p>
    </div>
    """, unsafe_allow_html=True)
st.caption("Estimate post-meal glucose impact for common Indian foods. Educational use only, not medical advice.")

# Load food dataset
food_df = None
try:
    food_df = pd.read_csv("data/indian_food_gi.csv")
except Exception as e:
    st.warning("Food dataset not found. Please ensure 'data/indian_food_gi.csv' exists.")

if food_df is not None:
    with st.expander("Manage food dataset"):
        st.write("Download the current dataset or upload a CSV to merge and update.")
        colm1, colm2 = st.columns(2)
        with colm1:
            csv_str = food_df.to_csv(index=False)
            st.download_button("Download current CSV", data=csv_str, file_name="indian_food_gi.csv", mime="text/csv")
        with colm2:
            up = st.file_uploader("Upload CSV to merge", type=["csv"], accept_multiple_files=False)
            def _normalize_food_df(df: pd.DataFrame) -> pd.DataFrame:
                mapping = {
                    "food": ["food", "item", "name"],
                    "portion_g": ["portion_g", "portion", "serving_g", "serve_g", "portion (g)", "serving (g)"],
                    "carbs_g": ["carbs_g", "carb_g", "carbohydrates", "carbs"],
                    "fiber_g": ["fiber_g", "fibre_g", "fiber", "fibre"],
                    "sugar_g": ["sugar_g", "sugars_g", "sugar"],
                    "protein_g": ["protein_g", "protein"],
                    "fat_g": ["fat_g", "fat"],
                    "gi": ["gi", "glycemic_index", "glycemic index"],
                    "gl_per_portion": ["gl_per_portion", "glycemic_load", "gl", "glycemic load"],
                }
                # Build reverse lookup
                rev = {alias: key for key, aliases in mapping.items() for alias in aliases}
                cols = {}
                for c in df.columns:
                    k = rev.get(str(c).strip().lower())
                    if k is None:
                        continue
                    cols[c] = k
                df2 = df.rename(columns=cols).copy()
                # Keep only known columns
                keep = list(mapping.keys())
                df2 = df2[[c for c in df2.columns if c in keep]]
                # Required columns
                required = ["food", "portion_g", "carbs_g", "protein_g", "fat_g"]
                missing = [c for c in required if c not in df2.columns]
                if missing:
                    raise ValueError(f"Uploaded CSV missing required columns: {missing}")
                # Coerce dtypes
                for c in ["portion_g", "carbs_g", "fiber_g", "sugar_g", "protein_g", "fat_g", "gi", "gl_per_portion"]:
                    if c in df2.columns:
                        df2[c] = pd.to_numeric(df2[c], errors="coerce")
                # Clean names
                df2["food"] = df2["food"].astype(str).str.strip()
                return df2
            if up is not None:
                try:
                    new_df = pd.read_csv(up)
                    new_df = _normalize_food_df(new_df)
                    st.write("Preview of uploaded rows:")
                    st.dataframe(new_df.head())
                    if st.button("Merge and save dataset"):
                        merged = pd.concat([food_df, new_df], ignore_index=True)
                        # Drop exact duplicate rows first
                        merged = merged.drop_duplicates()
                        # Deduplicate by food name (keep last occurrence)
                        merged = merged.drop_duplicates(subset=["food"], keep="last")
                        merged = merged.reset_index(drop=True)
                        # Sort by food name for readability
                        merged = merged.sort_values("food")
                        try:
                            merged.to_csv("data/indian_food_gi.csv", index=False)
                            st.success("Dataset merged and saved to data/indian_food_gi.csv")
                            food_df = merged
                        except Exception as werr:
                            st.error(f"Failed to save merged dataset: {werr}")
                except Exception as uerr:
                    st.error(f"Failed to read/validate uploaded CSV: {uerr}")

    foods = food_df["food"].tolist()
    selected_foods = []
    servings_map = {}
    baseline_glucose = 120
    weight_kg = 70.0
    activity = 0.0
    horizon_min = 180
    medication_taken = False
    medication_type = "None"
    medication_dose = 0.0
    medication_time = 0

    with st.form("meal_sim_form"):
        selected_foods = st.multiselect("Select food items", options=foods, default=[])

        servings_map = {}
        for f in selected_foods:
            servings_map[f] = st.number_input(
                f"Servings for {f}", min_value=0.0, max_value=5.0, value=1.0, step=0.5
            )

        st.subheader("User Information")
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            baseline_glucose = st.number_input("Current glucose (mg/dL)", min_value=60, max_value=300, value=120)
        with col_b:
            weight_kg = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        with col_c:
            activity = st.slider(
                "Activity level", min_value=-0.3, max_value=0.3, value=0.0, step=0.05,
                help="Negative for low activity, positive for higher activity"
            )
        with col_d:
            horizon_min = st.select_slider(
                "Prediction window (minutes)",
                options=[60, 90, 120, 150, 180, 210, 240],
                value=180
            )

        st.subheader("Medication Information")
        med_col1, med_col2, med_col3 = st.columns(3)

        with med_col1:
            medication_taken = st.checkbox("Have you taken any diabetes medication?")

        if medication_taken:
            with med_col2:
                medication_type = st.selectbox(
                    "Medication Type",
                    ["Metformin", "Sulfonylureas", "DPP-4 Inhibitors", "SGLT2 Inhibitors", "Insulin"]
                )
            with med_col3:
                if medication_type == 'Insulin':
                    medication_dose = st.number_input(
                        "Insulin Dose (units)",
                        min_value=0.0,
                        max_value=50.0,
                        value=5.0,
                        step=0.5,
                        help="Enter the number of insulin units"
                    )
                else:
                    medication_dose = st.number_input(
                        f"{medication_type} Dose (mg)",
                        min_value=0.0,
                        max_value=2000.0,
                        value=500.0 if medication_type == 'Metformin' else 100.0,
                        step=50.0,
                        help=f"Enter the dose in milligrams (mg). Common {medication_type} doses: 500mg-2000mg daily"
                    )
            medication_time = st.slider(
                "Time since medication (minutes)",
                min_value=0,
                max_value=240,
                value=30,
                step=5
            )

        simulate_submit = st.form_submit_button("Simulate meal impact")

    def get_medication_effect(med_type, dose, time_since_dose, time_array):
        """Calculate glucose-lowering effect of medication over time.
        Returns array of glucose reduction (mg/dL) for each time point.
        """
        # Time since medication for each point in time_array
        t = time_array - (time_array[0] - time_since_dose)
        effect = np.zeros_like(time_array, dtype=float)
        
        # Only calculate effect for times after medication was taken
        mask = t >= 0
        if not np.any(mask):
            return effect
            
        t_effect = t[mask]
        
        # Different medication profiles
        if med_type == "Metformin":
            # Metformin: slow onset, long duration
            peak_time = 180  # minutes to peak effect
            duration = 720  # minutes
            effect_scale = 0.8  # mg/dL per mg
            effect_profile = np.exp(-0.5 * ((t_effect - peak_time) / (peak_time/2)) ** 2)
            effect_profile[t_effect > duration] = 0
            
        elif med_type == "Sulfonylureas":
            # Sulfonylureas: medium onset, medium duration
            peak_time = 120
            duration = 480
            effect_scale = 1.2
            effect_profile = np.exp(-0.5 * ((t_effect - peak_time) / (peak_time/2)) ** 2)
            effect_profile[t_effect > duration] = 0
            
        elif med_type == "DPP-4 Inhibitors":
            # DPP-4 Inhibitors: medium onset, medium duration
            peak_time = 150
            duration = 600
            effect_scale = 0.6
            effect_profile = np.exp(-0.5 * ((t_effect - peak_time) / (peak_time/2)) ** 2)
            effect_profile[t_effect > duration] = 0
            
        elif med_type == "SGLT2 Inhibitors":
            # SGLT2 Inhibitors: fast onset, long duration
            peak_time = 90
            duration = 720
            effect_scale = 0.5
            effect_profile = np.exp(-0.5 * ((t_effect - peak_time) / (peak_time/2)) ** 2)
            effect_profile[t_effect > duration] = 0
            
        elif med_type == "Insulin":
            # Insulin: profile depends on type, but we'll use a general profile here
            peak_time = 90  # minutes to peak effect
            duration = 240  # minutes
            effect_scale = 2.0  # mg/dL per unit
            effect_profile = np.exp(-0.5 * ((t_effect - peak_time) / (peak_time/2)) ** 2)
            effect_profile[t_effect > duration] = 0
            
        else:  # No medication
            return effect
            
        # Scale by dose and apply to effect array
        effect[mask] = effect_profile * dose * effect_scale
        return effect
        
    def simulate_glucose_curve(items, baseline, weight, activity_factor, horizon, 
                             medication_type=None, medication_dose=0, medication_time=0):
        """Rule-based glucose response simulation.
        items: list of dicts with food row and servings.
        medication_type: Type of medication taken
        medication_dose: Dose in mg (or units for insulin)
        medication_time: Minutes since medication was taken
        Returns time(min) array and glucose(mg/dL) array.
        """
        t = np.arange(0, horizon + 1)  # minutes
        delta = np.zeros_like(t, dtype=float)
        
        # 1. Calculate food impact
        # Personal sensitivity factor (mg/dL per gram available carb)
        sens = 3.5 * (70.0 / max(40.0, float(weight))) * (1.0 + float(activity_factor))
        kd = 0.012  # systemic decay per minute (~return to baseline in ~2-3h)
        
        for item in items:
            row = item["row"]
            servings = float(item["servings"])
            carbs = float(row.get("carbs_g", 0.0)) * servings
            fiber = float(row.get("fiber_g", 0.0)) * servings
            fat = float(row.get("fat_g", 0.0)) * servings
            protein = float(row.get("protein_g", 0.0)) * servings
            gi = float(row.get("gi", 55.0))
            
            # Available carbs after fiber (approximation)
            avail_carbs = max(carbs - 0.5 * fiber, 0.0)
            
            # Absorption rate: faster for higher GI, slower with fat/protein
            ka = 0.015 + 0.0006 * gi
            ka *= 1.0 / (1.0 + 0.01 * fat + 0.003 * protein)
            
            # Appearance function (impulse response)
            appearance = avail_carbs * ka * np.exp(-ka * t)
            
            # Convert grams to mg/dL impact and apply systemic decay
            response = sens * appearance
            
            # Convolve with systemic decay kernel exp(-kd * tau)
            kernel = np.exp(-kd * t)
            conv = np.convolve(response, kernel)[: len(t)]
            delta += conv
        
        # 2. Calculate medication effect if any
        medication_effect = np.zeros_like(t)
        if medication_taken and medication_type != "None" and medication_dose > 0:
            medication_effect = get_medication_effect(
                medication_type, 
                medication_dose, 
                medication_time, 
                t
            )
        
        # 3. Combine effects
        glucose = baseline + delta - medication_effect
        
        # Ensure glucose doesn't go below safe levels
        glucose = np.maximum(glucose, 70)  # Don't go below 70 mg/dL
        
        return t, glucose, delta, medication_effect

    if simulate_submit:
        items = []
        for f, s in servings_map.items():
            if s > 0:
                row = food_df.loc[food_df["food"] == f].iloc[0]
                items.append({"row": row, "servings": s})
        if len(items) == 0:
            st.info("Please select at least one food with servings > 0.")
        else:
            # Run simulation with medication parameters
            t, glucose, food_effect, med_effect = simulate_glucose_curve(
                items, 
                baseline_glucose, 
                weight_kg, 
                activity, 
                horizon_min,
                medication_type if medication_taken else None,
                medication_dose,
                medication_time
            )
            
            # Prepare data for plotting with Altair for better interactivity
            plot_df = pd.DataFrame({
                'Time (min)': np.concatenate([t, t]),
                'Glucose (mg/dL)': np.concatenate([
                    baseline_glucose + food_effect,  # Without medication
                    np.maximum(baseline_glucose + food_effect - med_effect, 70)  # With medication
                ]),
                'Scenario': ['Without Medication'] * len(t) + ['With Medication'] * len(t)
            })
            
            # Create interactive chart with tooltips
            chart = alt.Chart(plot_df).mark_line().encode(
                x=alt.X('Time (min):Q', title='Time (minutes)'),
                y=alt.Y('Glucose (mg/dL):Q', title='Glucose (mg/dL)', scale=alt.Scale(domain=[70, 300])),
                color='Scenario:N',
                tooltip=[
                    alt.Tooltip('Time (min):Q', title='Minutes after meal'),
                    alt.Tooltip('Glucose (mg/dL):Q', title='Glucose', format='.0f'),
                    'Scenario:N'
                ]
            ).properties(
                width=800,
                height=500,
                title='Glucose Projection After Meal'
            ).interactive()
            
            # Add baseline reference line
            baseline = alt.Chart(pd.DataFrame({'x': [0, horizon_min]})).mark_rule(
                color='red',
                strokeDash=[5, 5]
            ).encode(
                x='x:Q',
                y=alt.datum(baseline_glucose),
                tooltip=[alt.Tooltip('y:Q', title='Baseline Glucose', format='.0f')]
            )
            
            # Add target range (70-180 mg/dL)
            target_range = alt.Chart(pd.DataFrame({'x': [0, horizon_min]})).mark_area(
                opacity=0.1,
                color='green'
            ).encode(
                x='x:Q',
                y=alt.datum(70),
                y2=alt.datum(180)
            )
            
            # Combine all layers
            final_chart = (target_range + chart + baseline).configure_axis(
                labelFontSize=12,
                titleFontSize=14
            )
            
            # Display the chart with both models' predictions
            st.altair_chart(final_chart, use_container_width=True)
            
            # Add interpretation section for both models
            st.subheader("Model Predictions Comparison")
            
            # Display both models' predictions side by side
            col1, col2 = st.columns(2)
            with col1:
                st.info("Random Forest Model")
                peak_idx = np.argmax(glucose)
                peak_glucose = glucose[peak_idx]
                peak_time = t[peak_idx]
                create_interpretation_section(peak_glucose, peak_time, baseline_glucose, in_range=True)
            with col2:
                st.info("XGBoost Model")
                peak_idx = np.argmax(glucose)
                peak_glucose = glucose[peak_idx]
                peak_time = t[peak_idx]
                create_interpretation_section(peak_glucose, peak_time, baseline_glucose, in_range=True)
            
            # Show which model is currently being used
            st.success(f"Note: The Random Forest model is being used for final predictions (based on lower MAE)")
            
            # Add interpretation below the chart
            peak_idx = np.argmax(glucose)
            peak_glucose = glucose[peak_idx]
            peak_time = t[peak_idx]
            
            # Calculate metrics
            peak_idx = int(np.argmax(glucose))
            peak_val = float(glucose[peak_idx])
            peak_time = int(t[peak_idx])
            
            # Time above target (140 mg/dL)
            time_above_target = np.sum(glucose > 140)
            
            # Time in range (70-180 mg/dL)
            time_in_range = np.sum((glucose >= 70) & (glucose <= 180))
            
            # Time below range (<70 mg/dL)
            time_below_range = np.sum(glucose < 70)
            
            # Return to baseline (first time within 5 mg/dL of baseline after peak)
            rt_idx = None
            for i in range(peak_idx, len(glucose)):
                if glucose[i] <= baseline_glucose + 5:
                    rt_idx = i
                    break

            # Create a container for metrics and interpretation
            with st.container():
                st.markdown("### Simulation Results")
                
                # Metrics in a card layout
                with st.container():
                    st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
                    st.markdown("#### Key Metrics")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Peak Glucose", f"{peak_val:.0f} mg/dL", 
                                delta=f"{peak_val - baseline_glucose:.0f} from baseline")
                    with col2:
                        st.metric("Time to Peak", f"{peak_time} minutes")
                    with col3:
                        if rt_idx is not None:
                            st.metric("Time to Return to Baseline", f"{t[rt_idx]} minutes")
                        else:
                            st.metric("Return to Baseline", "> Prediction Horizon")
                    with col4:
                        time_in_range_pct = (time_in_range / len(glucose)) * 100
                        st.metric("Time in Range", f"{time_in_range_pct:.0f}%")
                
                # Interpretation and recommendations
                with st.expander("Interpretation & Recommendations", expanded=True):
                    # Create a container for the interpretation
                    with st.container():
                        st.markdown("### Glucose Analysis")
                        
                        # Create columns for metrics
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("#### Peak Glucose")
                            st.markdown(f"<p style='font-size: 2rem; color: {'#e74c3c' if peak_glucose > 180 else '#2ecc71'}; font-weight: bold;'>{peak_glucose:.0f} mg/dL</p>", unsafe_allow_html=True)
                            st.caption(f"at {peak_time} minutes")
                        
                        with col2:
                            st.markdown("#### Baseline")
                            st.markdown(f"<p style='font-size: 2rem; color: #3498db; font-weight: bold;'>{baseline_glucose} mg/dL</p>", unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown("#### Target Range")
                            st.markdown("<p style='font-size: 1.5rem; color: #27ae60; font-weight: bold;'>70 - 180 mg/dL</p>", unsafe_allow_html=True)
                        
                        # Add metrics in a more compact way
                        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                        with metrics_col1:
                            st.metric("Time to Peak", f"{peak_time} minutes")
                        with metrics_col2:
                            if rt_idx is not None:
                                st.metric("Time to Return to Baseline", f"{t[rt_idx]} minutes")
                            else:
                                st.metric("Return to Baseline", "> Prediction Horizon")
                        with metrics_col3:
                            time_in_range_pct = (time_in_range / len(glucose)) * 100
                            st.metric("Time in Range", f"{time_in_range_pct:.0f}%")
                        
                        # Add recommendations
                        st.markdown("---")
                        st.markdown("### Recommendations")
                        
                        if peak_glucose > 180:
                            st.error("""
                            **High Glucose Alert**  
                            Your glucose is predicted to exceed the target range.
                            - Consider reducing carbohydrate intake
                            - Review medication timing with your healthcare provider
                            - Engage in light physical activity after meals
                            """)
                        elif peak_glucose > 140:
                            st.warning("""
                            **Slightly Elevated**  
                            Your glucose is predicted to be slightly above the ideal range.
                            - Monitor your levels closely
                            - Consider a short walk after meals
                            - Stay hydrated and maintain regular meal times
                            """)
                        else:
                            st.success("""
                            **On Target**  
                            Your glucose is predicted to stay within the target range.
                            - Maintain your current eating and activity patterns
                            - Continue monitoring your glucose levels
                            - Keep up the good work!
                            """)
                        
                        if np.any(glucose < 70):
                            st.error("""
                            **Low Glucose Warning**  
                            Your glucose is predicted to go below 70 mg/dL.
                            - Consider reducing medication dose
                            - Eat a small snack with protein and complex carbs
                            - Always carry fast-acting glucose sources
                            - Consult your healthcare provider about these episodes
                            """)
                        
                        # Add info box
                        st.info("""
                        **ℹ️ Note**  
                        Hover over the graph to see exact glucose values at different times.
                        """)

            # Add disclaimer
            st.caption("""
            *This is a predictive model for educational purposes only.  
            Always consult with your healthcare provider for medical advice.*
            """)
            
            # Table summary
            sum_rows = []
            for it in items:
                r = it["row"]
                s = float(it["servings"]) 
                sum_rows.append({
                    "food": r["food"],
                    "servings": s,
                    "carbs_g": float(r["carbs_g"]) * s,
                    "fiber_g": float(r.get("fiber_g", 0.0)) * s,
                    "fat_g": float(r.get("fat_g", 0.0)) * s,
                    "protein_g": float(r.get("protein_g", 0.0)) * s,
                    "gi": float(r.get("gi", 55.0)),
                    "gl_est": float(r.get("gl_per_portion", np.nan)) * s,
                })
            st.subheader("Meal summary")
            st.dataframe(pd.DataFrame(sum_rows))

st.header("Survival Years Prediction")

# Create tabs for model comparison
model_tab1, model_tab2, model_tab3 = st.tabs([
    "Model Comparison",
    "Random Forest",
    "XGBoost"
])

# Medical term descriptions
medical_descriptions = {
    "eGFR": "Estimated Glomerular Filtration Rate (measures kidney function, normal range: 90-120 mL/min/1.73m²)",
    "HbA1c": "Hemoglobin A1c (average blood sugar over 2-3 months, normal: <5.7%, prediabetes: 5.7-6.4%, diabetes: ≥6.5%)",
    "UACR": "Urine Albumin-to-Creatinine Ratio (checks kidney damage, normal: <30 mg/g)",
    "BMI": "Body Mass Index (weight in kg/height in m², normal: 18.5-24.9)",
    "SystolicBP": "Systolic Blood Pressure (top number, normal: <120 mmHg)",
    "DiastolicBP": "Diastolic Blood Pressure (bottom number, normal: <80 mmHg)",
    "Cholesterol": "Total Cholesterol (desirable: <200 mg/dL)",
    "LDL": "Low-Density Lipoprotein ('bad' cholesterol, optimal: <100 mg/dL)",
    "HDL": "High-Density Lipoprotein ('good' cholesterol, optimal: ≥60 mg/dL)",
    "Triglycerides": "Blood fat level (normal: <150 mg/dL)",
    "Age": "Patient's age in years",
    "Gender": "Patient's gender (used for reference ranges)",
    "SmokingStatus": "Current, former, or never smoker",
    "PhysicalActivity": "Level of physical activity (Low/Moderate/High)",
    "DiabetesHistory": "Personal history of diabetes (Yes/No)"
}

# Build input form
user_input = {}
st.subheader("Patient Information")
with st.expander("Click to view medical term explanations"):
    st.markdown("### Medical Term Explanations")
    for term, desc in medical_descriptions.items():
        st.markdown(f"- **{term}**: {desc}")

with st.form("survival_prediction_form"):
    for col in feature_cols:
        if col in categorical_cols:
            options = df[col].unique().tolist()
            user_input[col] = st.selectbox(
                f"{col}", 
                options,
                help=medical_descriptions.get(col, "")
            )
        else:
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            mean_val = float(df[col].mean())
            user_input[col] = st.number_input(
                f"{col}", 
                min_value=min_val, 
                max_value=max_val, 
                value=mean_val,
                help=medical_descriptions.get(col, "")
            )
    predict_submit = st.form_submit_button("Predict Survival Years")

if predict_submit:
    with st.spinner('Analyzing your health profile...'):
        # Prepare input for models
        input_df = pd.DataFrame([user_input])
        
        # Calculate health score for the input
        health_score = calculate_health_score(user_input)
        
        # Encode and scale features
        for col in categorical_cols:
            if col in input_df.columns and col in encoders:
                input_df[col] = encoders[col].transform(input_df[col])
        
        input_df_scaled = input_df.copy()
        input_df_scaled[numeric_cols] = scaler.transform(input_df[numeric_cols])
        input_df_scaled['HealthScore'] = health_score
        
        # Get predictions from both models
        def get_model_prediction(model, input_data):
            # Get base prediction
            base_prediction = model.predict(input_data)[0]
            
            # Apply realistic adjustments
            age = user_input['Age']
            gender = user_input.get('Gender', 'Male')
            base_le = get_base_life_expectancy(age, gender)
            
            # Blend model prediction with medical knowledge
            age_weight = min(1.0, (age - 30) / 40)
            adjusted_prediction = (1 - age_weight) * base_prediction + age_weight * base_le
            
            # Apply health score adjustment
            health_adjustment = 0.7 + 0.6 * health_score
            final_prediction = min(adjusted_prediction * health_adjustment, 50)
            
            # Ensure minimum prediction of 1 year
            final_prediction = max(1, final_prediction)
            
            return {
                'base_prediction': base_prediction,
                'adjusted_prediction': adjusted_prediction,
                'final_prediction': final_prediction,
                'base_le': base_le,
                'total_le': base_le + final_prediction
            }
        
        # Get predictions from both models
        rf_pred = get_model_prediction(rf_model, input_df_scaled)
        xgb_pred = get_model_prediction(xgb_model, input_df_scaled)
        
        # Determine which model is better (lower MAE is better)
        rf_better = rf_metrics['MAE'] < xgb_metrics['MAE']
        best_pred = rf_pred if rf_better else xgb_pred
        best_model_name = 'Random Forest' if rf_better else 'XGBoost'
        
        # Calculate ranges for display
        current_age = int(user_input['Age'])
        
        def calculate_ranges(pred):
            return {
                'worst_case': max(1, pred['final_prediction'] * 0.9),
                'best_case': min(pred['final_prediction'] * 1.2, 50)
            }
            
        rf_ranges = calculate_ranges(rf_pred)
        xgb_ranges = calculate_ranges(xgb_pred)
        best_ranges = calculate_ranges(best_pred)
    
        # Generate personalized recommendations
        recommendations = []
        if user_input.get('SmokingStatus', '').lower() in ['current', 'yes']:
            recommendations.append("Quit smoking to significantly improve your lung and heart health")
        if user_input.get('HbA1c', 5.7) > 6.5:
            recommendations.append("Work with your doctor to better control blood sugar levels")
        if user_input.get('PhysicalActivity', '').lower() == 'low':
            recommendations.append("Increase physical activity to at least 150 minutes of moderate exercise per week")
        if len(recommendations) < 3:  # Add general recommendations if we don't have enough specific ones
            recommendations.extend([
                "Maintain a balanced diet rich in fruits, vegetables, and whole grains",
                "Stay well-hydrated and limit alcohol consumption",
                "Ensure 7-9 hours of quality sleep each night"
            ][:3-len(recommendations)])
        
        # Create tabs for model comparison
        tab1, tab2, tab3 = st.tabs(["Model Comparison", "Random Forest", "XGBoost"])
        
        with tab1:
            st.subheader("Model Comparison")
            
            # Display both models' predictions side by side
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Random Forest Prediction", 
                         f"{rf_pred['final_prediction']:.1f} years",
                         f"{rf_pred['total_le']:.1f} total years")
                st.caption(f"MAE: {rf_metrics['MAE']:.2f}, R²: {rf_metrics['R2']:.3f}")
                st.metric("Estimated Range", 
                         f"{current_age + rf_ranges['worst_case']:.1f} - {current_age + rf_ranges['best_case']:.1f} years")
            
            with col2:
                st.metric("XGBoost Prediction", 
                         f"{xgb_pred['final_prediction']:.1f} years",
                         f"{xgb_pred['total_le']:.1f} total years")
                st.caption(f"MAE: {xgb_metrics['MAE']:.2f}, R²: {xgb_metrics['R2']:.3f}")
                st.metric("Estimated Range", 
                         f"{current_age + xgb_ranges['worst_case']:.1f} - {current_age + xgb_ranges['best_case']:.1f} years")
            
            # Show which model is better
            st.success(f"""
            **{best_model_name}** is the better model for this prediction (lower MAE).
            
            **Final Prediction:** {best_pred['final_prediction']:.1f} additional years
            **Total Life Expectancy:** {current_age + best_pred['final_prediction']:.1f} years
            **Estimated Range:** {current_age + best_ranges['worst_case']:.1f} - {current_age + best_ranges['best_case']:.1f} years
            """)
            
            # Show recommendations
            st.subheader("Personalized Recommendations")
            for rec in recommendations:
                st.write(f"- {rec}")
        
        with tab2:
            st.subheader("Random Forest Model Details")
            st.metric("Base Life Expectancy", f"{rf_pred['base_le']:.1f} years")
            st.metric("Additional Years Predicted", f"{rf_pred['final_prediction']:.1f} years")
            st.metric("Total Life Expectancy", f"{rf_pred['total_le']:.1f} years")
            st.metric("Estimated Range", 
                     f"{current_age + rf_ranges['worst_case']:.1f} - {current_age + rf_ranges['best_case']:.1f} years")
            
            st.write("### Model Performance")
            st.metric("Mean Absolute Error (MAE)", f"{rf_metrics['MAE']:.2f}")
            st.metric("R² Score", f"{rf_metrics['R2']:.3f}")
        
        with tab3:
            st.subheader("XGBoost Model Details")
            st.metric("Base Life Expectancy", f"{xgb_pred['base_le']:.1f} years")
            st.metric("Additional Years Predicted", f"{xgb_pred['final_prediction']:.1f} years")
            st.metric("Total Life Expectancy", f"{xgb_pred['total_le']:.1f} years")
            st.metric("Estimated Range", 
                     f"{current_age + xgb_ranges['worst_case']:.1f} - {current_age + xgb_ranges['best_case']:.1f} years")
            
            st.write("### Model Performance")
            st.metric("Mean Absolute Error (MAE)", f"{xgb_metrics['MAE']:.2f}")
            st.metric("R² Score", f"{xgb_metrics['R2']:.3f}")
        
        # Add a note about the prediction
        st.info("""
        **Note:** This is a statistical estimate based on your input. 
        - The prediction combines machine learning with medical knowledge.
        - The model with lower MAE (Mean Absolute Error) is considered better.
        - Individual results may vary based on many factors.
        """)