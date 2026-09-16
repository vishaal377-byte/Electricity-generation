"""
ML Model training, evaluation, explainability, and inference pipeline.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import KFold, cross_val_predict

from .config import MODEL_BUNDLE_PATH, MODEL_FEATURES, TARGET_COL


class ElectricityModel:
    """Manages training, saving, loading, and predicting with ML model."""

    def __init__(self, model_path: Optional[Path] = None):
        self.model_path = model_path or MODEL_BUNDLE_PATH
        self.model: Optional[Any] = None
        self.feature_names: List[str] = list(MODEL_FEATURES)
        self.metrics: Dict[str, float] = {}
        self.feature_importances: Dict[str, float] = {}
        self.medians: Dict[str, float] = {}

    def train(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        medians: Optional[Dict[str, float]] = None,
        n_estimators: int = 150,
        random_state: int = 42,
    ) -> Dict[str, float]:
        """
        Trains an ensemble Random Forest model and performs 5-fold cross-validation.
        """
        self.medians = medians or {}
        self.feature_names = list(X.columns)

        # Regressor configuration
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=22,
            min_samples_split=3,
            min_samples_leaf=1,
            n_jobs=-1,
            random_state=random_state,
        )

        # 5-fold Cross-Validation
        kf = KFold(n_splits=5, shuffle=True, random_state=random_state)
        cv_preds = cross_val_predict(self.model, X, y, cv=kf, n_jobs=-1)

        r2 = float(r2_score(y, cv_preds))
        mae = float(mean_absolute_error(y, cv_preds))
        rmse = float(root_mean_squared_error(y, cv_preds))
        non_zero = y > 0.05
        mape = float(np.mean(np.abs((y[non_zero] - cv_preds[non_zero]) / y[non_zero])) * 100)

        self.metrics = {
            "r2_score": round(r2, 4),
            "mae_twh": round(mae, 2),
            "rmse_twh": round(rmse, 2),
            "mape_pct": round(mape, 2),
            "train_samples": int(len(X)),
        }

        # Fit final model on all data
        self.model.fit(X, y)

        # Calculate feature importances
        fi = self.model.feature_importances_
        sorted_indices = np.argsort(fi)[::-1]
        self.feature_importances = {
            self.feature_names[i]: float(fi[i]) for i in sorted_indices
        }

        return self.metrics

    def save(self, path: Optional[Path] = None) -> Path:
        """Saves trained model bundle to disk."""
        save_path = path or self.model_path
        save_path.parent.mkdir(parents=True, exist_ok=True)
        bundle = {
            "model": self.model,
            "feature_names": self.feature_names,
            "metrics": self.metrics,
            "feature_importances": self.feature_importances,
            "medians": self.medians,
        }
        joblib.dump(bundle, save_path)
        return save_path

    def load(self, path: Optional[Path] = None) -> bool:
        """Loads model bundle from disk."""
        load_path = path or self.model_path
        if not load_path.exists():
            return False

        bundle = joblib.load(load_path)
        self.model = bundle["model"]
        self.feature_names = bundle["feature_names"]
        self.metrics = bundle.get("metrics", {})
        self.feature_importances = bundle.get("feature_importances", {})
        self.medians = bundle.get("medians", {})
        return True

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predicts electricity demand (TWh) from features DataFrame."""
        if self.model is None:
            raise ValueError("Model is not trained or loaded.")

        # Ensure all required features are present
        X_eval = X.copy()
        for f in self.feature_names:
            if f not in X_eval.columns:
                X_eval[f] = self.medians.get(f, 0.0)
            else:
                X_eval[f] = X_eval[f].fillna(self.medians.get(f, 0.0))

        X_eval = X_eval[self.feature_names]
        preds = self.model.predict(X_eval)
        # Demand cannot be negative
        return np.maximum(0.0, preds)

    def predict_single(self, feature_dict: Dict[str, float]) -> float:
        """Predicts electricity demand for a single feature dictionary."""
        df_single = pd.DataFrame([feature_dict])
        pred = self.predict(df_single)[0]
        return float(pred)
