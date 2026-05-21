# 🐳 CHAPTER 6: Docker Containerization

Now that you have Docker running, we can containerize the entire machine learning pipeline. This wraps the Django service, SQLite database, Gunicorn WSGI server, and Nginx proxy into two clean, isolated containers.

---

## 🛠️ How We Optimized the Docker Setup

In the original tutorial, the Dockerfile installed a very old Ubuntu/Python 3.6 image and heavy build tools. In our updated setup, we modernized and streamlined this:

1. **Python 3.12 Base Image:**
   - Since your Django 6.0.5 environment strictly requires **Python >= 3.12**, we configured the base container to use `python:3.12-slim`.
   
2. **No Heavy Compiler Libraries:**
   - We **completely removed the heavy `build-essential` compiler suite** from the OS installation. Because modern Python packages like `scikit-learn` and `numpy` download pre-compiled wheels, the container does not need to build them from source. This reduces download size by hundreds of megabytes and speeds up the build process from 15 minutes to under a minute!

3. **Port Mapping (8000:8000):**
   - We updated `docker-compose.yml` to map host port `8000` to Nginx container port `8000`. You can now access your API directly at `http://127.0.0.1:8000/api/v1/`.

---

## 🚀 Step-by-Step Deployment Instructions

### Step 1: Build the Docker Images
Open your host PowerShell terminal and run:
```powershell
docker-compose build
```
*Because we removed all heavy compilation packages, pip will instantly download the pre-compiled binary packages and cache them.*

### Step 2: Start the Containers
Once the build is complete, launch both Nginx and your Gunicorn wsgiserver:
```powershell
docker-compose up
```
*This will:*
- Wait for the server volume.
- Automatically execute `python manage.py migrate` inside the container to apply SQLite tables.
- Automatically run `python manage.py collectstatic` to bundle Nginx's static files.
- Boot up Gunicorn to serve predictions.

---

## 🧪 Testing the Dockerized API

While the container is running in your first terminal, open a **second host PowerShell** terminal and test the production API using the following command:

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

# Note that we are calling port 8000 served by Nginx proxy
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/v1/industry_classifier/predict",
    data=data, headers={"Content-Type": "application/json"}, method="POST"
)
res = urllib.request.urlopen(req)
print(res.read().decode())
```

**Expected JSON Response:**
```json
{"probability": 0.85, "label": "Automotive", "status": "OK", "request_id": 1}
```

---
*(You can shut down the active containers at any time by pressing `Ctrl + C` in the docker-compose terminal).*
