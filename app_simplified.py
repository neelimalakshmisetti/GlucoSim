import streamlit as st
import pandas as pd
import numpy as np
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
            box-shadow: 0 0 0 2px rgba(110, 69, 226, 0.2);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main title
st.title("🍽️ Glucose Meal Impact Simulator")
st.markdown("""
*Simulate how different foods and medications will affect your glucose levels*
""")

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
                    "gl_per_portion": ["gl_per_portion", "glucose_per_portion", "glucose_impact"]
                }
                # Rename columns to match expected names
                rename_dict = {}
                for target, possible in mapping.items():
                    for col in df.columns:
                        if col.lower().strip() in [p.lower().strip() for p in possible]:
                            rename_dict[col] = target
                            break
                df2 = df.rename(columns=rename_dict)
                # Ensure required columns exist
                for c in ["food", "portion_g", "carbs_g", "fiber_g", "sugar_g", "protein_g", "fat_g", "gi", "gl_per_portion"]:
                    if c not in df2.columns:
                        df2[c] = 0
                # Convert numeric columns
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
            
            # Display the chart
            st.altair_chart(final_chart, use_container_width=True)
            
            # Add interpretation section
            st.subheader("Simulation Results")
            
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
                        st.markdown(f"<p style='font-size: 2rem; color: {'#e74c3c' if peak_val > 180 else '#2ecc71'}; font-weight: bold;'>{peak_val:.0f} mg/dL</p>", unsafe_allow_html=True)
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
                    
                    if peak_val > 180:
                        st.error("""
                        **High Glucose Alert**  
                        Your glucose is predicted to exceed the target range.
                        - Consider reducing carbohydrate intake
                        - Review medication timing with your healthcare provider
                        - Engage in light physical activity after meals
                        """)
                    elif peak_val > 140:
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

else:
    st.error("Food dataset could not be loaded. Please ensure 'data/indian_food_gi.csv' exists in the correct location.")
