# ⚙️ Setup & Run Guide

> Quick reference for running the ML Service. For the full build tutorial, see `Tutorial.md`.

---

# 🚀 OPTION A — Run Locally (Development)

## Quick Start

```powershell
# 1. Open PowerShell, go to project root
cd C:\Users\provu\Desktop\my_ml_service

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Go to Django project
cd backend\server

# 4. Start the server
python manage.py runserver 8001

# 5. Open browser → http://127.0.0.1:8001/api/v1/
```

> Use port `8001` if port 8000 is occupied by another project.
> Press `CTRL + C` to stop the server.

---

## First-Time Setup (only once)

```powershell
# Run migrations (creates database tables)
python manage.py migrate

# Create admin account (optional)
python manage.py createsuperuser
```

---

# 🐳 OPTION B — Run with Docker (Production)

## Prerequisites
- Docker Desktop installed and running
- Download: https://www.docker.com/products/docker-desktop/

## Quick Start

```powershell
# 1. Open PowerShell, go to project root
cd C:\Users\provu\Desktop\my_ml_service

# 2. Build (first time only — takes 5-15 minutes)
docker-compose build

# 3. Start containers (detached mode)
docker-compose up -d

# 4. Open browser → http://localhost:8080/api/v1/
```

> Docker runs on port **8080** (mapped to internal port 8000).

## Docker Commands

| Command | What It Does |
|---|---|
| `docker-compose up -d` | Start containers in background |
| `docker-compose up` | Start containers (shows logs in terminal) |
| `docker-compose down` | Stop and remove containers |
| `docker-compose logs -f` | Watch live logs |
| `docker-compose logs wsgiserver` | View backend logs only |
| `docker-compose build` | Rebuild after code changes |
| `docker ps` | Show running containers |

## After Code Changes

```powershell
# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

## What's Running Inside Docker

| Container | Role | Port |
|---|---|---|
| `my_ml_service-nginx-1` | Reverse proxy + static files | `8080 → 8000` |
| `my_ml_service-wsgiserver-1` | Django + Gunicorn (4 workers) | `8000` (internal) |

---

# 🌐 Browser Pages

| URL (Local) | URL (Docker) | What You See |
|---|---|---|
| `http://127.0.0.1:8001/api/v1/` | `http://localhost:8080/api/v1/` | API root — all routes |
| `.../api/v1/endpoints` | `.../api/v1/endpoints` | Registered endpoints |
| `.../api/v1/mlalgorithms` | `.../api/v1/mlalgorithms` | Algorithms + current status |
| `.../api/v1/mlalgorithmstatuses` | `.../api/v1/mlalgorithmstatuses` | Status history |
| `.../api/v1/mlrequests` | `.../api/v1/mlrequests` | All prediction logs |
| `.../api/v1/abtests` | `.../api/v1/abtests` | A/B tests list |
| `.../admin/` | `.../admin/` | Django Admin (needs superuser) |

---

# 🧪 Test a Prediction

## Option A — Quick Python Script

Open a **second** terminal (keep server running):

```python
import urllib.request, json

# Change port: 8001 for local, 8080 for Docker
PORT = 8001

data = json.dumps({
    "age": 37, "workclass": "Private", "fnlwgt": 34146,
    "education": "HS-grad", "education-num": 9,
    "marital-status": "Married-civ-spouse", "occupation": "Craft-repair",
    "relationship": "Husband", "race": "White", "sex": "Male",
    "capital-gain": 0, "capital-loss": 0, "hours-per-week": 68,
    "native-country": "United-States"
}).encode()

req = urllib.request.Request(
    f"http://127.0.0.1:{PORT}/api/v1/income_classifier/predict",
    data=data, headers={"Content-Type": "application/json"}, method="POST"
)
res = urllib.request.urlopen(req)
print(res.read().decode())
```

Expected:
```json
{"probability": 0.04, "label": "<=50K", "status": "OK", "request_id": 1}
```

## Option B — Run Full Test Suite

```powershell
# From project root with venv activated:
python test_all.py
```

This runs all 11 end-to-end tests automatically.

## Option C — Django Unit Tests

```powershell
# From backend/server/ with venv activated:
python manage.py test apps
```

Expected: `Ran 3 tests ... OK`

---

# 🔄 How to Change the Dataset

## Files to Update

| # | File | What to Change |
|---|---|---|
| 1 | `research/train_models.ipynb` | Load new data, new columns, retrain |
| 2 | `apps/ml/income_classifier/random_forest.py` | Categorical columns + labels |
| 3 | `apps/ml/income_classifier/extra_trees.py` | Same as random_forest.py |
| 4 | `server/wsgi.py` | Endpoint name (optional) |

## Steps

### 1. Retrain in Jupyter

```powershell
cd C:\Users\provu\Desktop\my_ml_service\research
.venv\Scripts\activate
jupyter notebook
```

Create a new notebook. Load your dataset, train, and save:
```python
import joblib
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier

# ... load your data, preprocess, split ...

rf = RandomForestClassifier(n_estimators=100).fit(X_train, y_train)
et = ExtraTreesClassifier(n_estimators=100).fit(X_train, y_train)

joblib.dump(train_mode, "./train_mode.joblib", compress=True)
joblib.dump(encoders,   "./encoders.joblib",   compress=True)
joblib.dump(rf,         "./random_forest.joblib", compress=True)
joblib.dump(et,         "./extra_trees.joblib",   compress=True)
```

### 2. Update Classifier Files

In `random_forest.py` and `extra_trees.py`:
```python
# Change categorical columns to YOUR text columns:
for column in ["your_col_1", "your_col_2"]:
    input_data[column] = self.encoders[column].transform(input_data[column])

# Change labels in postprocessing():
def postprocessing(self, input_data):
    label = "class_A"
    if input_data[1] > 0.5:
        label = "class_B"
    return {"probability": float(input_data[1]), "label": label, "status": "OK"}
```

### 3. Reset Database & Restart

```powershell
# From backend/server/:
del db.sqlite3
python manage.py migrate
python manage.py runserver 8001
```

### 4. For Docker — Rebuild

```powershell
# From project root:
docker-compose down
docker-compose build
docker-compose up -d
# Open → http://localhost:8080/api/v1/
```

---

# ❓ Common Issues

| Problem | Fix |
|---|---|
| **Port already in use** | Use a different port: `python manage.py runserver 8002` |
| **"no such table" error** | Run `python manage.py migrate` |
| **FileNotFoundError for .joblib** | Run Jupyter notebook to generate the model files in `research/` |
| **"ML algorithm is not available"** | Check `/api/v1/mlalgorithmstatuses` — ensure an algorithm has `"status": "production"` and `"active": true` |
| **Docker port conflict** | Change port in `docker-compose.yml`: `"8080:8000"` → `"9000:8000"` |
| **Docker "permission denied" on .sh** | Convert `wsgi-entrypoint.sh` to Unix line endings (LF not CRLF) |

---

# 📋 All API Endpoints

| Method | URL | Description |
|---|---|---|
| GET | `/api/v1/` | API root — all routes |
| GET | `/api/v1/endpoints` | List endpoints |
| GET | `/api/v1/mlalgorithms` | List algorithms + status |
| GET | `/api/v1/mlalgorithmstatuses` | Status history |
| GET | `/api/v1/mlrequests` | Prediction logs |
| GET | `/api/v1/abtests` | A/B tests |
| POST | `/api/v1/{endpoint}/predict` | Predict (production model) |
| POST | `/api/v1/{endpoint}/predict?status=testing` | Predict (testing model) |
| POST | `/api/v1/{endpoint}/predict?status=ab_testing` | Predict (A/B split) |
| POST | `/api/v1/abtests` | Create A/B test |
| POST | `/api/v1/stop_ab_test/{id}` | Stop test, pick winner |
| PUT | `/api/v1/mlrequests/{id}` | Add feedback |
| GET | `/admin/` | Django admin panel |
