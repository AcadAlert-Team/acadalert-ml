from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Load artifacts
try:
    model = joblib.load("dropout_risk_model.pkl")
    scaler = joblib.load("feature_scaler.pkl")
    encoder = joblib.load("label_encoder.pkl")
except Exception as e:
    print(f"Error loading model files: {e}")

# 1. Updated variable names to match your spec exactly
class StudentData(BaseModel):
    attendance_rate: float
    test_scores: float
    backlogs: int
    assignment_score: float

@app.post("/predict-dropout")
def predict_dropout(data: StudentData):
    try:
        # 2. CRITICAL: Fixed the order to match your pipeline
        # [attendance_rate, test_scores, backlogs, assignment_score]
        features = np.array([[
            data.attendance_rate, 
            data.test_scores, 
            data.backlogs, 
            data.assignment_score
        ]])

        # Scale features
        scaled_features = scaler.transform(features)

        # Predict class (0, 1, or 2)
        prediction = model.predict(scaled_features)
        risk_label = encoder.inverse_transform(prediction)[0]

        # 3. Extract confidence probabilities
        # predict_proba returns a 2D array, we grab the first row [0]
        probabilities = model.predict_proba(scaled_features)[0]
        
        # Map probabilities to their corresponding labels
        # encoder.classes_ usually looks like ['High', 'Low', 'Medium'] depending on training
        classes = encoder.classes_
        confidence = {
            classes[i]: round(float(probabilities[i]) * 100, 2) 
            for i in range(len(classes))
        }

        # Generate insight
        if risk_label == 'High':
            ai_insight = "Immediate attention required. High risk of dropout predicted."
        elif risk_label == 'Medium':
            ai_insight = "Warning signs present, needs attention."
        else:
            ai_insight = "Student is academically stable."

        return {
            "risk_label": risk_label,
            "confidence": confidence,
            "ai_insight": ai_insight
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))