"""
Unit tests for ML model.
"""

import unittest
from pathlib import Path
import tempfile
import pandas as pd
from electricity_agent.data_pipeline import DataLoader
from electricity_agent.model import ElectricityModel
from electricity_agent.config import MODEL_BUNDLE_PATH


class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loader = DataLoader()
        cls.model = ElectricityModel()
        cls.is_loaded = cls.model.load()

    def test_model_loaded_or_trained(self):
        self.assertTrue(self.is_loaded, "Model should be loaded from bundle")
        self.assertIsNotNone(self.model.model)
        self.assertIn("r2_score", self.model.metrics)
        self.assertGreaterEqual(self.model.metrics["r2_score"], 0.95)

    def test_prediction_output(self):
        X, _, _ = self.loader.prepare_training_data()
        preds = self.model.predict(X.head(10))
        self.assertEqual(len(preds), 10)
        self.assertTrue((preds >= 0).all(), "Demand predictions should be non-negative")

    def test_model_save_and_reload(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / "test_model.joblib"
            self.model.save(tmp_path)
            self.assertTrue(tmp_path.exists())

            new_model = ElectricityModel(model_path=tmp_path)
            loaded = new_model.load()
            self.assertTrue(loaded)
            self.assertEqual(new_model.feature_names, self.model.feature_names)


if __name__ == "__main__":
    unittest.main()
