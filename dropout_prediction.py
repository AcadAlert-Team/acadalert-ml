from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# 1. Load the EXACT filenames from your spec
try:
    model = joblib.load('dropout_risk_model.pkl')
    le = joblib.load('label_encoder.pkl')
except Exception as e:
    print(f"Error loading model files: {e}")

# 2. Match the EXACT feature names from your spec
class StudentFeatures(BaseModel):
    attendance_rate: float
    test_scores: float
    backlogs: int
    assignment_score: float

@app.post("/predict-dropout")
def predict_dropout(data: StudentFeatures):
    try:
        # 3. Use a Pandas DataFrame to maintain feature names and order
        # This prevents warnings if the model was trained on a DataFrame
        features = pd.DataFrame([{
            "attendance_rate": data.attendance_rate,
            "test_scores": data.test_scores,
            "backlogs": data.backlogs,
            "assignment_score": data.assignment_score
        }])
        
        # Make the prediction (Pipeline handles imputation/scaling automatically)
        prediction = model.predict(features)
        
        # Decode the integer back to text ('low', 'medium', 'high')
        risk_label = le.inverse_transform(prediction)[0] 
        
        # Generate custom insights based on the decoded label
        if risk_label == 'high':
            insight = "Immediate attention required. Historical data flags high dropout risk."
        elif risk_label == 'medium':
            insight = "Student needs monitoring. Risk is elevated."
        else:
            insight = "On track. Keep up the good work!"

        return {
            "risk_level": risk_label.upper(), # Uppercase for the frontend UI consistency
            "ai_insight": insight
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))