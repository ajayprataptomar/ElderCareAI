# agents/safety_agent.py

import joblib
import pandas as pd
import random

class SafetyAgent:
    def __init__(self):
        self.model = joblib.load("models/fall_model.pkl")
        self.movement_encoder = joblib.load("models/fall_movement_encoder.pkl")
        self.impact_encoder = joblib.load("models/fall_impact_encoder.pkl")

    def get_sensor_data(self):
        return {
            "Movement Activity": random.choice(["Walking", "Sitting", "Lying", "No Movement"]),
            "Impact Force Level": random.choice(["Low", "Medium", "High"]),
            "Post-Fall Inactivity Duration (Seconds)": random.randint(0, 300)
        }

    def predict_fall(self, data):
        try:
            encoded_movement = self.movement_encoder.transform([data["Movement Activity"]])[0]
            encoded_impact = self.impact_encoder.transform([data["Impact Force Level"]])[0]

            features = pd.DataFrame([{
                "Movement Encoded": encoded_movement,
                "Impact Encoded": encoded_impact,
                "Post-Fall Inactivity Duration (Seconds)": data["Post-Fall Inactivity Duration (Seconds)"]
            }])

            result = self.model.predict(features)[0]
            return result == 1
        except Exception as e:
            print("❌ Error in prediction:", e)
            return False

    def run(self):
        data = self.get_sensor_data()
        print("🔍 Simulated Sensor Data:", data)
        if self.predict_fall(data):
            return ["🚨 Fall detected by ML model! Immediate action needed."]
        return []
