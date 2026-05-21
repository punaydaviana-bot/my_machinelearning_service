# 🧠 CHAPTER 2: Training the Machine Learning Models

## Creating and Running the Training Script

Originally, the tutorial asked you to run a Jupyter Notebook to train your models. We have automated this process into a single Python script (`research\train_industry_models.py`) to make it instantly repeatable if your data ever changes.

### Detailed Instructions & Explanations:
What exactly does this script do?
1. **Loads the Data:** It ingests `industry_exposure.csv` using the `pandas` library.
2. **Prepares the Target and Features:** It separates the `industry` column as the target we want to predict (`y`), and sets all other numeric vulnerability metrics as the input features (`X`).
3. **Splits the Data:** It sets aside 30% of your rows strictly for testing, ensuring the model is evaluated on data it hasn't memorized.
4. **Trains the Models:** It trains a `RandomForestClassifier` and an `ExtraTreesClassifier` on the remaining 70%.
5. **Saves Everything:** It dumps the models as compressed `.joblib` files directly into the `research\` folder so the Django backend can load them into memory.

### Step-by-step to Train:
Ensure your `venv` is activated, then run:
```powershell
# From the project root (ml_vivian_punay):
python research\train_industry_models.py
```

**Expected Output:**
You will see it confirm the data shape `Shape: (250, 14)` and then print:
```text
Random Forest trained!
Extra Trees trained!
All files saved!
```
The Django backend is now armed with fresh intelligence.
