import streamlit as st
import json
import boto3 


# Page Config
st.set_page_config(page_title="🏠House Prediction")
st.title("🏠 Smart House Price Predictor")

# --- Input Fields
st.subheader("Enter House Details")
col1, col2 = st.columns(2)

with col1:
    bed = st.number_input("Number of Bedrooms", min_value=1, step=1, value=3)
    sqm = st.number_input("Area (Sq Meters)", min_value=10, value=120)
    age = st.number_input("House Age (Years)", min_value=0, value=5)

with col2:
    dist_center = st.number_input("Distance to Center (km)", min_value=0.0, value=5.0)
    dist_metro = st.number_input("Distance to Metro (km)", min_value=0.0, value=1.0)

# --- Prediction Logic ---
if st.button("Predict Price"):
    # 1. Prepare data (Payload)
    payload = {"features": [bed, sqm, dist_center, dist_metro, age]}
    
    try:
        # 2. Initialize Client
        # Ensure your EC2 has IAM permissions for SageMaker
        client = boto3.client('sagemaker-runtime', region_name='eu-north-1')
        
        # 3. Call SageMaker Endpoint
        response = client.invoke_endpoint(
            EndpointName="MyNewEnd",
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        
        # 4. Parse Result
        result = json.loads(response['Body'].read().decode())
        price = result['prediction']
        
        st.balloons()
        st.success(f"### Estimated Price: ${price:,.2f}")
        
    except Exception as e:
        st.error(f"Prediction Error: {str(e)}")