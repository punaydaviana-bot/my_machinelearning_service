# Student Performance Prediction - Full Demonstration

> **Dataset:** StudentPerformanceFactors.csv (6,607 students, 20 columns)
> **Goal:** Predict if a student scores **High (>= 70)** or **Low (< 70)**
> **Model Accuracy:** Random Forest **91.93%** | Extra Trees **90.97%**
> **Architecture:** Django REST API + scikit-learn + Docker

---

## Table of Contents

| Chapter | What It Covers |
|---|---|
| **Chapter 1** | Train the models + Update classifier files (Phase 1, 2) |
| **Chapter 2** | Reset database + Start server (Phase 3) |
| **Chapter 3** | Get predictions - actual output (Phase 4) |
| **Chapter 4** | A/B Testing workflow (Phase 5) |
| **Chapter 5** | Docker deployment + Browser URLs (Phase 6, 7) |
| **Appendix** | Dataset columns, valid values, flow diagram |

---

## Dataset Quick Look

| Column | Type | Values |
|---|---|---|
| Hours_Studied | Number | 1 to 44 |
| Attendance | Number | 60 to 100 |
| Parental_Involvement | Text | Low, Medium, High |
| Access_to_Resources | Text | Low, Medium, High |
| Extracurricular_Activities | Text | Yes, No |
| Sleep_Hours | Number | 4 to 10 |
| Previous_Scores | Number | 50 to 100 |
| Motivation_Level | Text | Low, Medium, High |
| Internet_Access | Text | Yes, No |
| Tutoring_Sessions | Number | 0 to 8 |
| Family_Income | Text | Low, Medium, High |
| Teacher_Quality | Text | Low, Medium, High |
| School_Type | Text | Public, Private |
| Peer_Influence | Text | Positive, Neutral, Negative |
| Physical_Activity | Number | 0 to 6 |
| Learning_Disabilities | Text | Yes, No |
| Parental_Education_Level | Text | High School, College, Postgraduate |
| Distance_from_Home | Text | Near, Moderate, Far |
| Gender | Text | Male, Female |
| **Exam_Score** | **Target** | Converted to High/Low |

---

## What Files Were Changed (From Original Tutorial)

| File | What Changed |
|---|---|
| research/train_mode.joblib | Retrained with student data |
| research/encoders.joblib | 13 student categorical encoders |
| research/random_forest.joblib | Retrained RF model |
| research/extra_trees.joblib | Retrained ET model |
| apps/ml/income_classifier/random_forest.py | Student columns + High/Low labels |
| apps/ml/income_classifier/extra_trees.py | Student columns + High/Low labels |
| apps/ml/tests.py | Student sample data |
| apps/endpoints/tests.py | Student sample data |
| test_all.py | Student sample data + A/B test |
| research/train_student_models.py | New training script |

---
---

# CHAPTER 1 - Train Models and Update Files

This chapter has 2 phases:
- Phase 1: Retrain the ML models using StudentPerformanceFactors.csv
- Phase 2: Update the classifier Python files

---

## Phase 1 - Retrain the Models

> **SKIP NOTE:** This is **ALREADY DONE** for you. The 4 .joblib model files are already in the research/ folder. If you want to skip, go directly to **Chapter 2**.
>
> If you want to redo the training yourself, follow the steps below.

### Quick Way (No Jupyter Needed)

Open PowerShell and run:

```powershell
cd C:\Users\provu\Desktop\my_ml_service
.venv\Scripts\activate
python research\train_student_models.py
```

Expected output:

```
Loaded 6607 rows from StudentPerformanceFactors.csv
Features: 19, Samples: 6607
Training Random Forest...
Random Forest trained! Test accuracy: 0.9193
Training Extra Trees...
Extra Trees trained! Test accuracy: 0.9097
All 4 .joblib files saved to research/
```

Done! Skip to Phase 2 or Chapter 2.

---

### Jupyter Way (Step by Step)

If you prefer Jupyter Notebook, follow these steps:

**Step 1:** Open PowerShell and run:

```powershell
cd C:\Users\provu\Desktop\my_ml_service
.venv\Scripts\activate
cd research
jupyter notebook
```

**Step 2:** Your browser opens. Click **New** then **Notebook**. Select the **.venv** kernel.

**Step 3:** Create 8 cells. Copy-paste each one below:

**Cell 1 - Imports:**

```python
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
import joblib
```

**Cell 2 - Load dataset:**

```python
df = pd.read_csv(r'C:\Users\provu\Desktop\my_ml_service\StudentPerformanceFactors.csv')
df['performance'] = df['Exam_Score'].apply(lambda x: 'High' if x >= 70 else 'Low')
x_cols = [c for c in df.columns if c not in ['Exam_Score', 'performance']]
X = df[x_cols]
y = df['performance']
print(f"Shape: {X.shape}")
print(f"Target distribution:\n{y.value_counts()}")
```

**Cell 3 - Split data:**

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)
print(f"Train: {X_train.shape}, Test: {X_test.shape}")
```

**Cell 4 - Fill missing values:**

```python
train_mode = dict(X_train.mode().iloc[0])
X_train = X_train.fillna(train_mode)
print("Fill values:", train_mode)
```

**Cell 5 - Encode categorical columns:**

```python
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
print("Encoders created for:", list(encoders.keys()))
```

**Cell 6 - Train Random Forest:**

```python
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf = rf.fit(X_train, y_train)
X_test_clean = X_test.fillna(train_mode)
for col in categorical_columns:
    X_test_clean[col] = encoders[col].transform(X_test_clean[col])
print(f"Random Forest accuracy: {rf.score(X_test_clean, y_test):.4f}")
```

**Cell 7 - Train Extra Trees:**

```python
et = ExtraTreesClassifier(n_estimators=100, random_state=42)
et = et.fit(X_train, y_train)
print(f"Extra Trees accuracy: {et.score(X_test_clean, y_test):.4f}")
```

**Cell 8 - Save all models:**

```python
joblib.dump(train_mode, "./train_mode.joblib", compress=True)
joblib.dump(encoders, "./encoders.joblib", compress=True)
joblib.dump(rf, "./random_forest.joblib", compress=True)
joblib.dump(et, "./extra_trees.joblib", compress=True)
print("All 4 files saved!")
```

After Cell 8, you should have these 4 files in research/:

| File | What It Contains |
|---|---|
| train_mode.joblib | Fill-missing values (mode of each column) |
| encoders.joblib | Label encoders for 13 categorical columns |
| random_forest.joblib | Trained Random Forest model |
| extra_trees.joblib | Trained Extra Trees model |

---

## Phase 2 - Update Classifier Files

> **SKIP NOTE:** This is **ALREADY DONE** for you. Both random_forest.py and extra_trees.py are already updated. Also tests.py and test_all.py are updated. If you want to skip, go directly to **Chapter 2**.
>
> The code below is for reference only.

### File 1: random_forest.py

Location: `backend/server/apps/ml/income_classifier/random_forest.py`

Full file content (copy-paste to replace entire file):

```python
from pathlib import Path

import joblib
import pandas as pd


class RandomForestClassifier:
    def __init__(self):
        project_root = Path(__file__).resolve().parents[5]
        research_dir = project_root / "research"

        self.values_fill_missing = joblib.load(research_dir / "train_mode.joblib")
        self.encoders = joblib.load(research_dir / "encoders.joblib")
        self.model = joblib.load(research_dir / "random_forest.joblib")

    def preprocessing(self, input_data):
        input_data = pd.DataFrame(input_data, index=[0])
        input_data = input_data.fillna(self.values_fill_missing)
        for column in [
            "Parental_Involvement", "Access_to_Resources",
            "Extracurricular_Activities", "Motivation_Level",
            "Internet_Access", "Family_Income", "Teacher_Quality",
            "School_Type", "Peer_Influence", "Learning_Disabilities",
            "Parental_Education_Level", "Distance_from_Home", "Gender",
        ]:
            input_data[column] = self.encoders[column].transform(input_data[column])
        return input_data

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def postprocessing(self, input_data):
        # index [0] = probability of 'High' (model classes_ = ['High', 'Low'])
        label = "Low"
        if input_data[0] > 0.5:
            label = "High"
        return {"probability": float(input_data[0]), "label": label, "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)[0]
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        return prediction
```

### File 2: extra_trees.py

Location: `backend/server/apps/ml/income_classifier/extra_trees.py`

Full file content (copy-paste to replace entire file):

```python
from pathlib import Path

import joblib
import pandas as pd


class ExtraTreesClassifier:
    def __init__(self):
        project_root = Path(__file__).resolve().parents[5]
        research_dir = project_root / "research"

        self.values_fill_missing = joblib.load(research_dir / "train_mode.joblib")
        self.encoders = joblib.load(research_dir / "encoders.joblib")
        self.model = joblib.load(research_dir / "extra_trees.joblib")

    def preprocessing(self, input_data):
        input_data = pd.DataFrame(input_data, index=[0])
        input_data = input_data.fillna(self.values_fill_missing)
        for column in [
            "Parental_Involvement", "Access_to_Resources",
            "Extracurricular_Activities", "Motivation_Level",
            "Internet_Access", "Family_Income", "Teacher_Quality",
            "School_Type", "Peer_Influence", "Learning_Disabilities",
            "Parental_Education_Level", "Distance_from_Home", "Gender",
        ]:
            input_data[column] = self.encoders[column].transform(input_data[column])
        return input_data

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def postprocessing(self, input_data):
        # index [0] = probability of 'High' (model classes_ = ['High', 'Low'])
        label = "Low"
        if input_data[0] > 0.5:
            label = "High"
        return {"probability": float(input_data[0]), "label": label, "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)[0]
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        return prediction
```

---

> **END OF CHAPTER 1.** Next: Chapter 2 (Reset Database and Start Server)

---
---

# CHAPTER 2 - Reset Database and Start Server

This is where you **START** if you skipped Chapter 1.

You need **one PowerShell terminal** for this chapter.

---

## Step 1: Open PowerShell

Press `Win + R`, type `powershell`, press Enter.

Or open **Windows Terminal** from Start Menu.

---

## Step 2: Go to the project and activate virtual environment

Copy-paste this into PowerShell:

```powershell
cd C:\Users\provu\Desktop\my_ml_service
.venv\Scripts\activate
```

You should see `(.venv)` at the start of your prompt:

```
(.venv) PS C:\Users\provu\Desktop\my_ml_service>
```

If you dont see `(.venv)`, type `.venv\Scripts\activate` again.

---

## Step 3: Go to the Django server folder

```powershell
cd backend\server
```

Your prompt should now show:

```
(.venv) PS C:\Users\provu\Desktop\my_ml_service\backend\server>
```

---

## Step 4: Delete the old database

```powershell
del db.sqlite3
```

**Why?** The old database has the previous algorithms registered. We need a fresh one.

**Note:** If you see "Cannot find path" - thats OK. It means there was no old database.

---

## Step 5: Create a fresh database

```powershell
python manage.py migrate
```

You should see:

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, endpoints, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying endpoints.0001_initial... OK
  Applying endpoints.0003_abtest... OK
  Applying sessions.0001_initial... OK
```

---

## Step 6: Start the server

```powershell
python manage.py runserver 8001
```

You should see:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 6.0.5, using settings 'server.settings'
Starting development server at http://127.0.0.1:8001/
Quit the server with CTRL-BREAK.
```

**What happens automatically:** When the server starts, wsgi.py:
1. Creates an endpoint called `income_classifier`
2. Loads Random Forest model and sets it as **production**
3. Loads Extra Trees model and sets it as **testing**

> **IMPORTANT: Do NOT close this terminal! Keep the server running.**
>
> You will open a **second terminal** for Chapter 3.
>
> If port 8001 is busy, use: `python manage.py runserver 8002`

---

## Step 7: Verify in your browser

Open your browser and check these URLs (server must be running):

**URL 1:** http://127.0.0.1:8001/api/v1/endpoints

You should see:

```json
[{"id": 1, "name": "income_classifier", "owner": "Piotr", "created_at": "..."}]
```

**URL 2:** http://127.0.0.1:8001/api/v1/mlalgorithms

You should see 2 algorithms:
- "random forest" with status "production"
- "extra trees" with status "testing"

**URL 3:** http://127.0.0.1:8001/api/v1/mlalgorithmstatuses

You should see 2 active statuses.

If you see 0 algorithms, check the PowerShell terminal for errors.

---

> **END OF CHAPTER 2.** The server is running. Next: Chapter 3 (Get Predictions)

---
---

# CHAPTER 3 - Get Predictions (Output)

> **The server from Chapter 2 must still be running.** Do NOT close that terminal.

You need to open a **SECOND PowerShell terminal** for this chapter.

---

## How to Run

**Step 1:** Open a NEW PowerShell terminal (keep the server terminal open)

**Step 2:** Activate the virtual environment:

```powershell
cd C:\Users\provu\Desktop\my_ml_service
.venv\Scripts\activate
```

**Step 3:** You have 2 options to run the prediction code:

**Option A - Save as file and run (recommended):**
1. Copy the code below into a file (e.g. `test_predict.py`)
2. Run: `python test_predict.py`

**Option B - Use Python interactive mode:**
1. Type `python` to start Python
2. Paste the code
3. Type `exit()` when done

---

## Example 1: Predict a LOW-performing student

Copy this entire block:

```python
import urllib.request, json

PORT = 8001

data = json.dumps({
    "Hours_Studied": 8,
    "Attendance": 62,
    "Parental_Involvement": "Low",
    "Access_to_Resources": "Low",
    "Extracurricular_Activities": "No",
    "Sleep_Hours": 5,
    "Previous_Scores": 55,
    "Motivation_Level": "Low",
    "Internet_Access": "No",
    "Tutoring_Sessions": 0,
    "Family_Income": "Low",
    "Teacher_Quality": "Low",
    "School_Type": "Public",
    "Peer_Influence": "Negative",
    "Physical_Activity": 1,
    "Learning_Disabilities": "Yes",
    "Parental_Education_Level": "High School",
    "Distance_from_Home": "Far",
    "Gender": "Male"
}).encode()

req = urllib.request.Request(
    f"http://127.0.0.1:{PORT}/api/v1/income_classifier/predict",
    data=data, headers={"Content-Type": "application/json"}, method="POST"
)
res = urllib.request.urlopen(req)
print(res.read().decode())
```

**Actual Output:**

```json
{"probability": 0.15, "label": "Low", "status": "OK", "request_id": 1}
```

**What it means:** "Low" = the model predicts this student will score below 70. Probability of High is only 15%.

---

## Example 2: Predict a HIGH-performing student

Copy this entire block:

```python
import urllib.request, json

PORT = 8001

data = json.dumps({
    "Hours_Studied": 35,
    "Attendance": 98,
    "Parental_Involvement": "High",
    "Access_to_Resources": "High",
    "Extracurricular_Activities": "Yes",
    "Sleep_Hours": 7,
    "Previous_Scores": 95,
    "Motivation_Level": "High",
    "Internet_Access": "Yes",
    "Tutoring_Sessions": 3,
    "Family_Income": "High",
    "Teacher_Quality": "High",
    "School_Type": "Private",
    "Peer_Influence": "Positive",
    "Physical_Activity": 4,
    "Learning_Disabilities": "No",
    "Parental_Education_Level": "Postgraduate",
    "Distance_from_Home": "Near",
    "Gender": "Female"
}).encode()

req = urllib.request.Request(
    f"http://127.0.0.1:{PORT}/api/v1/income_classifier/predict",
    data=data, headers={"Content-Type": "application/json"}, method="POST"
)
res = urllib.request.urlopen(req)
print(res.read().decode())
```

**Actual Output:**

```json
{"probability": 0.93, "label": "High", "status": "OK", "request_id": 2}
```

**What it means:** "High" = the model predicts this student will score 70 or above. 93% confident.

---

## Example 3: Predict using Extra Trees (testing model)

Copy this entire block. Notice the `?status=testing` in the URL:

```python
import urllib.request, json

PORT = 8001

data = json.dumps({
    "Hours_Studied": 20,
    "Attendance": 85,
    "Parental_Involvement": "Medium",
    "Access_to_Resources": "Medium",
    "Extracurricular_Activities": "Yes",
    "Sleep_Hours": 7,
    "Previous_Scores": 75,
    "Motivation_Level": "Medium",
    "Internet_Access": "Yes",
    "Tutoring_Sessions": 2,
    "Family_Income": "Medium",
    "Teacher_Quality": "Medium",
    "School_Type": "Public",
    "Peer_Influence": "Positive",
    "Physical_Activity": 3,
    "Learning_Disabilities": "No",
    "Parental_Education_Level": "College",
    "Distance_from_Home": "Near",
    "Gender": "Male"
}).encode()

req = urllib.request.Request(
    f"http://127.0.0.1:{PORT}/api/v1/income_classifier/predict?status=testing",
    data=data, headers={"Content-Type": "application/json"}, method="POST"
)
res = urllib.request.urlopen(req)
print(res.read().decode())
```

**Actual Output:**

```json
{"probability": 0.36, "label": "Low", "status": "OK", "request_id": 3}
```

**What it means:** Extra Trees gives 36% chance of High (so predicts Low).

---

## Run All Tests at Once

Instead of running examples one by one, you can run the full test suite:

```powershell
cd C:\Users\provu\Desktop\my_ml_service
.venv\Scripts\activate
python test_all.py
```

This runs Tests 4-11: predictions, A/B test creation, feedback, and stopping.

---

> **END OF CHAPTER 3.** Next: Chapter 4 (A/B Testing)

---
---

# CHAPTER 4 - A/B Testing

> **The server must still be running** from Chapter 2.
>
> Use the same second terminal from Chapter 3.

A/B testing compares Random Forest vs Extra Trees to find which model is better.

---

## Step 1: Create the A/B test

Save this as `test_ab.py` and run `python test_ab.py`:

```python
import requests

BASE = "http://127.0.0.1:8001/api/v1"

# Step 1: Create A/B test (algorithm 1 = RF, algorithm 2 = ET)
print("Creating A/B test...")
response = requests.post(f"{BASE}/abtests", json={
    "title": "RF vs ET - Student Performance",
    "created_by": "demo_user",
    "parent_mlalgorithm_1": 1,
    "parent_mlalgorithm_2": 2
})
ab_test = response.json()
print("A/B Test created:", ab_test)
ab_test_id = ab_test["id"]

# Step 2: Send 100 predictions with correct answers as feedback
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv(r'C:\Users\provu\Desktop\my_ml_service\StudentPerformanceFactors.csv')
df['performance'] = df['Exam_Score'].apply(lambda x: 'High' if x >= 70 else 'Low')
X = df[[c for c in df.columns if c not in ['Exam_Score', 'performance']]]
y = df['performance']
_, X_test, _, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)

print("\nSending 100 predictions with feedback...")
for i in range(100):
    input_data = dict(X_test.iloc[i])
    input_data = {k: (None if str(v) == 'nan' else v) for k, v in input_data.items()}
    correct_label = y_test.iloc[i]

    r = requests.post(
        f"{BASE}/income_classifier/predict?status=ab_testing",
        json=input_data
    ).json()

    requests.put(
        f"{BASE}/mlrequests/{r['request_id']}",
        json={"feedback": correct_label}
    )

    if (i + 1) % 25 == 0:
        print(f"  Sent {i+1}/100 predictions...")

# Step 3: Stop the A/B test and see the winner
print("\nStopping A/B test...")
result = requests.post(f"{BASE}/stop_ab_test/{ab_test_id}").json()
print("Result:", result)
```

**Expected Output:**

```
Creating A/B test...
A/B Test created: {"id": 1, "title": "RF vs ET - Student Performance", ...}

Sending 100 predictions with feedback...
  Sent 25/100 predictions...
  Sent 50/100 predictions...
  Sent 75/100 predictions...
  Sent 100/100 predictions...

Stopping A/B test...
Result: {"message": "AB Test finished.", "summary": "Algorithm #1 accuracy: 0.86, ..."}
```

**What happens:** The winner is automatically promoted to "production" status.

---

> **END OF CHAPTER 4.** Next: Chapter 5 (Docker + Browser)

---
---

# CHAPTER 5 - Docker Deployment and Browser URLs

## Docker Deployment

If Docker is installed (as per Setup.md), you can deploy to Docker:

```powershell
cd C:\Users\provu\Desktop\my_ml_service
docker-compose down
docker-compose build
docker-compose up -d
```

Then test at: http://localhost:8080/api/v1/income_classifier/predict

---

## Browser URLs (Quick Reference)

| URL | What You See |
|---|---|
| http://127.0.0.1:8001/api/v1/ | API root with all routes |
| http://127.0.0.1:8001/api/v1/endpoints | The income_classifier endpoint |
| http://127.0.0.1:8001/api/v1/mlalgorithms | Both algorithms + current status |
| http://127.0.0.1:8001/api/v1/mlrequests | Every prediction logged (input + output) |
| http://127.0.0.1:8001/api/v1/mlalgorithmstatuses | Algorithm statuses (production/testing) |
| http://127.0.0.1:8001/api/v1/abtests | A/B test results |

---

> **END OF CHAPTER 5.**

---
---

# APPENDIX - JSON Template and Valid Values

## JSON Template (all 19 fields)

Copy this when making a POST request:

```json
{
    "Hours_Studied": 20,
    "Attendance": 85,
    "Parental_Involvement": "Medium",
    "Access_to_Resources": "Medium",
    "Extracurricular_Activities": "Yes",
    "Sleep_Hours": 7,
    "Previous_Scores": 75,
    "Motivation_Level": "Medium",
    "Internet_Access": "Yes",
    "Tutoring_Sessions": 2,
    "Family_Income": "Medium",
    "Teacher_Quality": "Medium",
    "School_Type": "Public",
    "Peer_Influence": "Positive",
    "Physical_Activity": 3,
    "Learning_Disabilities": "No",
    "Parental_Education_Level": "College",
    "Distance_from_Home": "Near",
    "Gender": "Male"
}
```

## Valid Values for Text Fields

| Field | Valid Values |
|---|---|
| Parental_Involvement | Low, Medium, High |
| Access_to_Resources | Low, Medium, High |
| Extracurricular_Activities | Yes, No |
| Motivation_Level | Low, Medium, High |
| Internet_Access | Yes, No |
| Family_Income | Low, Medium, High |
| Teacher_Quality | Low, Medium, High |
| School_Type | Public, Private |
| Peer_Influence | Positive, Neutral, Negative |
| Learning_Disabilities | Yes, No |
| Parental_Education_Level | High School, College, Postgraduate |
| Distance_from_Home | Near, Moderate, Far |
| Gender | Male, Female |

## Quick Start (If You Skipped Everything)

All files are already updated. Just run these commands:

```powershell
cd C:\Users\provu\Desktop\my_ml_service
.venv\Scripts\activate
cd backend\server
del db.sqlite3
python manage.py migrate
python manage.py runserver 8001
```

Then in a second terminal:

```powershell
cd C:\Users\provu\Desktop\my_ml_service
.venv\Scripts\activate
python test_all.py
```

---

**END OF DEMONSTRATION**
