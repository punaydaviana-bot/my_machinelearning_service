# ⚙️ CHAPTER 3: Django Backend & API Logic Modifications

## Explanation of Backend Changes

Once the `.joblib` files exist, they need to be served via Django. Here is what we changed from the tutorial to make it compatible with your `industry_exposure` dataset.

### 1. New App Routing
We transitioned the API away from `income_classifier` and renamed it appropriately to `industry_classifier` under `backend/server/apps/ml/industry_classifier/`.

### 2. Updating `random_forest.py` & `extra_trees.py`
These are the files that act as the bridge between Django and the ML model.
- **Skipped Preprocessing Code:** We entirely deleted the loop that applied `LabelEncoder` transformations. The `preprocessing` function now solely handles filling in missing values (NaNs).
- **Modified Postprocessing for Multi-Class:** In the tutorial's binary model, we just looked at index `[0]` to check if the probability was greater than `0.5`. Since we have 10 industries, the model now returns 10 different probabilities. We introduced `numpy.argmax()` to automatically scan the probabilities, locate the highest one, and return the corresponding industry label directly from the model's memory (`self.model.classes_`).

### 3. Registering the API in `wsgi.py`
The `MLRegistry` starts up alongside the Django server. We altered `backend/server/server/wsgi.py` to map these Python classes to a new REST endpoint URL named `"industry_classifier"`. We left Random Forest tagged as `"production"` and Extra Trees as `"testing"`.

This completes the pipeline setup. Next, we test it.
