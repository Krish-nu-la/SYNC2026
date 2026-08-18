import joblib
import xgboost as xgb
from pathlib import Path

from app.core.logger import logger


class ModelLoader:

    def __init__(self):

        self.model = None
        self.encoders = None
        self.features = None

    def load(self):

        if self.model is not None:
            return self.model

        model_dir = Path("app/ml/models")

        # Load native XGBoost model
        self.model = xgb.XGBRegressor()

        self.model.load_model(
            model_dir / "flood_model.json"
        )

        # Load supporting artifacts
        self.encoders = joblib.load(
            model_dir / "encoders.pkl"
        )

        self.features = joblib.load(
            model_dir / "feature_columns.pkl"
        )

        logger.info("AI Model Loaded")

        return self.model


model_loader = ModelLoader()