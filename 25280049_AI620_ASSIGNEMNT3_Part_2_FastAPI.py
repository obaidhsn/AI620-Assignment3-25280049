from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Load Model on Startup
model = joblib.load("pakwheels_svm_model.pkl")

app = FastAPI()

# Input Schema
class CarInput(BaseModel):
    city: str
    body: str
    year: float
    engine: float
    transmission: str
    fuel: str
    mileage: int


# Root Endpoint
@app.get("/")
def home():
    return {"message": "PakWheels Price Prediction API"}

# Prediction Endpoint
@app.post("/predict")
def predict(data: CarInput):

    # Convert input to DataFrame
    input_dict = data.model_dump()
    df = pd.DataFrame([input_dict])

    if any(field not in df.columns for field in ['city', 'body', 'year', 'engine', 'transmission', 'fuel']):
        return {"error": "Missing required fields. Please provide city, body, year, engine, transmission, and fuel."}

    # Reorder columns
    df = df[
        ['city', 'body', 'year', 'engine', 'transmission', 'fuel', 'mileage']
    ]

    # Prediction
    prediction = model.predict(df)[0]

    # Convert to label
    predicted_category = "High Price" if prediction == 1 else "Low Price"

    return {
        "Price Category": predicted_category
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)