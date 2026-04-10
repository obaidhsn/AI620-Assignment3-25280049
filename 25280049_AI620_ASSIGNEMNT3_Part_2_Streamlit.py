import streamlit as st
import requests
import pandas as pd

# API URL (FastAPI backend)
url = "http://localhost:8000/predict"

# Page Title
st.title("PakWheels Price Category Predictor")

st.write("Enter car details to predict whether it's a High or Low price car.")

# Load Pakwheels Dataset to get unique cities, body types, transmission types, and fuel types for dropdowns
@st.cache_data
def load_data():
    df = pd.read_csv("data-a2.csv", usecols=['city', 'body', 'transmission', 'fuel'])
    return df

pakwheels_df = load_data()

# Get unique values for dropdowns
unique_cities = sorted(pakwheels_df['city'].dropna().unique())
unique_bodies = sorted(pakwheels_df['body'].dropna().unique())
unique_transmissions = sorted(pakwheels_df['transmission'].dropna().unique())
unique_fuels = sorted(pakwheels_df['fuel'].dropna().unique())

# User Inputs
city = st.selectbox("City", unique_cities)
body = st.selectbox("Body Type", unique_bodies) 

year = st.number_input("Year", 1970, 2026, 2018)
engine = st.number_input("Engine (cc)", 600, 5000, 1300)
mileage = st.number_input("Mileage", 0, 500000, 45000)

transmission = st.selectbox("Transmission", unique_transmissions)
fuel = st.selectbox("Fuel", unique_fuels)

if st.button("Predict"):

    # Prepare JSON data
    data = {
        "city": city,
        "body": body,
        "year": float(year),
        "engine": float(engine),
        "transmission": transmission,
        "fuel": fuel,
        "mileage": int(mileage)
    }

    try:
        # Send POST request
        response = requests.post(url, json=data)

        if response.status_code == 200:
            result = response.json()

            st.success(f"Prediction: {result['Price Category']}")

        else:
            st.error("Error from API")

    except:
        st.error("Could not connect to FastAPI server")