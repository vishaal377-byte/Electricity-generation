"""
Unit tests for data pipeline.
"""

import unittest
import pandas as pd
from electricity_agent.data_pipeline import DataLoader
from electricity_agent.config import MODEL_FEATURES, TARGET_COL


class TestDataPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loader = DataLoader()

    def test_data_loaded(self):
        self.assertIsNotNone(self.loader.history_data)
        self.assertFalse(self.loader.history_data.empty)
        self.assertGreater(len(self.loader.get_all_countries()), 150)

    def test_find_country_row(self):
        row_usa = self.loader.find_country_row("United States")
        self.assertIsNotNone(row_usa)
        self.assertEqual(row_usa["iso_code"], "USA")

        row_ind = self.loader.find_country_row("ind")
        self.assertIsNotNone(row_ind)
        self.assertEqual(row_ind["iso_code"], "IND")

        row_nonexistent = self.loader.find_country_row("Atlantis")
        self.assertIsNone(row_nonexistent)

    def test_prepare_training_data(self):
        X, y, meta = self.loader.prepare_training_data()
        self.assertEqual(len(X), len(y))
        self.assertEqual(len(X), len(meta))
        self.assertEqual(list(X.columns), MODEL_FEATURES)
        self.assertFalse(X.isnull().any().any(), "Training features should have no NaNs")
        self.assertFalse(y.isnull().any(), "Training targets should have no NaNs")


if __name__ == "__main__":
    unittest.main()
