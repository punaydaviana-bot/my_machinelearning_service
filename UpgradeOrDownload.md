# ⬆️ Upgrade or Download Guide
## Python, Django, and All Packages

---

# PART 1 — INSTALL PYTHON (Fresh Install)

## Check if Python is already installed
Open CMD or PowerShell:
```bash
python --version
# Example output: Python 3.12.3
```

If you see `Python is not recognized` — Python is not installed.

---

## Download and Install Python (Windows)

1. Go to: **https://www.python.org/downloads/**
2. Click the yellow **"Download Python 3.x.x"** button (latest stable)
3. Run the installer `.exe`
4. ⚠️ **IMPORTANT:** Check the box **"Add Python to PATH"** before clicking Install
5. Click **"Install Now"**
6. Wait for installation to finish
7. Open a NEW terminal and verify:
```bash
python --version
pip --version
```

---

## Download a Specific Python Version

If you need a specific version (e.g. 3.11):
1. Go to: **https://www.python.org/downloads/windows/**
2. Scroll down to find `Python 3.11.x`
3. Click it → download `Windows installer (64-bit)`
4. Run and install with **"Add to PATH"** checked

---

# PART 2 — UPGRADE PYTHON

## Option A — Download the New Version (Recommended for Windows)

1. Go to **https://www.python.org/downloads/**
2. Download the latest version installer
3. Run it — it will upgrade your existing Python
4. Verify:
```bash
python --version
```

## Option B — Using winget (Windows 10/11 built-in package manager)
```powershell
# Check what's available
winget search Python.Python

# Install/upgrade specific version
winget install Python.Python.3.12

# Or upgrade all
winget upgrade Python.Python.3.12
```

## Option C — Using pyenv (Best for managing multiple versions)

Install pyenv-win:
```powershell
pip install pyenv-win --target "$HOME\.pyenv"
```

Then add to PATH (follow the pyenv-win setup instructions at https://github.com/pyenv-win/pyenv-win)

```bash
# List available versions
pyenv install --list

# Install a version
pyenv install 3.12.3

# Set as global default
pyenv global 3.12.3

# Verify
python --version
```

---

# PART 3 — INSTALL DJANGO (Fresh)

Always install Django inside a virtual environment, NOT globally.

```bash
# Step 1: Create venv (if not already)
python -m venv .venv

# Step 2: Activate venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

# Step 3: Install Django
pip install django

# Verify
python -m django --version
```

### Install a Specific Django Version
```bash
pip install django==6.0.5    # exact version
pip install "django>=5.0"    # minimum version
pip install "django>=4.2,<5" # version range
```

---

# PART 4 — UPGRADE DJANGO

## Check Current Version
```bash
python -m django --version
# or
pip show django
```

## Upgrade to Latest
```bash
pip install --upgrade django
```

## Upgrade to Specific Version
```bash
pip install django==6.0.5
```

## ⚠️ Before Upgrading Django — Check Compatibility

| Django Version | Python Versions Supported | Notes |
|---|---|---|
| Django 2.2 LTS | 3.5, 3.6, 3.7, 3.8 | Old — do not use |
| Django 3.2 LTS | 3.6, 3.7, 3.8, 3.9, 3.10 | Old LTS |
| Django 4.2 LTS | 3.8, 3.9, 3.10, 3.11, 3.12 | Current LTS (recommended stable) |
| Django 5.0 | 3.10, 3.11, 3.12 | Latest stable |
| Django 6.0 | 3.12+ | Newest (used in this project) |

> **LTS = Long Term Support** — gets security updates for 3 years.
> Recommended for production projects: **Django 4.2 LTS** or **Django 5.0+**

---

# PART 5 — UPGRADE ALL PROJECT PACKAGES

## See What's Installed
```bash
pip list
```

## See What's Outdated
```bash
pip list --outdated
```

## Upgrade a Single Package
```bash
pip install --upgrade scikit-learn
pip install --upgrade pandas
pip install --upgrade djangorestframework
```

## Upgrade Everything at Once (Use Carefully!)
```powershell
# Windows PowerShell:
pip freeze | ForEach-Object { $pkg = ($_ -split "==")[0]; pip install --upgrade $pkg }
```

```bash
# Mac/Linux:
pip freeze | grep -v "^-e" | cut -d "=" -f 1 | xargs pip install --upgrade
```

> ⚠️ WARNING: Upgrading all packages at once can break compatibility.
> Always test after upgrading.

---

# PART 6 — UPGRADE THIS PROJECT (my_ml_service) SPECIFICALLY

## Step 1: Activate venv
```powershell
# From my_ml_service/ folder:
.venv\Scripts\activate
```

## Step 2: Upgrade Django
```bash
pip install --upgrade django
python -m django --version
```

## Step 3: Upgrade Django REST Framework
```bash
pip install --upgrade djangorestframework
```

## Step 4: Upgrade ML packages
```bash
pip install --upgrade scikit-learn numpy pandas joblib scipy
```

## Step 5: Update requirements.txt
```bash
pip freeze > requirements.txt
```

## Step 6: Check for Django deprecation warnings
```bash
cd backend/server
python manage.py check
```

> If you see warnings like `WARNINGS: endpoints.Endpoint: (models.W042)` — these are just warnings, not errors. The project still works.

## Step 7: Re-run migrations if needed
```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 8: Run all tests to confirm nothing broke
```bash
python manage.py test apps
```

---

# PART 7 — COMMON UPGRADE ISSUES AND FIXES

## Issue: `url()` is removed (Django 4.0+)
**Error:** `ImportError: cannot import name 'url' from 'django.conf.urls'`
**Fix:** Replace `url(r'^...')` with `path(...)` in `urls.py`
```python
# OLD (Django 2.x):
from django.conf.urls import url
url(r'^api/', views.api)

# NEW (Django 4+):
from django.urls import path
path('api/', views.api)
```

## Issue: `DEFAULT_AUTO_FIELD` warning
**Warning:** `models.W042: Auto-created primary key...`
**Fix:** Add to `settings.py`:
```python
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

## Issue: Template `request` context processor missing
**Error:** Templates fail silently
**Fix:** In `settings.py` TEMPLATES section:
```python
"context_processors": [
    "django.template.context_processors.request",  # ← must be present
    ...
]
```

## Issue: `scikit-learn` version mismatch with saved models
**Error:** `InconsistentVersionWarning` when loading `.joblib` files
**Fix:** Re-train and re-save models with the new scikit-learn version (re-run Jupyter Chapter 2)

## Issue: `numpy` array API changes
**Error:** Various numpy deprecation errors
**Fix:** `pip install "numpy<2.0"` to pin old behavior, or update your code

---

# PART 8 — DOWNGRADE (If Upgrade Breaks Things)

## Downgrade Django
```bash
pip install django==4.2.0
```

## Downgrade a specific package
```bash
pip install scikit-learn==1.3.2
pip install numpy==1.26.4
pip install pandas==2.1.4
```

## Restore from requirements.txt (go back to working state)
```bash
pip install -r requirements.txt
```

---

# Quick Version Reference for This Project

| Package | Version Used | Upgrade Command |
|---|---|---|
| Python | 3.10+ | Download from python.org |
| Django | 6.0.5 | `pip install django==6.0.5` |
| djangorestframework | 3.17.1 | `pip install djangorestframework==3.17.1` |
| scikit-learn | 1.8.0 | `pip install scikit-learn==1.8.0` |
| numpy | 2.4.4 | `pip install numpy==2.4.4` |
| pandas | 3.0.3 | `pip install pandas==3.0.3` |
| joblib | 1.5.3 | `pip install joblib==1.5.3` |
| gunicorn | 23.0.0 | `pip install gunicorn==23.0.0` |
