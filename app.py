import numpy as np
import pickle
import sys  # System arguments handle karne ke liye
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

# Model load karein
model = pickle.load(open("housing-prices-model.pkl", "rb"))

class HouseFeatures(BaseModel):
    bedroom_count: int
    net_sqm: float
    center_distance: float
    metro_distance: float
    age: int

@app.get("/ping")
async def ping():
    # SageMaker expects 200 OK for health check
    return {"status": "ok"}

@app.post("/invocations")
async def invocations(request: Request):
    payload = await request.json()
    
    # SageMaker data flexibility ke liye
    if 'features' in payload:
        data = payload['features']
    else:
        data = payload # Agar direct JSON data hai
    
    features = np.array([data])
    prediction = model.predict(features)
    return {"prediction": float(prediction[0])}

# Local testing ke liye purana predict endpoint
@app.post("/predict")
async def predict(data: HouseFeatures):
    final_features = np.array([[
        data.bedroom_count, data.net_sqm, 
        data.center_distance, data.metro_distance, data.age
    ]])
    prediction = model.predict(final_features)
    return {"predicted_price": round(prediction[0], 2)}

if __name__ == "__main__":
    import uvicorn
    # SageMaker 'serve' command bhejta hai, use ignore karne ke liye port fix rakhein
    uvicorn.run(app, host="0.0.0.0", port=8080)