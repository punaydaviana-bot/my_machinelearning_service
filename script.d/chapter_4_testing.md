# 🧪 CHAPTER 4: Testing & Serving Predictions

It is crucial to verify that the API logic works without throwing a 500 Server Error before putting it live.

## Step 1: Run the Django Unit Tests

We rebuilt the automated tests in `apps/ml/tests.py` to send a mock JSON payload of vulnerability metrics (matching the columns from `industry_exposure.csv`).

**Instruction:**
```powershell
cd backend\server
python manage.py test apps.ml.tests
```
**Expected Output:** `Ran 2 tests in ...s OK`. This proves the API successfully calculates predictions.

## Step 2: Start the Django Server

With tests passing, start the Gunicorn/Django service.
```powershell
# From within backend/server
python manage.py runserver 8001
```

## Step 3: Test a Live API Request

Open a **SECOND PowerShell terminal** (do not close the server terminal). This represents a user making a request to your API from anywhere in the world.

Run the following Python script to fire a payload at the endpoint:

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

req = urllib.request.Request(
    "http://127.0.0.1:8001/api/v1/industry_classifier/predict",
    data=data, headers={"Content-Type": "application/json"}, method="POST"
)
res = urllib.request.urlopen(req)
print(res.read().decode())
```

**Expected JSON Response:**
```json
{"probability": 0.85, "label": "Automotive", "status": "OK", "request_id": 1}
```
*The model has successfully analyzed the vulnerability footprint and predicted the industry.*
