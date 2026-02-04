import streamlit as st
import json
import joblib  # <--- Local model load karne ke liye
import numpy as np # <--- Data format sahi karne ke liye

# Page Config
st.set_page_config(page_title="House Price Predictor")
st.title("🏡 House Price Prediction")

# Input Fields
st.subheader("Enter House Details")
bed = st.number_input("Number of Bedrooms", min_value=1, max_value=10, value=3)
sqm = st.number_input("Area (Sq Meters)", min_value=10, value=120)
dist_center = st.number_input("Distance to City Center (km)", value=5.0)
dist_metro = st.number_input("Distance to Metro (km)", value=1.0)
age = st.number_input("House Age (Years)", value=5)

if st.button("Predict Price"):
    # Wrap everything in a try block to catch all errors
    try:
        # 1. Local Model Load karein 
        # (Dhyan rahe ki housing-prices-model.pkl file isi folder mein honi chahiye)
        model = joblib.load('housing-prices-model.pkl')
        
        # 2. Data ko prepare karein (Numpy array format)
        features = np.array([[bed, sqm, dist_center, dist_metro, age]])
        
        # 3. Prediction karein (Bina SageMaker ke)
        prediction = model.predict(features)
        
        # 4. Show result
        # Note: prediction[0] use kar rahe hain kyunki model array return karta hai
        st.success(f"### Estimated Price: {prediction[0]:,.2f} Rupees")
        
    except Exception as e:
        st.error(f"Prediction Error: {str(e)}")