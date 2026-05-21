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