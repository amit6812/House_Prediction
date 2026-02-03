import streamlit as st
import boto3
import json

# Page Config
st.set_page_config(page_title="House Price Predictor")
st.title("🏡 House Price Prediction")

# Input Fields (matching your features: [bed, sqm, center_dist, metro_dist, age])
st.subheader("Enter House Details")
bed = st.number_input("Number of Bedrooms", min_value=1, max_value=10, value=3)
sqm = st.number_input("Area (Sq Meters)", min_value=10, value=120)
dist_center = st.number_input("Distance to City Center (km)", value=5.0)
dist_metro = st.number_input("Distance to Metro (km)", value=1.0)
age = st.number_input("House Age (Years)", value=5)

if st.button("Predict Price"):
    # 1. Prepare data
    payload = {"features": [bed, sqm, dist_center, dist_metro, age]}
    
    # Wrap everything in a try block to catch all errors
    try:
        # 2. Initialize Client
        client = boto3.client('sagemaker-runtime', region_name='eu-north-1')
        
        # 3. Call SageMaker
        response = client.invoke_endpoint(
            EndpointName="New-EndPoint",
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        result = json.loads(response['Body'].read().decode())
        
        # 4. Show result
        price = result['prediction']
        st.success(f"### Estimated Price: {price:,.2f} Rupees")
        
    except Exception as e:
        # This will show a helpful error if permissions or endpoint fail
        st.error(f"Prediction Error: {str(e)}")