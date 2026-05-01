# Glucose Meal Impact Simulator

A simplified Streamlit application that simulates post-meal glucose impact for common Indian foods.

## Features

- **Meal Impact Simulator**: Select Indian foods and portions to predict glucose response
- **Medication Integration**: Include diabetes medications in simulations  
- **Interactive Visualizations**: Real-time glucose curves with Altair charts
- **Personalized Recommendations**: Get health advice based on predictions
- **Food Database Management**: Upload/download custom food datasets

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Required Files

- `app.py` - Main application
- `data/indian_food_gi.csv` - Food nutrition database
- `static/bg.jpg` - Background image (optional)

## Dependencies

- streamlit>=1.24.0
- pandas>=1.5.0  
- numpy>=1.21.0
- altair>=4.2.0

## Usage

1. Select food items and serving sizes
2. Enter personal health information
3. Add medication details if applicable
4. Click "Simulate meal impact" to see results
5. Review glucose projections and recommendations

*Educational use only. Always consult healthcare providers for medical advice.*

