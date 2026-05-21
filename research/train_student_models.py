"""
Train ML models using StudentPerformanceFactors.csv
Produces 4 joblib files: train_mode, encoders, random_forest, extra_trees
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
import joblib
import os

# Load dataset
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
csv_path = os.path.join(project_root, "StudentPerformanceFactors.csv")

df = pd.read_csv(csv_path)
print(f"Loaded {len(df)} rows from StudentPerformanceFactors.csv")

# Create binary target: High (>=70) / Low (<70)
df['performance'] = df['Exam_Score'].apply(lambda x: 'High' if x >= 70 else 'Low')

x_cols = [c for c in df.columns if c not in ['Exam_Score', 'performance']]
X = df[x_cols]
y = df['performance']
print(f"Features: {X.shape[1]}, Samples: {X.shape[0]}")
print(f"Target distribution:\n{y.value_counts().to_string()}")

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1234
)
print(f"\nTrain: {X_train.shape}, Test: {X_test.shape}")

# Fill Missing Values
train_mode = dict(X_train.mode().iloc[0])
X_train = X_train.fillna(train_mode)

# Encode Categorical Columns
encoders = {}
categorical_columns = [
    'Parental_Involvement', 'Access_to_Resources',
    'Extracurricular_Activities', 'Motivation_Level',
    'Internet_Access', 'Family_Income', 'Teacher_Quality',
    'School_Type', 'Peer_Influence', 'Learning_Disabilities',
    'Parental_Education_Level', 'Distance_from_Home', 'Gender'
]
for column in categorical_columns:
    le = LabelEncoder()
    X_train[column] = le.fit_transform(X_train[column])
    encoders[column] = le
print(f"Encoders created for: {list(encoders.keys())}")

# Prepare test set
X_test_clean = X_test.fillna(train_mode)
for col in categorical_columns:
    X_test_clean[col] = encoders[col].transform(X_test_clean[col])

# Train Random Forest
print("\nTraining Random Forest...")
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_acc = rf.score(X_test_clean, y_test)
print(f"Random Forest trained! Test accuracy: {rf_acc:.4f}")

# Train Extra Trees
print("\nTraining Extra Trees...")
et = ExtraTreesClassifier(n_estimators=100, random_state=42)
et.fit(X_train, y_train)
et_acc = et.score(X_test_clean, y_test)
print(f"Extra Trees trained! Test accuracy: {et_acc:.4f}")

# Save All Models
joblib.dump(train_mode, os.path.join(script_dir, "train_mode.joblib"), compress=True)
joblib.dump(encoders,   os.path.join(script_dir, "encoders.joblib"),   compress=True)
joblib.dump(rf,         os.path.join(script_dir, "random_forest.joblib"), compress=True)
joblib.dump(et,         os.path.join(script_dir, "extra_trees.joblib"),   compress=True)

print(f"\nAll 4 .joblib files saved to research/")
print(f"   Random Forest accuracy: {rf_acc:.4f}")
print(f"   Extra Trees accuracy:   {et_acc:.4f}")
