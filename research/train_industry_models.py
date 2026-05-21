import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
import joblib

# Load the dataset
df = pd.read_csv('industry_exposure.csv', skipinitialspace=True)

# Separate features (X) and target (y)
x_cols = [c for c in df.columns if c != 'industry']
X = df[x_cols]
y = df['industry']

print(f"Shape: {X.shape}")

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1234
)
print(f"Train: {X_train.shape}, Test: {X_test.shape}")

# Fill Missing Values
train_mode = dict(X_train.mode().iloc[0])
X_train = X_train.fillna(train_mode)
print("Fill values:", train_mode)

# Train Random Forest
rf = RandomForestClassifier(n_estimators=100)
rf = rf.fit(X_train, y_train)
print("Random Forest trained!")

# Train Extra Trees
et = ExtraTreesClassifier(n_estimators=100)
et = et.fit(X_train, y_train)
print("Extra Trees trained!")

# Save All Models
joblib.dump(train_mode, "./train_mode.joblib",   compress=True)
joblib.dump(rf,         "./random_forest.joblib", compress=True)
joblib.dump(et,         "./extra_trees.joblib",   compress=True)
print("All files saved!")
