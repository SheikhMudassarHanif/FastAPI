from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import joblib
import numpy as np
# import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")   # Use a non-GUI backend
import matplotlib.pyplot as plt

from sklearn import tree
import io

# Initialize FastAPI
app = FastAPI(title="Iris Classifier API")

# Load saved model
model = joblib.load("iris_classifier.pkl")

# Define input schema
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Prediction endpoint
@app.post("/predict")
def predict_iris(data: IrisInput):
    features = np.array([[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]])
    prediction = model.predict(features)[0]
    class_names = ["Setosa", "Versicolor", "Virginica"]
    return {
        "prediction": int(prediction),
        "class_name": class_names[prediction]
    }

# Visualization endpoint
@app.get("/visualize")
def visualize_tree():
    fig, ax = plt.subplots(figsize=(12, 8))
    tree.plot_tree(model, filled=True, feature_names=["sepal_length", "sepal_width", "petal_length", "petal_width"], class_names=["Setosa", "Versicolor", "Virginica"])
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return StreamingResponse(buf, media_type="image/png")

# Health check endpoint
@app.get("/")
def root():
    return {"message": "Iris Classifier is running!"}
