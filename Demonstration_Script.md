# Industry Exposure Prediction - Full Demonstration

> **Dataset:** industry_exposure.csv (14 numeric columns)
> **Goal:** Predict the **Industry** classification based on vulnerability and exposure metrics
> **Model Used:** Random Forest & Extra Trees
> **Architecture:** Django REST API + scikit-learn + Docker (Python 3.12-slim)

---

## Table of Contents

| Chapter | What It Covers |
|---|---|
| **Chapter 1** | Train the models & Update Python Classifiers (Phase 1 & 2) |
| **Chapter 2** | Start Server & Verify Database (Phase 3) |
| **Chapter 3** | Get Predictions - API Output (Phase 4) |
| **Chapter 4** | A/B Testing Workflow (Phase 5) |
| **Chapter 5** | Docker Deployment (Phase 6) |

---

## Dataset Quick Look

| Column | Type | Example |
|---|---|---|
| year | Number | 2024 |
| pandemic_exposure | Number | 7.8 |
| geopolitical_exposure | Number | 6.7 |
| natural_disaster_exposure | Number | 6.8 |
| tariff_exposure | Number | 7.7 |
| logistics_exposure | Number | 9.4 |
| energy_exposure | Number | 8.0 |
| labor_exposure | Number | 9.7 |
| cyber_exposure | Number | 6.1 |
| overall_vulnerability | Number | 7.87 |
| inventory_days | Number | 21 |
| supplier_concentration_hhi | Number | 0.193 |
| just_in_time_dependency | Number | 0.733 |
| nearshoring_score_2024 | Number | 0.623 |
| **industry** | **Target** | Automotive, Semiconductors, etc. |

---

## What Files Were Changed (From Original Tutorial)

| File | What Changed |
|---|---|
| research/train_industry_models.py | New training script |
| research/train_mode.joblib | Fill-NA values (Retrained) |
| research/random_forest.joblib | Retrained RF model for 10 industries |
| research/extra_trees.joblib | Retrained ET model for 10 industries |
| apps/ml/industry_classifier/random_forest.py | Switched to multi-class target `numpy.argmax` |
| apps/ml/industry_classifier/extra_trees.py | Switched to multi-class target `numpy.argmax` |
| apps/ml/tests.py | Industry sample data updated |
| server/wsgi.py | Switched endpoint to `industry_classifier` |
| docker/backend/Dockerfile | Updated to `python:3.12-slim`, removed `build-essential` |
| docker-compose.yml | Mapped to `8000:8000` |

---
---

# CHAPTER 1 - Train Models and Update Files

This chapter has 2 phases:
- Phase 1: Retrain the ML models using industry_exposure.csv
- Phase 2: Update the classifier Python files

---

## Phase 1 - Retrain the Models

### Step 1: Create the Training Script

Open PowerShell and create a new script file inside the `research` folder:

Location: `research/train_industry_models.py`

Copy-paste this exact python code into the file:

```python
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
import joblib

# Load the dataset
df = pd.read_csv('../industry_exposure.csv', skipinitialspace=True)

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
```

### Step 2: Run the Training Script

Run the script you just created to train your Random Forest and Extra Trees models and save the `.joblib` files.

Open PowerShell and run:

```powershell
cd C:\Users\provu\Desktop\ml_vivian_punay
venv\Scripts\activate
cd research
python train_industry_models.py
```

Expected output:

```
Shape: (250, 14)
Train: (175, 14), Test: (75, 14)
Fill values: {...}
Random Forest trained!
Extra Trees trained!
All files saved!
```

---

### Jupyter Way (Step by Step)

If you prefer Jupyter Notebook, follow these exact steps:

**Step 1:** Open PowerShell and run:

```powershell
cd C:\Users\provu\Desktop\ml_vivian_punay
venv\Scripts\activate
python -m pip install notebook
cd research
python -m notebook
```

**Step 2:** Your browser opens. Click **New** then **Notebook**. Select the **venv** kernel.

**Step 3:** Create 5 cells. Copy-paste each one below and run them sequentially:

**Cell 1 - Imports:**
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
import joblib
```

**Cell 2 - Load dataset & Split:**
```python
df = pd.read_csv('../industry_exposure.csv', skipinitialspace=True)
x_cols = [c for c in df.columns if c != 'industry']
X = df[x_cols]
y = df['industry']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)
print(f"Train: {X_train.shape}, Test: {X_test.shape}")
```

**Cell 3 - Fill missing values:**
```python
train_mode = dict(X_train.mode().iloc[0])
X_train = X_train.fillna(train_mode)
print("Fill values:", train_mode)
```

**Cell 4 - Train Models:**
```python
rf = RandomForestClassifier(n_estimators=100)
rf = rf.fit(X_train, y_train)

et = ExtraTreesClassifier(n_estimators=100)
et = et.fit(X_train, y_train)
print("Models trained!")
```

**Cell 5 - Save models:**
```python
joblib.dump(train_mode, "./train_mode.joblib", compress=True)
joblib.dump(rf, "./random_forest.joblib", compress=True)
joblib.dump(et, "./extra_trees.joblib", compress=True)
print("All 3 files saved to research/ directory!")
```

---

## Phase 2 - Update the Classifier Files

The original tutorial handled categorical strings (like "Yes" or "High") using `LabelEncoder`. Because our dataset only has numeric exposure metrics, we **deleted the encoding loop** entirely. 
Additionally, we changed binary classification to multi-class using `np.argmax`.

Here is exactly what to paste into your two classifier files to update them for the new dataset.

### File 1: random_forest.py

Location: `backend/server/apps/ml/industry_classifier/random_forest.py`

Full file content (copy-paste to replace entire file):

```python
from pathlib import Path
import joblib
import pandas as pd
import numpy as np

class RandomForestClassifier:
    def __init__(self):
        project_root = Path(__file__).resolve().parents[5]
        research_dir = project_root / "research"

        self.values_fill_missing = joblib.load(research_dir / "train_mode.joblib")
        self.model = joblib.load(research_dir / "random_forest.joblib")

    def preprocessing(self, input_data):
        input_data = pd.DataFrame(input_data, index=[0])

        # fill missing values
        input_data = input_data.fillna(self.values_fill_missing)

        return input_data

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def postprocessing(self, input_data):
        # find the index with the highest probability
        max_index = np.argmax(input_data)
        label = self.model.classes_[max_index]
        return {"probability": float(input_data[max_index]), "label": label, "status": "OK"}

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

Location: `backend/server/apps/ml/industry_classifier/extra_trees.py`

Full file content (copy-paste to replace entire file):

```python
from pathlib import Path
import joblib
import pandas as pd
import numpy as np

class ExtraTreesClassifier:
    def __init__(self):
        project_root = Path(__file__).resolve().parents[5]
        research_dir = project_root / "research"

        self.values_fill_missing = joblib.load(research_dir / "train_mode.joblib")
        self.model = joblib.load(research_dir / "extra_trees.joblib")

    def preprocessing(self, input_data):
        input_data = pd.DataFrame(input_data, index=[0])

        # fill missing values
        input_data = input_data.fillna(self.values_fill_missing)

        return input_data

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def postprocessing(self, input_data):
        # find the index with the highest probability
        max_index = np.argmax(input_data)
        label = self.model.classes_[max_index]
        return {"probability": float(input_data[max_index]), "label": label, "status": "OK"}

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
cd C:\Users\provu\Desktop\ml_vivian_punay
venv\Scripts\activate
```

You should see `(venv)` at the start of your prompt.

---

## Step 3: Go to the Django server folder
```powershell
cd backend\server
```

---

## Step 4: Delete the old database
```powershell
del db.sqlite3
```
**Why?** The old database has the previous tutorials algorithms registered. We need a fresh one for the industry_classifier.

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
  ...
```

---

## Step 6: Start the server
```powershell
python manage.py runserver 8001
```

You should see:
```
Django version 6.0.5, using settings 'server.settings'
Starting development server at http://127.0.0.1:8001/
```

**What happens automatically:** When the server starts, `wsgi.py`:
1. Creates an endpoint called `industry_classifier`
2. Loads Random Forest model and sets it as **production**
3. Loads Extra Trees model and sets it as **testing**

> **IMPORTANT: Do NOT close this terminal! Keep the server running.**
> You will open a **second terminal** for Chapter 3.

---

## Step 7: Verify in your browser
Open your browser and check these URLs:

**URL 1:** http://127.0.0.1:8001/api/v1/endpoints
You should see: `[{..., "name": "industry_classifier", ...}]`

**URL 2:** http://127.0.0.1:8001/api/v1/mlalgorithms
You should see 2 algorithms:
- "random forest" with status "production"
- "extra trees" with status "testing"

---

> **END OF CHAPTER 2.** The server is running. Next: Chapter 3 (Get Predictions)

---
---

# CHAPTER 3 - Get Predictions (Output)

> **The server from Chapter 2 must still be running.** Do NOT close that terminal.

You need to open a **SECOND PowerShell terminal** for this chapter.

---

## How to Run a Prediction

**Step 1:** Open a NEW PowerShell terminal.
**Step 2:** Run Python directly in the terminal to hit the API!

```powershell
python
```

Paste this exact code into Python and press Enter:

```python
import urllib.request
import json

data = json.dumps({
    "year": 2024,
    "pandemic_exposure": 7.8,
    "geopolitical_exposure": 6.7,
    "natural_disaster_exposure": 6.8,
    "tariff_exposure": 7.7,
    "logistics_exposure": 9.4,
    "energy_exposure": 8.0,
    "labor_exposure": 9.7,
    "cyber_exposure": 6.1,
    "overall_vulnerability": 7.87,
    "inventory_days": 21,
    "supplier_concentration_hhi": 0.193,
    "just_in_time_dependency": 0.733,
    "nearshoring_score_2024": 0.623
}).encode('utf-8')

req = urllib.request.Request(
    "http://127.0.0.1:8001/api/v1/industry_classifier/predict",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)
res = urllib.request.urlopen(req)
print(res.read().decode('utf-8'))
```

**Expected Output from the API:**
```json
{"probability": 0.85, "label": "Automotive", "status": "OK", "request_id": 1}
```

*(The prediction tells you that these vulnerability scores point to the Automotive industry!)*

---

> **END OF CHAPTER 3.** Next: Chapter 4 (A/B Testing)

---
---

# CHAPTER 4 - A/B Testing Phase

Because we registered *both* the Random Forest (as `"production"`) and Extra Trees (as `"testing"`), you can run A/B tests between them.

### How to Run an A/B Test in the Terminal

Open a new PowerShell terminal and start Python.
*(**Note:** Only copy the python code itself, do NOT copy the ```python backticks into your terminal!)*

```powershell
python
```

**1. Start A/B Test:**
Send a POST to `/api/v1/abtests` mapping Algorithm 1 (Random Forest) against Algorithm 2 (Extra Trees).

```python
import urllib.request
import json

ab_test_data = json.dumps({
    "title": "Industry Classifier A/B Test",
    "created_by": "admin",
    "parent_mlalgorithm_1": 1,
    "parent_mlalgorithm_2": 2
}).encode('utf-8')

req1 = urllib.request.Request(
    "http://127.0.0.1:8001/api/v1/abtests",
    data=ab_test_data,
    headers={"Content-Type": "application/json"},
    method="POST"
)
res1 = urllib.request.urlopen(req1)
ab_test_response = json.loads(res1.read().decode('utf-8'))
print("A/B Test Started:", ab_test_response)
```

**2. Send Traffic (Route Randomly):**
Send prediction requests. Notice the `?status=ab_testing` in the URL! The API will automatically balance requests between the two models.

```python
import urllib.request
import json

predict_data = json.dumps({
    "year": 2024,
    "pandemic_exposure": 7.8,
    "geopolitical_exposure": 6.7,
    "natural_disaster_exposure": 6.8,
    "tariff_exposure": 7.7,
    "logistics_exposure": 9.4,
    "energy_exposure": 8.0,
    "labor_exposure": 9.7,
    "cyber_exposure": 6.1,
    "overall_vulnerability": 7.87,
    "inventory_days": 21,
    "supplier_concentration_hhi": 0.193,
    "just_in_time_dependency": 0.733,
    "nearshoring_score_2024": 0.623
}).encode('utf-8')

req2 = urllib.request.Request(
    "http://127.0.0.1:8001/api/v1/industry_classifier/predict?status=ab_testing",
    data=predict_data,
    headers={"Content-Type": "application/json"},
    method="POST"
)
res2 = urllib.request.urlopen(req2)
prediction_response = json.loads(res2.read().decode('utf-8'))
print("Prediction:", prediction_response)

# Save the request ID to send feedback next
request_id = prediction_response["request_id"]
```

**3. Send Feedback:**
Tell the system if the prediction was correct or not. Use a PUT request to update the record.

```python
import urllib.request
import json

feedback_data = json.dumps({
    "feedback": "Automotive"
}).encode('utf-8')

# If you skipped Step 2 in this terminal, manually set request_id (e.g. request_id = 1)
if 'request_id' not in locals():
    request_id = 1

req3 = urllib.request.Request(
    f"http://127.0.0.1:8001/api/v1/mlrequests/{request_id}",
    data=feedback_data,
    headers={"Content-Type": "application/json"},
    method="PUT"
)
res3 = urllib.request.urlopen(req3)
print("Feedback Sent:", res3.read().decode('utf-8'))
```

**4. Stop Test and Promote Winner:**
Hit the stop endpoint. The system calculates accuracy based on feedback and automatically changes the winner's status to `"production"`.

```python
import urllib.request
import json

# If you skipped Step 1 in this terminal, manually set ab_test_id (e.g. ab_test_id = 1)
if 'ab_test_response' in locals():
    ab_test_id = ab_test_response['id']
else:
    ab_test_id = 1

req4 = urllib.request.Request(
    f"http://127.0.0.1:8001/api/v1/stop_ab_test/{ab_test_id}",
    headers={"Content-Type": "application/json"},
    method="POST"
)
res4 = urllib.request.urlopen(req4)
print("A/B Test Stopped:", res4.read().decode('utf-8'))
```


---

> **END OF CHAPTER 4.** Next: Chapter 5 (Docker)

---
---

# CHAPTER 5 - Docker Containerization

Wrapping our modernized, lightweight Django server and Nginx proxy in a secure container environment.

### Optimized Docker Settings:
- **Base Image:** We updated the backend to use `python:3.12-slim` so that it satisfies Django 6.0.5's requirement (Python >= 3.12).
- **Fast Build:** We completely removed the heavy `build-essential` OS compilers from the `Dockerfile`. Pip will instantly install pre-compiled Python binary wheels instead, speeding up build time dramatically!
- **Port Mapping:** Port `8000:8000` is mapped from the Nginx proxy to the host machine.

### How to Run:

1. **Pull the Base Image (Prevents TLS timeouts):**
   ```powershell
   docker pull python:3.12-slim
   ```
2. **Build:**
   ```powershell
   docker-compose build
   ```
3. **Start:**
   ```powershell
   docker-compose up
   ```
4. **Test:**
Open a second PowerShell terminal, run `python`, and paste this:

```python
import urllib.request, json
data = json.dumps({
    "year": 2024,
    "pandemic_exposure": 7.8,
    "geopolitical_exposure": 6.7,
    "natural_disaster_exposure": 6.8,
    "tariff_exposure": 7.7,
    "logistics_exposure": 9.4,
    "energy_exposure": 8.0,
    "labor_exposure": 9.7,
    "cyber_exposure": 6.1,
    "overall_vulnerability": 7.87,
    "inventory_days": 21,
    "supplier_concentration_hhi": 0.193,
    "just_in_time_dependency": 0.733,
    "nearshoring_score_2024": 0.623
}).encode()

# Call port 8000 (served by Nginx)
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/v1/industry_classifier/predict",
    data=data, headers={"Content-Type": "application/json"}, method="POST"
)
res = urllib.request.urlopen(req)
print(res.read().decode())
```

---
**End of Demonstration Script**
