# agents/health_monitor.py

import joblib
import pandas as pd

class HealthMonitorAgent:
    def __init__(self):
        self.model = joblib.load('models/health_model.pkl')

    def get_vital_signs(self):
        # read and return sensor data
        return {
            "Heart Rate": 105,
            "BP_Systolic": 150,
            "Glucose Levels": 180,
            "Oxygen Saturation (SpO₂%)": 94
        }

    def check_abnormalities(self, vitals):
        input_df = pd.DataFrame([vitals])
        prediction = self.model.predict(input_df)[0]
        if prediction == 1:
            return ["🩺 Abnormal health pattern detected by ML model."]
        return []

    def run(self):
        vitals = self.get_vital_signs()
        alerts = self.check_abnormalities(vitals)
        return alerts
