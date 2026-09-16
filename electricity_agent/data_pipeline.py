"""
Data loading and preprocessing pipeline for the Electricity Demand Agent.
"""

from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from .config import (
    CLEANED_DATASET_PATH,
    AUGMENTED_DATASET_PATH,
    MODEL_FEATURES,
    TARGET_COL,
)


class DataLoader:
    """Handles loading, querying, and preparing electricity datasets."""

    def __init__(
        self,
        cleaned_path: Optional[str] = None,
        augmented_path: Optional[str] = None,
    ):
        self.cleaned_path = cleaned_path or CLEANED_DATASET_PATH
        self.augmented_path = augmented_path or AUGMENTED_DATASET_PATH
        self._df_history: Optional[pd.DataFrame] = None
        self._df_ml_ready: Optional[pd.DataFrame] = None
        self._df_latest: Optional[pd.DataFrame] = None
        self._medians: Dict[str, float] = {}
        self.load_data()

    def load_data(self) -> None:
        """Loads sheets from Excel files."""
        # Load Demand_Model_Ready from augmented workbook if available
        if self.augmented_path.exists():
            xl_aug = pd.ExcelFile(self.augmented_path)
            if "Demand_Model_Ready" in xl_aug.sheet_names:
                self._df_history = xl_aug.parse("Demand_Model_Ready")
            elif "OWID_Energy_History" in xl_aug.sheet_names:
                self._df_history = xl_aug.parse("OWID_Energy_History")

        # Load ML_Ready_Cleaned from cleaned workbook
        if self.cleaned_path.exists():
            xl_clean = pd.ExcelFile(self.cleaned_path)
            if "ML_Ready_Cleaned" in xl_clean.sheet_names:
                self._df_ml_ready = xl_clean.parse("ML_Ready_Cleaned")

        # Fallback if augmented is not present: build from cleaned
        if self._df_history is None and self._df_ml_ready is not None:
            self._df_history = self._df_ml_ready.copy()

        # Compute medians for feature imputation
        if self._df_history is not None:
            for feat in MODEL_FEATURES:
                if feat in self._df_history.columns:
                    val = self._df_history[feat].median()
                    self._medians[feat] = float(val) if pd.notnull(val) else 0.0
                else:
                    self._medians[feat] = 0.0

        # Construct latest country profiles (using latest available year per country)
        if self._df_history is not None:
            self._df_latest = (
                self._df_history.sort_values("year")
                .groupby("country", as_index=False)
                .last()
            )

    @property
    def history_data(self) -> pd.DataFrame:
        return self._df_history

    @property
    def latest_data(self) -> pd.DataFrame:
        return self._df_latest

    @property
    def feature_medians(self) -> Dict[str, float]:
        return self._medians

    def get_all_countries(self) -> List[str]:
        """Returns sorted list of available countries."""
        if self._df_latest is not None:
            return sorted(self._df_latest["country"].dropna().unique().tolist())
        return []

    def find_country_row(self, identifier: str) -> Optional[pd.Series]:
        """
        Find the latest row for a given country name or iso_code (case-insensitive).
        """
        if self._df_latest is None:
            return None

        q = identifier.strip().lower()
        # Direct match on country or iso_code
        matches = self._df_latest[
            (self._df_latest["country"].str.lower() == q)
            | (self._df_latest["iso_code"].str.lower() == q)
        ]
        if not matches.empty:
            return matches.iloc[0]

        # Partial substring match
        sub_matches = self._df_latest[
            self._df_latest["country"].str.lower().str.contains(q, regex=False)
        ]
        if not sub_matches.empty:
            return sub_matches.iloc[0]

        return None

    def prepare_training_data(
        self,
    ) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
        """
        Prepares X, y, and metadata dataframe for ML model training.
        Fills missing values with precomputed medians.
        """
        if self._df_history is None:
            raise ValueError("History data is not loaded.")

        df_valid = self._df_history.dropna(subset=[TARGET_COL]).copy()

        # Fill features with medians
        for feat in MODEL_FEATURES:
            if feat not in df_valid.columns:
                df_valid[feat] = self._medians.get(feat, 0.0)
            else:
                df_valid[feat] = df_valid[feat].fillna(self._medians.get(feat, 0.0))

        X = df_valid[MODEL_FEATURES].copy()
        y = df_valid[TARGET_COL].copy()
        meta = df_valid[["country", "iso_code", "year"]].copy()

        return X, y, meta

    def extract_features_for_row(self, row: pd.Series) -> Dict[str, float]:
        """Extracts and imputes features from a country Series."""
        feature_dict = {}
        for feat in MODEL_FEATURES:
            val = row.get(feat, np.nan)
            if pd.isnull(val):
                val = self._medians.get(feat, 0.0)
            feature_dict[feat] = float(val)
        return feature_dict
