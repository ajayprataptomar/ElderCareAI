import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load dataset
df = pd.read_csv("Dataset/health_monitoring.csv")
df = df.dropna()

# --- Feature Engineering ---

# Parse systolic from 'Blood Pressure' (e.g., "120/80" → 120)
df['BP_Systolic'] = df['Blood Pressure'].apply(lambda x: int(str(x).split('/')[0]))

# Input features
X = df[['Heart Rate', 'BP_Systolic', 'Glucose Levels', 'Oxygen Saturation (SpO₂%)']]

# Target
y = df['Alert Triggered (Yes/No)'].map({'Yes': 1, 'No': 0})

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, 'models/health_model.pkl')
print("✅ Health model saved to models/health_model.pkl")
