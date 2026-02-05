if st.button("Predict Price"):
    # 1. Prepare data
    payload = {"features": [bed, sqm, dist_center, dist_metro, age]}
    
    # Wrap everything in a try block to catch all errors
    try:
        # 2. Initialize Client
        client = boto3.client('sagemaker-runtime', region_name='eu-north-1')
        
        # 3. Call SageMaker
        response = client.invoke_endpoint(
            EndpointName="MyNewEnd",
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        result = json.loads(response['Body'].read().decode())
        
        # 4. Show result
        price = result['prediction']
        st.success(f"### Estimated Price: ${price:,.2f}")
        
    except Exception as e:
        # This will show a helpful error if permissions or endpoint fail
        st.error(f"Prediction Error: {str(e)}")