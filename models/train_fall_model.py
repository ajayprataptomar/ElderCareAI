import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load and inspect CSV
df = pd.read_csv("Dataset/safety_monitoring.csv")
print("Initial shape:", df.shape)
df.columns = df.columns.str.strip()

# Replace "_" with NaN in impact column
df['Impact Force Level'] = df['Impact Force Level'].replace("_", pd.NA)

# Drop any rows with missing key values
df = df.dropna(subset=[
    'Movement Activity',
    'Impact Force Level',
    'Post-Fall Inactivity Duration (Seconds)',
    'Fall Detected (Yes/No)'
])

# Encode Movement Activity
movement_encoder = LabelEncoder()
df['Movement Encoded'] = movement_encoder.fit_transform(df['Movement Activity'])

# Encode Impact Force Level
impact_encoder = LabelEncoder()
df['Impact Encoded'] = impact_encoder.fit_transform(df['Impact Force Level'])

# Convert inactivity to numeric
df['Post-Fall Inactivity Duration (Seconds)'] = pd.to_numeric(df['Post-Fall Inactivity Duration (Seconds)'], errors='coerce')
df = df.dropna(subset=['Post-Fall Inactivity Duration (Seconds)'])

# Encode target
df['Fall Detected Encoded'] = df['Fall Detected (Yes/No)'].map({'Yes': 1, 'No': 0})

# Final feature + target
X = df[['Movement Encoded', 'Impact Encoded', 'Post-Fall Inactivity Duration (Seconds)']]
y = df['Fall Detected Encoded']

print("Fall class distribution:\n", y.value_counts())

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Report:\n", classification_report(y_test, y_pred))

# Save model + encoders
joblib.dump(model, "models/fall_model.pkl")
joblib.dump(movement_encoder, "models/fall_movement_encoder.pkl")
joblib.dump(impact_encoder, "models/fall_impact_encoder.pkl")
print("✅ Fall detection model + encoders saved.")
