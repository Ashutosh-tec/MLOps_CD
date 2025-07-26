# filename: main.py
from fastapi import FastAPI, Query
import joblib
import numpy as np

# Load the saved model
model = joblib.load("model.joblib")

# Initialize FastAPI app
app = FastAPI(title="Iris Prediction API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Iris Prediction API!"}

@app.get("/predict")
def predict(
    sepal_length: float = Query(..., description="Sepal length"),
    sepal_width: float = Query(..., description="Sepal width"),
    petal_length: float = Query(..., description="Petal length"),
    petal_width: float = Query(..., description="Petal width")
):
    # Prepare the input data for prediction
    input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    prediction = model.predict(input_data)
    return {"prediction": prediction[0]}

