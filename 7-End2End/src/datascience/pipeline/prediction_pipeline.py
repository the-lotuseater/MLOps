import joblib
import numpy as np
import pandas as pd
from pathlib import Path

class PredictionPipeline:
    def __init__(self):
        self.model = joblib.load('artifacts/model_trainer/model.joblib')

    def predict(self, input):
        pred = self.model.predict(input)
        return pred


