# 📖 CHAPTER 1: Phase Overview & Setup

## Explanation of What We Skipped and Why

In the original tutorial (`Tutorial.md`), the project used the Adult Income dataset and involved a process called **Label Encoding**. That process was needed because the data contained categorical strings (like `"Private"` or `"HS-grad"`), which machine learning models cannot understand mathematically. 

**Why we skipped this:** 
Your dataset, `industry_exposure.csv`, is structured differently. Every feature representing an exposure or vulnerability metric (like `pandemic_exposure: 7.8` or `cyber_exposure: 6.1`) is already numeric. Therefore, we **skipped the entire categorical Label Encoding logic** in the models.

We also replaced the original **Binary Classification** (predicting just two outcomes: `<=50K` or `>50K`) with **Multi-Class Classification**. Your models are now engineered to predict 10 distinct outcomes (the different `industry` names).

## Step 1: Activating the Environment

Before we do anything, the environment must be activated. This isolated space ensures that the upgraded Python, Django 6.0.5, and ML dependencies (like pandas and scikit-learn) do not conflict with your global computer settings.

**Instructions:**
1. Open PowerShell.
2. Navigate to your project folder:
   ```powershell
   cd C:\Users\provu\Desktop\ml_vivian_punay
   ```
3. Activate the virtual environment:
   ```powershell
   venv\Scripts\activate
   ```
*(You will know it worked if you see `(venv)` at the beginning of your terminal line).*
