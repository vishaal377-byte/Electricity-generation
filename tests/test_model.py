"""
Unit tests for ML model.
Verifies 80% Train / 20% Test split and holdout evaluation.
"""

import unittest
from pathlib import Path
import tempfile
from electricity_agent.data_pipeline import DataLoader
from electricity_agent.model import ElectricityModel


class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loader = DataLoader()
        cls.model = ElectricityModel()
        cls.is_loaded = cls.model.load()

    def test_model_loaded_or_trained(self):
        self.assertTrue(self.is_loaded, "Model should be loaded from bundle")
        self.assertIsNotNone(self.model.model)
        self.assertIn("test_r2_score", self.model.metrics)
        self.assertGreaterEqual(self.model.metrics["test_r2_score"], 0.95)
        self.assertEqual(self.model.metrics["split_ratio"], "80% Train / 20% Test")

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
            self.assertEqual(new_model.metrics["split_ratio"], "80% Train / 20% Test")


if __name__ == "__main__":
    unittest.main()
