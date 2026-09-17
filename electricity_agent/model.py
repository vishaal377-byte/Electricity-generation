"""
ML Model training, evaluation, explainability, and inference pipeline.
Enforces strict 80% Train / 20% Test split.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

from .config import MODEL_BUNDLE_PATH, MODEL_FEATURES, TARGET_COL


class ElectricityModel:
    """Manages training, saving, loading, and predicting with ML model."""

    def __init__(self, model_path: Optional[Path] = None):
        self.model_path = model_path or MODEL_BUNDLE_PATH
        self.model: Optional[Any] = None
        self.feature_names: List[str] = list(MODEL_FEATURES)
        self.metrics: Dict[str, Any] = {}
        self.feature_importances: Dict[str, float] = {}
        self.medians: Dict[str, float] = {}

    def train(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        medians: Optional[Dict[str, float]] = None,
        test_size: float = 0.20,
        n_estimators: int = 150,
        random_state: int = 42,
    ) -> Dict[str, Any]:
        """
        Trains the Random Forest model strictly using an 80% Train / 20% Test split.
        Evaluates metrics on the unseen 20% holdout test dataset.
        """
        self.medians = medians or {}
        self.feature_names = list(X.columns)

        # Strict 80% Train / 20% Test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        # Regressor configuration
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=22,
            min_samples_split=3,
            min_samples_leaf=1,
            n_jobs=-1,
            random_state=random_state,
        )

        # Train on 80% train set
        self.model.fit(X_train, y_train)

        # Evaluate strictly on 20% unseen test set
        test_preds = self.model.predict(X_test)
        test_r2 = float(r2_score(y_test, test_preds))
        test_mae = float(mean_absolute_error(y_test, test_preds))
        test_rmse = float(root_mean_squared_error(y_test, test_preds))

        non_zero = y_test > 0.05
        test_mape = float(
            np.mean(np.abs((y_test[non_zero] - test_preds[non_zero]) / y_test[non_zero])) * 100
        )

        # Also compute train metrics for completeness
        train_preds = self.model.predict(X_train)
        train_r2 = float(r2_score(y_train, train_preds))

        self.metrics = {
            "test_r2_score": round(test_r2, 4),
            "test_mae_twh": round(test_mae, 2),
            "test_rmse_twh": round(test_rmse, 2),
            "test_mape_pct": round(test_mape, 2),
            "train_r2_score": round(train_r2, 4),
            "train_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "split_ratio": f"{int((1 - test_size) * 100)}% Train / {int(test_size * 100)}% Test",
        }

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

        X_eval = X.copy()
        for f in self.feature_names:
            if f not in X_eval.columns:
                X_eval[f] = self.medians.get(f, 0.0)
            else:
                X_eval[f] = X_eval[f].fillna(self.medians.get(f, 0.0))

        X_eval = X_eval[self.feature_names]
        preds = self.model.predict(X_eval)
        return np.maximum(0.0, preds)

    def predict_single(self, feature_dict: Dict[str, float]) -> float:
        """Predicts electricity demand for a single feature dictionary."""
        df_single = pd.DataFrame([feature_dict])
        pred = self.predict(df_single)[0]
        return float(pred)
