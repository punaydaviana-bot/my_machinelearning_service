# ðŸš€ Machine Learning Service with Django
## Complete Step-by-Step Tutorial

> Based on: https://www.deploymachinelearning.com
> Dataset used: Adult Income Dataset (predict if income >50K or <=50K)
> You CAN use your own dataset â€” see Chapter 8 at the end.

---

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CHAPTER 1 â€” Project Setup
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

## What You Will Do
- Create the project folder
- Set up a Python virtual environment
- Install all required packages
- Initialize the Django project
- Run the server to confirm it works

---

## STEP 1 â€” Create the Project Folder

Open your terminal (PowerShell on Windows, Terminal on Mac/Linux).

```bash
mkdir my_ml_service
cd my_ml_service
```

> âœ… You are now inside your project root: `my_ml_service/`

---

## STEP 2 â€” Create a Virtual Environment

A virtual environment keeps your packages isolated from other Python projects.

```bash
python -m venv .venv
```

This creates a `.venv/` folder inside `my_ml_service/`.

---

## STEP 3 â€” Activate the Virtual Environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\activate
```

**Mac / Linux:**
```bash
source .venv/bin/activate
```

> âœ… You will see `(.venv)` appear at the start of your terminal prompt.
> You must activate this every time you open a new terminal.

---

## STEP 4 â€” Install All Required Packages

Run these commands one by one with the venv activated:

```bash
pip install django==6.0.5
pip install djangorestframework==3.17.1
pip install django-filter
pip install numpy pandas scikit-learn joblib requests
pip install jupyter notebook ipykernel
```

> â³ This may take 2â€“5 minutes. Wait for each to finish.

Verify Django is installed:
```bash
python -m django --version
# Should output: 6.0.5
```

---

## STEP 5 â€” Register Jupyter with Your Virtual Environment

This lets Jupyter use your venv's Python instead of system Python:

```bash
ipython kernel install --user --name=.venv
```

> âœ… You will see: `Installed kernelspec .venv in C:\Users\...\kernels\.venv`

---

## STEP 6 â€” Create the Django Project

```bash
mkdir backend
cd backend
django-admin startproject server
cd server
```

Your folder structure is now:
```
my_ml_service/
â”œâ”€â”€ .venv/
â””â”€â”€ backend/
    â””â”€â”€ server/
        â”œâ”€â”€ manage.py
        â””â”€â”€ server/
            â”œâ”€â”€ __init__.py
            â”œâ”€â”€ settings.py
            â”œâ”€â”€ urls.py
            â”œâ”€â”€ asgi.py
            â””â”€â”€ wsgi.py
```

---

## STEP 7 â€” Run the Django Development Server

```bash
python manage.py runserver
```

Open your browser and go to: **http://127.0.0.1:8000**

> âœ… You should see the Django "The install worked successfully!" welcome page.

Press `CTRL + C` in the terminal to stop the server.

---

## âœ… CHAPTER 1 COMPLETE

You now have:
- A virtual environment with all packages installed
- A running Django project at `backend/server/`

**Next: Chapter 2 â€” Train the ML Models in Jupyter Notebook**

---



# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CHAPTER 2 â€” Train the ML Models
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

## What You Will Do
- Create a `research/` folder for Jupyter notebooks
- Open Jupyter Notebook
- Load and preprocess the Adult Income dataset
- Train two ML algorithms: Random Forest and Extra Trees
- Save the trained models as `.joblib` files

---

## STEP 1 â€” Create the Research Folder

Open a NEW terminal. Navigate to your project root `my_ml_service/`.
Activate your venv first, then:

```bash
mkdir research
cd research
```

---

## STEP 2 â€” Start Jupyter Notebook

```bash
jupyter notebook
```

> Your browser opens showing the Jupyter file browser.
> If it does not open, copy the URL from the terminal (starts with http://127.0.0.1:8888).

---

## STEP 3 â€” Create a New Notebook

1. Click **New** then **Notebook**
2. When asked to select a kernel, choose **`.venv`**
3. Click the title at the top and rename it to `train_models`

---

## STEP 4 â€” Run Each Cell in Order

Copy each block into a separate Jupyter cell. Press **SHIFT + ENTER** to run each.

### Cell 1 â€” Imports
```python
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
import joblib
```

### Cell 2 â€” Load the dataset
```python
df = pd.read_csv(
    'https://raw.githubusercontent.com/pplonski/datasets-for-start/master/adult/data.csv',
    skipinitialspace=True
)
x_cols = [c for c in df.columns if c != 'income']
X = df[x_cols]
y = df['income']
print(f"Shape: {X.shape}")
df.head()
```

### Cell 3 â€” Train/Test Split
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1234
)
print(f"Train: {X_train.shape}, Test: {X_test.shape}")
```

### Cell 4 â€” Fill Missing Values
```python
train_mode = dict(X_train.mode().iloc[0])
X_train = X_train.fillna(train_mode)
print("Fill values:", train_mode)
```

### Cell 5 â€” Encode Categorical Columns
```python
encoders = {}
categorical_columns = [
    'workclass', 'education', 'marital-status',
    'occupation', 'relationship', 'race', 'sex', 'native-country'
]
for column in categorical_columns:
    le = LabelEncoder()
    X_train[column] = le.fit_transform(X_train[column])
    encoders[column] = le
print("Encoders created for:", list(encoders.keys()))
```

### Cell 6 â€” Train Random Forest
```python
rf = RandomForestClassifier(n_estimators=100)
rf = rf.fit(X_train, y_train)
print("Random Forest trained!")
```

### Cell 7 â€” Train Extra Trees
```python
et = ExtraTreesClassifier(n_estimators=100)
et = et.fit(X_train, y_train)
print("Extra Trees trained!")
```

### Cell 8 â€” Save All Models
```python
joblib.dump(train_mode, "./train_mode.joblib",   compress=True)
joblib.dump(encoders,   "./encoders.joblib",      compress=True)
joblib.dump(rf,         "./random_forest.joblib", compress=True)
joblib.dump(et,         "./extra_trees.joblib",   compress=True)
print("All 4 files saved!")
```

After running Cell 8, your `research/` folder should look like:
```
research/
â”œâ”€â”€ train_models.ipynb
â”œâ”€â”€ train_mode.joblib     (small, fill-missing values)
â”œâ”€â”€ encoders.joblib       (label encoders)
â”œâ”€â”€ random_forest.joblib  (about 9 MB)
â””â”€â”€ extra_trees.joblib    (about 23 MB)
```

---

## CHAPTER 2 COMPLETE

You now have two trained ML models saved and ready to serve.

**Next: Chapter 3 â€” Django Models and REST API**

---



# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CHAPTER 3 â€” Django Models and REST API
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

## What You Will Do
- Create the `apps/endpoints` and `apps/ml` Django apps
- Define 5 database models
- Create serializers, views, and URL routes
- Run database migrations
- Test the browsable REST API

---

## STEP 1 â€” Create the App Folders

In terminal, navigate to `backend/server/` with venv activated:

```bash
cd backend/server

# Create the apps directory structure
mkdir apps
mkdir apps\endpoints
mkdir apps\ml
mkdir apps\ml\income_classifier
```

Create these empty `__init__.py` files (they tell Python these are packages):
- `apps/__init__.py`
- `apps/endpoints/__init__.py`
- `apps/ml/__init__.py`
- `apps/ml/income_classifier/__init__.py`

**Windows PowerShell:**
```powershell
New-Item apps/__init__.py -ItemType File
New-Item apps/endpoints/__init__.py -ItemType File
New-Item apps/ml/__init__.py -ItemType File
New-Item apps/ml/income_classifier/__init__.py -ItemType File
```

---

## STEP 2 â€” Create `apps/endpoints/apps.py`

Create the file `backend/server/apps/endpoints/apps.py`:
```python
from django.apps import AppConfig

class EndpointsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.endpoints"
```

---

## STEP 3 â€” Create `apps/ml/apps.py`

Create the file `backend/server/apps/ml/apps.py`:
```python
from django.apps import AppConfig

class MlConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ml"
```

---

## STEP 4 â€” Create `apps/endpoints/models.py`

Create the file `backend/server/apps/endpoints/models.py`:
```python
from django.db import models

class Endpoint(models.Model):
    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class MLAlgorithm(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    code = models.TextField()
    version = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    def __str__(self): return self.name

class MLAlgorithmStatus(models.Model):
    status = models.CharField(max_length=32)
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    parent_mlalgorithm = models.ForeignKey(
        MLAlgorithm, on_delete=models.CASCADE, related_name="status")
    def __str__(self): return self.status

class MLRequest(models.Model):
    input_data = models.TextField()
    full_response = models.TextField()
    response = models.TextField()
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE)
    def __str__(self): return str(self.created_at)

class ABTest(models.Model):
    title = models.CharField(max_length=10000)
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    summary = models.CharField(max_length=10000, blank=True, null=True)
    parent_mlalgorithm_1 = models.ForeignKey(
        MLAlgorithm, on_delete=models.CASCADE, related_name="parent_mlalgorithm_1")
    parent_mlalgorithm_2 = models.ForeignKey(
        MLAlgorithm, on_delete=models.CASCADE, related_name="parent_mlalgorithm_2")
    def __str__(self): return self.title
```

---

## STEP 5 â€” Update `server/settings.py`

Open `backend/server/server/settings.py`. Make these changes:

**Find INSTALLED_APPS and replace it with:**
```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.endpoints.apps.EndpointsConfig",
    "apps.ml.apps.MlConfig",
]
```

**Find ALLOWED_HOSTS and replace:**
```python
ALLOWED_HOSTS = ["0.0.0.0", "localhost", "127.0.0.1"]
```

**At the very top of the file, add `import os`:**
```python
import os
from pathlib import Path
```

**At the very bottom of the file, add:**
```python
STATIC_ROOT = os.path.join(BASE_DIR, "static")
```

---

## STEP 6 â€” Create `apps/endpoints/serializers.py`

Create `backend/server/apps/endpoints/serializers.py`:
```python
from rest_framework import serializers
from .models import ABTest, Endpoint, MLAlgorithm, MLAlgorithmStatus, MLRequest

class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        read_only_fields = ("id", "name", "owner", "created_at")
        fields = read_only_fields

class MLAlgorithmSerializer(serializers.ModelSerializer):
    current_status = serializers.SerializerMethodField(read_only=True)
    def get_current_status(self, obj):
        return MLAlgorithmStatus.objects.filter(
            parent_mlalgorithm=obj).latest("created_at").status
    class Meta:
        model = MLAlgorithm
        read_only_fields = ("id","name","description","code","version",
                            "owner","created_at","parent_endpoint","current_status")
        fields = read_only_fields

class MLAlgorithmStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithmStatus
        read_only_fields = ("id", "active")
        fields = ("id","active","status","created_by","created_at","parent_mlalgorithm")

class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        read_only_fields = ("id","input_data","full_response","response",
                            "created_at","parent_mlalgorithm")
        fields = ("id","input_data","full_response","response","feedback",
                  "created_at","parent_mlalgorithm")

class ABTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABTest
        read_only_fields = ("id", "ended_at", "created_at", "summary")
        fields = ("id","title","created_by","created_at","ended_at",
                  "summary","parent_mlalgorithm_1","parent_mlalgorithm_2")
```

---

## STEP 7 â€” Run Migrations

In `backend/server/` with venv activated:
```bash
python manage.py makemigrations
python manage.py migrate
```

You should see all migrations applied with `OK`.

---

## CHAPTER 3 COMPLETE

Database tables are created. Serializers are ready.

**Next: Chapter 4 â€” Serve ML Models (ML Registry)**

---



# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CHAPTER 4 â€” Serve ML Models
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

## What You Will Do
- Write the RandomForestClassifier server-side class
- Write the ExtraTreesClassifier server-side class
- Write the MLRegistry (maps algorithm IDs to objects)
- Register both algorithms in wsgi.py
- Run tests to confirm the ML code works

---

## STEP 1 â€” Create `apps/ml/income_classifier/random_forest.py`

Create `backend/server/apps/ml/income_classifier/random_forest.py`:
```python
from pathlib import Path
import joblib
import pandas as pd

class RandomForestClassifier:
    def __init__(self):
        # Go up 5 levels from this file to reach my_ml_service/
        project_root = Path(__file__).resolve().parents[5]
        research_dir = project_root / "research"

        self.values_fill_missing = joblib.load(research_dir / "train_mode.joblib")
        self.encoders = joblib.load(research_dir / "encoders.joblib")
        self.model = joblib.load(research_dir / "random_forest.joblib")

    def preprocessing(self, input_data):
        input_data = pd.DataFrame(input_data, index=[0])
        input_data = input_data.fillna(self.values_fill_missing)
        for column in ["workclass","education","marital-status","occupation",
                        "relationship","race","sex","native-country"]:
            input_data[column] = self.encoders[column].transform(input_data[column])
        return input_data

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def postprocessing(self, input_data):
        label = "<=50K"
        if input_data[1] > 0.5:
            label = ">50K"
        return {"probability": float(input_data[1]), "label": label, "status": "OK"}

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

## STEP 2 â€” Create `apps/ml/income_classifier/extra_trees.py`

Create `backend/server/apps/ml/income_classifier/extra_trees.py`
(Same as random_forest.py but loads `extra_trees.joblib`):
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
        for column in ["workclass","education","marital-status","occupation",
                        "relationship","race","sex","native-country"]:
            input_data[column] = self.encoders[column].transform(input_data[column])
        return input_data

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def postprocessing(self, input_data):
        label = "<=50K"
        if input_data[1] > 0.5:
            label = ">50K"
        return {"probability": float(input_data[1]), "label": label, "status": "OK"}

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

## STEP 3 â€” Create `apps/ml/registry.py`

Create `backend/server/apps/ml/registry.py`:
```python
from apps.endpoints.models import Endpoint, MLAlgorithm, MLAlgorithmStatus

class MLRegistry:
    def __init__(self):
        self.endpoints = {}   # maps algorithm DB id -> algorithm object

    def add_algorithm(self, endpoint_name, algorithm_object, algorithm_name,
                      algorithm_status, algorithm_version, owner,
                      algorithm_description, algorithm_code):
        endpoint, _ = Endpoint.objects.get_or_create(name=endpoint_name, owner=owner)
        db_obj, created = MLAlgorithm.objects.get_or_create(
            name=algorithm_name,
            description=algorithm_description,
            code=algorithm_code,
            version=algorithm_version,
            owner=owner,
            parent_endpoint=endpoint,
        )
        if created:
            status = MLAlgorithmStatus(
                status=algorithm_status,
                created_by=owner,
                parent_mlalgorithm=db_obj,
                active=True,
            )
            status.save()
        self.endpoints[db_obj.id] = algorithm_object
```

---

## STEP 4 â€” Update `server/wsgi.py`

Replace the full contents of `backend/server/server/wsgi.py`:
```python
import inspect
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
application = get_wsgi_application()

from apps.ml.registry import MLRegistry
from apps.ml.income_classifier.random_forest import RandomForestClassifier
from apps.ml.income_classifier.extra_trees import ExtraTreesClassifier

try:
    registry = MLRegistry()

    # Register Random Forest as "production"
    rf = RandomForestClassifier()
    registry.add_algorithm(
        endpoint_name="income_classifier",
        algorithm_object=rf,
        algorithm_name="random forest",
        algorithm_status="production",
        algorithm_version="0.0.1",
        owner="YourName",
        algorithm_description="Random Forest with simple pre- and post-processing",
        algorithm_code=inspect.getsource(RandomForestClassifier),
    )

    # Register Extra Trees as "testing"
    et = ExtraTreesClassifier()
    registry.add_algorithm(
        endpoint_name="income_classifier",
        algorithm_object=et,
        algorithm_name="extra trees",
        algorithm_status="testing",
        algorithm_version="0.0.1",
        owner="YourName",
        algorithm_description="Extra Trees with simple pre- and post-processing",
        algorithm_code=inspect.getsource(ExtraTreesClassifier),
    )

except Exception as e:
    print("Exception while loading algorithms to registry:", str(e))
```

---

## STEP 5 â€” Create `apps/ml/tests.py` and Run Tests

Create `backend/server/apps/ml/tests.py`:
```python
import inspect
from django.test import TestCase
from apps.ml.income_classifier.random_forest import RandomForestClassifier
from apps.ml.registry import MLRegistry

class MLTests(TestCase):
    def test_rf_algorithm(self):
        input_data = {
            "age": 37, "workclass": "Private", "fnlwgt": 34146,
            "education": "HS-grad", "education-num": 9,
            "marital-status": "Married-civ-spouse", "occupation": "Craft-repair",
            "relationship": "Husband", "race": "White", "sex": "Male",
            "capital-gain": 0, "capital-loss": 0, "hours-per-week": 68,
            "native-country": "United-States"
        }
        my_alg = RandomForestClassifier()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual("OK", response["status"])
        self.assertIn("label", response)
        self.assertEqual("<=50K", response["label"])

    def test_registry(self):
        registry = MLRegistry()
        self.assertEqual(len(registry.endpoints), 0)
        algorithm_object = RandomForestClassifier()
        registry.add_algorithm(
            "income_classifier", algorithm_object, "random forest",
            "production", "0.0.1", "YourName",
            "Random Forest with simple pre- and post-processing",
            inspect.getsource(RandomForestClassifier),
        )
        self.assertEqual(len(registry.endpoints), 1)
```

Run the tests:
```bash
python manage.py test apps.ml.tests
```

Expected output:
```
Ran 2 tests in X.XXXs
OK
```

---

## CHAPTER 4 COMPLETE

Both ML classifiers and the registry are working and tested.

**Next: Chapter 5 â€” Compute Predictions (the Predict API endpoint)**

---



# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CHAPTER 5 â€” Compute Predictions
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

## What You Will Do
- Create the views (API logic handlers)
- Create the URL routes
- Update the main URL config
- Register models in the Django Admin
- Start the server and test predictions

---

## STEP 1 â€” Create `apps/endpoints/views.py`

Create `backend/server/apps/endpoints/views.py`:
```python
import datetime
import json
from django.db import transaction
from django.db.models import F
from numpy.random import rand
from rest_framework import mixins, status, views, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .models import ABTest, Endpoint, MLAlgorithm, MLAlgorithmStatus, MLRequest
from .serializers import (ABTestSerializer, EndpointSerializer,
    MLAlgorithmSerializer, MLAlgorithmStatusSerializer, MLRequestSerializer)
from server.wsgi import registry


def deactivate_other_statuses(instance):
    old_statuses = MLAlgorithmStatus.objects.filter(
        parent_mlalgorithm=instance.parent_mlalgorithm,
        created_at__lt=instance.created_at,
        active=True,
    )
    for s in old_statuses:
        s.active = False
    MLAlgorithmStatus.objects.bulk_update(old_statuses, ["active"])


class EndpointViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()


class MLAlgorithmViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = MLAlgorithmSerializer
    queryset = MLAlgorithm.objects.all()


class MLAlgorithmStatusViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                                mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = MLAlgorithmStatusSerializer
    queryset = MLAlgorithmStatus.objects.all()

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active=True)
                deactivate_other_statuses(instance)
        except Exception as e:
            raise APIException(str(e))


class MLRequestViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                       mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = MLRequestSerializer
    queryset = MLRequest.objects.all()


class ABTestViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                    mixins.CreateModelMixin, mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ABTestSerializer
    queryset = ABTest.objects.all()

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save()
                status_1 = MLAlgorithmStatus(status="ab_testing",
                    created_by=instance.created_by,
                    parent_mlalgorithm=instance.parent_mlalgorithm_1, active=True)
                status_1.save()
                deactivate_other_statuses(status_1)
                status_2 = MLAlgorithmStatus(status="ab_testing",
                    created_by=instance.created_by,
                    parent_mlalgorithm=instance.parent_mlalgorithm_2, active=True)
                status_2.save()
                deactivate_other_statuses(status_2)
        except Exception as e:
            raise APIException(str(e))


class StopABTestView(views.APIView):
    def post(self, request, ab_test_id, format=None):
        try:
            ab_test = ABTest.objects.get(pk=ab_test_id)
            if ab_test.ended_at is not None:
                return Response({"message": "AB Test already finished."})
            date_now = datetime.datetime.now()

            all_1 = MLRequest.objects.filter(
                parent_mlalgorithm=ab_test.parent_mlalgorithm_1,
                created_at__gt=ab_test.created_at, created_at__lt=date_now).count()
            correct_1 = MLRequest.objects.filter(
                parent_mlalgorithm=ab_test.parent_mlalgorithm_1,
                created_at__gt=ab_test.created_at, created_at__lt=date_now,
                response=F("feedback")).count()
            accuracy_1 = correct_1 / float(all_1) if all_1 else 0.0

            all_2 = MLRequest.objects.filter(
                parent_mlalgorithm=ab_test.parent_mlalgorithm_2,
                created_at__gt=ab_test.created_at, created_at__lt=date_now).count()
            correct_2 = MLRequest.objects.filter(
                parent_mlalgorithm=ab_test.parent_mlalgorithm_2,
                created_at__gt=ab_test.created_at, created_at__lt=date_now,
                response=F("feedback")).count()
            accuracy_2 = correct_2 / float(all_2) if all_2 else 0.0

            alg_1 = ab_test.parent_mlalgorithm_1
            alg_2 = ab_test.parent_mlalgorithm_2
            if accuracy_1 < accuracy_2:
                alg_1, alg_2 = alg_2, alg_1

            s1 = MLAlgorithmStatus(status="production", created_by=ab_test.created_by,
                parent_mlalgorithm=alg_1, active=True)
            s1.save()
            deactivate_other_statuses(s1)
            s2 = MLAlgorithmStatus(status="testing", created_by=ab_test.created_by,
                parent_mlalgorithm=alg_2, active=True)
            s2.save()
            deactivate_other_statuses(s2)

            summary = "Algorithm #1 accuracy: {}, Algorithm #2 accuracy: {}".format(
                accuracy_1, accuracy_2)
            ab_test.ended_at = date_now
            ab_test.summary = summary
            ab_test.save()

        except Exception as e:
            return Response({"status": "Error", "message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "AB Test finished.", "summary": summary})


class PredictView(views.APIView):
    def post(self, request, endpoint_name, format=None):
        algorithm_status = self.request.query_params.get("status", "production")
        algorithm_version = self.request.query_params.get("version")

        algs = MLAlgorithm.objects.filter(
            parent_endpoint__name=endpoint_name,
            status__status=algorithm_status,
            status__active=True,
        )
        if algorithm_version is not None:
            algs = algs.filter(version=algorithm_version)

        if len(algs) == 0:
            return Response({"status": "Error", "message": "ML algorithm is not available"},
                            status=status.HTTP_400_BAD_REQUEST)

        if len(algs) != 1 and algorithm_status != "ab_testing":
            return Response({"status": "Error",
                "message": "ML algorithm selection is ambiguous. Please specify version."},
                status=status.HTTP_400_BAD_REQUEST)

        alg_index = 0
        if algorithm_status == "ab_testing":
            alg_index = 0 if rand() < 0.5 else 1

        algorithm_object = registry.endpoints[algs[alg_index].id]
        prediction = algorithm_object.compute_prediction(request.data)
        label = prediction["label"] if "label" in prediction else "error"

        ml_request = MLRequest(
            input_data=json.dumps(request.data),
            full_response=json.dumps(prediction),
            response=label,
            feedback="",
            parent_mlalgorithm=algs[alg_index],
        )
        ml_request.save()

        prediction["request_id"] = ml_request.id
        return Response(prediction)
```

---

## STEP 2 â€” Create `apps/endpoints/urls.py`

Create `backend/server/apps/endpoints/urls.py`:
```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.endpoints.views import (ABTestViewSet, EndpointViewSet,
    MLAlgorithmStatusViewSet, MLAlgorithmViewSet, MLRequestViewSet,
    PredictView, StopABTestView)

router = DefaultRouter(trailing_slash=False)
router.register(r"endpoints", EndpointViewSet, basename="endpoints")
router.register(r"mlalgorithms", MLAlgorithmViewSet, basename="mlalgorithms")
router.register(r"mlalgorithmstatuses", MLAlgorithmStatusViewSet, basename="mlalgorithmstatuses")
router.register(r"mlrequests", MLRequestViewSet, basename="mlrequests")
router.register(r"abtests", ABTestViewSet, basename="abtests")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/<str:endpoint_name>/predict", PredictView.as_view(), name="predict"),
    path("api/v1/stop_ab_test/<int:ab_test_id>", StopABTestView.as_view(), name="stop_ab_test"),
]
```

---

## STEP 3 â€” Update `server/urls.py`

Open `backend/server/server/urls.py` and replace it with:
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.endpoints.urls")),
]
```

---

## STEP 4 â€” Register Models in Admin

Create `backend/server/apps/endpoints/admin.py`:
```python
from django.contrib import admin
from .models import ABTest, Endpoint, MLAlgorithm, MLAlgorithmStatus, MLRequest

admin.site.register(Endpoint)
admin.site.register(MLAlgorithm)
admin.site.register(MLAlgorithmStatus)
admin.site.register(MLRequest)
admin.site.register(ABTest)
```

---

## STEP 5 â€” Start the Server and Test

```bash
python manage.py runserver 8001
```

Open your browser:
- `http://127.0.0.1:8001/api/v1/` â€” API root (all endpoints listed)
- `http://127.0.0.1:8001/api/v1/endpoints` â€” see income_classifier endpoint
- `http://127.0.0.1:8001/api/v1/mlalgorithms` â€” see random forest + extra trees

### Test a Prediction

In a new terminal (keep server running), run Python:
```python
import urllib.request, json

data = json.dumps({
    "age": 37, "workclass": "Private", "fnlwgt": 34146,
    "education": "HS-grad", "education-num": 9,
    "marital-status": "Married-civ-spouse", "occupation": "Craft-repair",
    "relationship": "Husband", "race": "White", "sex": "Male",
    "capital-gain": 0, "capital-loss": 0, "hours-per-week": 68,
    "native-country": "United-States"
}).encode()

req = urllib.request.Request(
    "http://127.0.0.1:8001/api/v1/income_classifier/predict",
    data=data, headers={"Content-Type": "application/json"}, method="POST"
)
res = urllib.request.urlopen(req)
print(res.read().decode())
```

Expected output:
```json
{"probability": 0.04, "label": "<=50K", "status": "OK", "request_id": 1}
```

---

## CHAPTER 5 COMPLETE

The predict API endpoint is working! Predictions are saved to the database.

**Next: Chapter 6 â€” A/B Testing**

---



# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CHAPTER 6 â€” A/B Testing
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

## What You Will Do
- Create an A/B test that pits Random Forest vs Extra Trees
- Send predictions through the ab_testing endpoint
- Provide feedback (correct answers) for each prediction
- Stop the test and let the system automatically pick the winner

---

## STEP 1 â€” Verify Both Algorithms Are Registered

With the server running on port 8001, open:
`http://127.0.0.1:8001/api/v1/mlalgorithms`

You should see two algorithms:
- `"random forest"` with `current_status: "production"`
- `"extra trees"` with `current_status: "testing"`

Note the IDs (usually 1 and 2).

---

## STEP 2 â€” Create an A/B Test via Jupyter or Python Script

Open Jupyter Notebook or create a file `research/ab_test.py`.

```python
import requests

BASE = "http://127.0.0.1:8001/api/v1"

# Step 1: Create the A/B test
response = requests.post(f"{BASE}/abtests", json={
    "title": "Random Forest vs Extra Trees",
    "created_by": "your_name",
    "parent_mlalgorithm_1": 1,   # Random Forest ID
    "parent_mlalgorithm_2": 2    # Extra Trees ID
})
ab_test = response.json()
print("A/B Test created:", ab_test)
ab_test_id = ab_test["id"]
```

After this, check statuses â€” both algorithms should now be `ab_testing`:
```python
statuses = requests.get(f"{BASE}/mlalgorithmstatuses").json()
for s in statuses:
    if s["active"]:
        print(f"Algorithm {s['parent_mlalgorithm']}: {s['status']}")
```

---

## STEP 3 â€” Load Test Data and Send Predictions

```python
import pandas as pd
from sklearn.model_selection import train_test_split

# Load same dataset
df = pd.read_csv(
    'https://raw.githubusercontent.com/pplonski/datasets-for-start/master/adult/data.csv',
    skipinitialspace=True
)
X = df[[c for c in df.columns if c != 'income']]
y = df['income']
_, X_test, _, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)

# Send 100 predictions with correct feedback
for i in range(100):
    input_data = dict(X_test.iloc[i])
    # Convert NaN to None for JSON compatibility
    input_data = {k: (None if str(v) == 'nan' else v) for k, v in input_data.items()}
    correct_label = y_test.iloc[i]

    # Send prediction (randomly goes to RF or ET)
    r = requests.post(
        f"{BASE}/income_classifier/predict?status=ab_testing",
        json=input_data
    ).json()

    # Provide feedback so accuracy can be computed
    requests.put(
        f"{BASE}/mlrequests/{r['request_id']}",
        json={"feedback": correct_label}
    )

    if (i + 1) % 10 == 0:
        print(f"Sent {i+1} predictions...")

print("Done sending predictions!")
```

---

## STEP 4 â€” Stop the A/B Test

```python
result = requests.post(f"{BASE}/stop_ab_test/{ab_test_id}").json()
print("Result:", result)
```

Expected output:
```
Result: {
  "message": "AB Test finished.",
  "summary": "Algorithm #1 accuracy: 0.86, Algorithm #2 accuracy: 0.84"
}
```

The higher accuracy algorithm is automatically set to `"production"`.
The lower accuracy algorithm is set to `"testing"`.

---

## STEP 5 â€” Verify Final Statuses

```python
statuses = requests.get(f"{BASE}/mlalgorithmstatuses").json()
for s in statuses:
    if s["active"]:
        alg = "random_forest" if s["parent_mlalgorithm"] == 1 else "extra_trees"
        print(f"{alg}: {s['status']}")
```

---

## CHAPTER 6 COMPLETE

A/B Testing is fully working. The system automatically promotes the better model.



# ═══════════════════════════════════════
# CHAPTER 7 — Docker Container
# ═══════════════════════════════════════

## Do You Need Docker?

| Use Case | Docker Needed? |
|---|---|
| Local development & testing | **NO** — `python manage.py runserver` is enough |
| Deploy to a real server | **YES** |

> Download Docker Desktop: https://www.docker.com/products/docker-desktop/
> After installing, **restart your computer**, then open Docker Desktop and wait for it to show "Docker is running".

---

## STEP 1 — Create `requirements.txt` in the project root (`my_ml_service/`)

> ⚠️ **Important:** Use `Django==5.2.1` (not 6.0.5) in `requirements.txt` for Docker.
> Django 6.0.5 is only available locally. PyPI has up to Django 5.2.x for Docker builds.
> The code is fully compatible with both versions.

Create the file `my_ml_service/requirements.txt`:
```
Django==5.2.1
django-filter==25.1
djangorestframework==3.17.1
joblib==1.5.3
numpy==2.4.4
pandas==3.0.3
requests==2.34.0
scikit-learn==1.8.0
scipy==1.17.1
gunicorn==23.0.0
```

---

## STEP 2 — Create the Docker folder structure

```powershell
mkdir docker
mkdir docker\nginx
mkdir docker\backend
```

Your project should now have:
```
my_ml_service/
├── docker/
│   ├── backend/
│   └── nginx/
├── backend/
├── research/
├── requirements.txt
└── ...
```

---

## STEP 3 — Create `docker/nginx/Dockerfile`

```dockerfile
# docker/nginx/Dockerfile
FROM nginx:1.13.12-alpine
CMD ["nginx", "-g", "daemon off;"]
```

---

## STEP 4 — Create `docker/nginx/default.conf`

```nginx
server {
    listen 8000 default_server;
    listen [::]:8000;

    client_max_body_size 20M;

    location / {
        try_files $uri @proxy_api;
    }

    location @proxy_api {
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Url-Scheme $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://wsgiserver:8000;
    }

    location /static/ {
        autoindex on;
        alias /app/backend/server/static/;
    }
}
```

---

## STEP 5 — Create `docker/backend/Dockerfile`

```dockerfile
# docker/backend/Dockerfile
FROM python:3.11-slim

# Install system dependencies (libgomp1 needed for scikit-learn)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn==23.0.0

# Copy project files
ADD ./backend /app/backend
ADD ./docker  /app/docker
ADD ./research /app/research

# Create static files directory
RUN mkdir -p /app/backend/server/static
```

---

## STEP 6 — Create `docker/backend/wsgi-entrypoint.sh`

```bash
#!/usr/bin/env bash

echo "Starting backend server..."

# Wait for server volume
until cd /app/backend/server
do
    echo "Waiting for server volume..."
done

# Wait for DB to be ready and apply migrations
until python manage.py migrate
do
    echo "Waiting for database to be ready..."
    sleep 2
done

# Collect static files
python manage.py collectstatic --noinput

# Start gunicorn WSGI server (4 workers x 4 threads = 16 concurrent requests)
gunicorn server.wsgi \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --threads 4 \
    --timeout 120
```

> ⚠️ **Windows Users:** This `.sh` file MUST have **Unix line endings (LF)**, not Windows (CRLF).
> Fix it with this PowerShell command after creating the file:
> ```powershell
> $content = Get-Content "docker\backend\wsgi-entrypoint.sh" -Raw
> $content = $content -replace "`r`n", "`n"
> [System.IO.File]::WriteAllText("$PWD\docker\backend\wsgi-entrypoint.sh", $content, [System.Text.UTF8Encoding]::new($false))
> ```

---

## STEP 7 — Create `docker-compose.yml` in the project root

```yaml
services:

  nginx:
    restart: always
    image: nginx:1.25-alpine
    ports:
      - "8080:8000"
    volumes:
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/backend/server/static
    depends_on:
      - wsgiserver

  wsgiserver:
    build:
      context: .
      dockerfile: ./docker/backend/Dockerfile
    entrypoint: /app/docker/backend/wsgi-entrypoint.sh
    volumes:
      - static_volume:/app/backend/server/static
    expose:
      - "8000"
    environment:
      - DJANGO_SETTINGS_MODULE=server.settings

volumes:
  static_volume: {}
```

> **Port `8080:8000`** means: your browser connects to port 8080, Docker routes it to port 8000 inside.
> If port 8080 is busy, change to `"9000:8000"` or any free port.
> If port 8000 is free on your machine, you can use `"8000:8000"` instead.

---

## STEP 8 — Verify Docker is Ready

Open a **new** PowerShell terminal:
```powershell
docker --version
```

Expected:
```
Docker version 29.x.x, build xxxxxxx
```

If this fails, make sure Docker Desktop is running (check the system tray icon).

---

## STEP 9 — Build the Docker Image

```powershell
cd C:\Users\YourName\Desktop\my_ml_service
docker-compose build
```

> ⏳ First build takes **5–15 minutes** (downloads Python image, installs all packages).
> Subsequent builds are much faster because Docker caches unchanged layers.

---

## STEP 10 — Start the Containers

```powershell
docker-compose up -d
```

Expected:
```
Container my_ml_service-wsgiserver-1  Created
Container my_ml_service-nginx-1      Created
Container my_ml_service-wsgiserver-1  Started
Container my_ml_service-nginx-1      Started
```

Check the logs to confirm it started correctly:
```powershell
docker-compose logs wsgiserver
```

You should see:
```
Starting backend server...
Apply all migrations...
No migrations to apply.
154 static files copied to '/app/backend/server/static'.
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:8000
[INFO] Booting worker with pid: 24
[INFO] Booting worker with pid: 25
[INFO] Booting worker with pid: 26
[INFO] Booting worker with pid: 27
```

---

## STEP 11 — Test the Docker Deployment

Open your browser: **http://localhost:8080/api/v1/**

You should see the DRF API root with all 5 endpoints listed.

### Test a prediction:

In a terminal, run Python:
```python
import urllib.request, json

data = json.dumps({
    "age": 37, "workclass": "Private", "fnlwgt": 34146,
    "education": "HS-grad", "education-num": 9,
    "marital-status": "Married-civ-spouse", "occupation": "Craft-repair",
    "relationship": "Husband", "race": "White", "sex": "Male",
    "capital-gain": 0, "capital-loss": 0, "hours-per-week": 68,
    "native-country": "United-States"
}).encode()

req = urllib.request.Request(
    "http://localhost:8080/api/v1/income_classifier/predict",
    data=data, headers={"Content-Type": "application/json"}, method="POST"
)
res = urllib.request.urlopen(req)
print(res.read().decode())
```

Expected:
```json
{"probability": 0.04, "label": "<=50K", "status": "OK", "request_id": 1}
```

---

## Docker Commands Quick Reference

| Command | What It Does |
|---|---|
| `docker-compose build` | Build/rebuild images |
| `docker-compose up -d` | Start in background |
| `docker-compose up` | Start with live logs |
| `docker-compose down` | Stop and remove containers |
| `docker-compose logs -f` | Watch live logs |
| `docker-compose logs wsgiserver` | Backend logs only |
| `docker ps` | Show running containers |
| `docker-compose restart` | Restart containers |

## After Changing Code — Rebuild

```powershell
docker-compose down
docker-compose build
docker-compose up -d
```

---

## CHAPTER 7 COMPLETE

**Next: Chapter 8 — Using Your Own Dataset**

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CHAPTER 8 â€” Using Your Own Dataset
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

Yes, you can use any dataset! Here is what to change:

## In Jupyter (Chapter 2 changes):
1. Replace the CSV URL with your own file
2. Change `'income'` to your target column name
3. Update `categorical_columns` to match your dataset's text columns
4. Save models the same way with `joblib.dump()`

## In `random_forest.py` (Chapter 4 changes):
Update the categorical columns list:
```python
for column in ["your_col1", "your_col2"]:  # your columns
    input_data[column] = self.encoders[column].transform(input_data[column])
```

Update `postprocessing()` for your labels:
```python
def postprocessing(self, input_data):
    label = "class_A"
    if input_data[1] > 0.5:
        label = "class_B"
    return {"probability": float(input_data[1]), "label": label, "status": "OK"}
```

## In `wsgi.py` (Chapter 4 changes):
Change the endpoint name:
```python
registry.add_algorithm(
    endpoint_name="your_classifier_name",  # e.g. "house_predictor"
    ...
)
```

Then call predictions at: `POST /api/v1/your_classifier_name/predict`

## Example Datasets You Can Use:

| Dataset | Task | Where to Get |
|---|---|---|
| Iris | Flower species (3 classes) | `from sklearn.datasets import load_iris` |
| Titanic | Survived or not | Kaggle (free download) |
| Heart Disease | Disease or not | UCI ML Repository |
| Wine Quality | Quality score | UCI ML Repository |
| House Prices | Price prediction | Kaggle |

---

## All API Endpoints Reference

| Method | URL | What It Does |
|---|---|---|
| GET | `/api/v1/` | API root â€” lists all routes |
| GET | `/api/v1/endpoints` | List registered endpoints |
| GET | `/api/v1/mlalgorithms` | List registered algorithms + current status |
| GET | `/api/v1/mlalgorithmstatuses` | Full status history |
| GET | `/api/v1/mlrequests` | All prediction requests logged |
| GET | `/api/v1/abtests` | All A/B tests |
| POST | `/api/v1/income_classifier/predict` | Predict (uses production model) |
| POST | `/api/v1/income_classifier/predict?status=testing` | Predict with testing model |
| POST | `/api/v1/income_classifier/predict?status=ab_testing` | Predict via A/B split |
| POST | `/api/v1/abtests` | Create a new A/B test |
| POST | `/api/v1/stop_ab_test/{id}` | Stop test, declare winner |
| PUT | `/api/v1/mlrequests/{id}` | Add feedback to a prediction |
| GET | `/api/v1/admin/` | Django admin panel |

---

## THE END â€” Tutorial Complete!

