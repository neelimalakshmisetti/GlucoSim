import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(
    page_title="Glucose Meal Impact Simulator",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.95)),
                        url('static/bg.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
        }
        
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.25) !important;
            backdrop-filter: blur(16px) saturate(180%);
            -webkit-backdrop-filter: blur(16px) saturate(180%);
            border-right: 1px solid rgba(255, 255, 255, 0.4);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            color: #2c3e50 !important;
        }
        
        .main .block-container {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.75));
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.25);
            padding: 2.8rem;
            margin: 2.5rem 1.5rem;
            box-shadow: 0 12px 35px 0 rgba(31, 38, 135, 0.1);
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-bottom: 1rem;
        }
        
        .stButton>button {
            background: linear-gradient(45deg, #6e45e2, #89d4cf);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(110, 69, 226, 0.3);
        }
        
        .metrics-container {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🍽️ Glucose Meal Impact Simulator")
st.markdown("*Simulate how different foods and medications will affect your glucose levels*")

food_df = None
try:
    food_df = pd.read_csv("data/indian_food_gi.csv")
except Exception as e:
    st.error("Food dataset not found. Please ensure 'data/indian_food_gi.csv' exists in the correct location.")

if food_df is not None:
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
        t = time_array - (time_array[0] - time_since_dose)
        effect = np.zeros_like(time_array, dtype=float)
        
        mask = t >= 0
        if not np.any(mask):
            return effect
            
        t_effect = t[mask]
        
        if med_type == "Metformin":
            peak_time = 180
            duration = 720
            effect_scale = 0.8
            effect_profile = np.exp(-0.5 * ((t_effect - peak_time) / (peak_time/2)) ** 2)
            effect_profile[t_effect > duration] = 0
            
        elif med_type == "Sulfonylureas":
            peak_time = 120
            duration = 480
            effect_scale = 1.2
            effect_profile = np.exp(-0.5 * ((t_effect - peak_time) / (peak_time/2)) ** 2)
            effect_profile[t_effect > duration] = 0
            
        elif med_type == "DPP-4 Inhibitors":
            peak_time = 150
            duration = 600
            effect_scale = 0.6
            effect_profile = np.exp(-0.5 * ((t_effect - peak_time) / (peak_time/2)) ** 2)
            effect_profile[t_effect > duration] = 0
            
        elif med_type == "SGLT2 Inhibitors":
            peak_time = 90
            duration = 720
            effect_scale = 0.5
            effect_profile = np.exp(-0.5 * ((t_effect - peak_time) / (peak_time/2)) ** 2)
            effect_profile[t_effect > duration] = 0
            
        elif med_type == "Insulin":
            peak_time = 90
            duration = 240
            effect_scale = 2.0
            effect_profile = np.exp(-0.5 * ((t_effect - peak_time) / (peak_time/2)) ** 2)
            effect_profile[t_effect > duration] = 0
            
        else:
            return effect
            
        effect[mask] = effect_profile * dose * effect_scale
        return effect
        
    def simulate_glucose_curve(items, baseline, weight, activity_factor, horizon, medication_type=None, medication_dose=0, medication_time=0):
        t = np.arange(0, horizon + 1)
        delta = np.zeros_like(t, dtype=float)
        
        sens = 3.5 * (70.0 / max(40.0, float(weight))) * (1.0 + float(activity_factor))
        kd = 0.012
        
        for item in items:
            row = item["row"]
            servings = float(item["servings"])
            carbs = float(row.get("carbs_g", 0.0)) * servings
            fiber = float(row.get("fiber_g", 0.0)) * servings
            fat = float(row.get("fat_g", 0.0)) * servings
            protein = float(row.get("protein_g", 0.0)) * servings
            gi = float(row.get("gi", 55.0))
            
            avail_carbs = max(carbs - 0.5 * fiber, 0.0)
            ka = 0.015 + 0.0006 * gi
            ka *= 1.0 / (1.0 + 0.01 * fat + 0.003 * protein)
            
            appearance = avail_carbs * ka * np.exp(-ka * t)
            response = sens * appearance
            
            kernel = np.exp(-kd * t)
            conv = np.convolve(response, kernel)[: len(t)]
            delta += conv
        
        medication_effect = np.zeros_like(t)
        if medication_taken and medication_type != "None" and medication_dose > 0:
            medication_effect = get_medication_effect(
                medication_type, 
                medication_dose, 
                medication_time, 
                t
            )
        
        glucose = baseline + delta - medication_effect
        glucose = np.maximum(glucose, 70)
        
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
            
            plot_df = pd.DataFrame({
                'Time (min)': np.concatenate([t, t]),
                'Glucose (mg/dL)': np.concatenate([
                    baseline_glucose + food_effect,
                    np.maximum(baseline_glucose + food_effect - med_effect, 70)
                ]),
                'Scenario': ['Without Medication'] * len(t) + ['With Medication'] * len(t)
            })
            
            chart = alt.Chart(plot_df).mark_line().encode(
                x=alt.X('Time (min):Q', title='Time (minutes)', scale=alt.Scale(domain=[0, horizon_min])),
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
            )
            
            baseline_chart = alt.Chart(pd.DataFrame({'x': [0, horizon_min]})).mark_rule(
                color='red',
                strokeDash=[5, 5]
            ).encode(
                x='x:Q',
                y=alt.datum(baseline_glucose),
                tooltip=[alt.Tooltip('y:Q', title='Baseline Glucose', format='.0f')]
            )
            
            target_range = alt.Chart(pd.DataFrame({'x': [0, horizon_min]})).mark_area(
                opacity=0.1,
                color='green'
            ).encode(
                x='x:Q',
                y=alt.datum(70),
                y2=alt.datum(180)
            )
            
            final_chart = (target_range + chart + baseline_chart).configure_axis(
                labelFontSize=12,
                titleFontSize=14
            )
            
            st.altair_chart(final_chart, use_container_width=True)
            
            st.subheader("Simulation Results")
            
            peak_idx = int(np.argmax(glucose))
            peak_val = float(glucose[peak_idx])
            peak_time = int(t[peak_idx])
            
            time_in_range = np.sum((glucose >= 70) & (glucose <= 180))
            time_in_range_pct = (time_in_range / len(glucose)) * 100
            
            rt_idx = None
            for i in range(peak_idx, len(glucose)):
                if glucose[i] <= baseline_glucose + 5:
                    rt_idx = i
                    break

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
                    st.metric("Time in Range", f"{time_in_range_pct:.0f}%")
            
            with st.expander("Interpretation & Recommendations", expanded=True):
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
                
                st.info("""
                    **ℹ️ Note**  
                    Hover over the graph to see exact glucose values at different times.
                    """)

            st.caption("""
                *This is a predictive model for educational purposes only.  
                Always consult with your healthcare provider for medical advice.*
                """)
            
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
