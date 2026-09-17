"""
Data loading, historical CAGR estimation, and future feature projection pipeline.
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from .config import (
    AUGMENTED_DATASET_PATH,
    CLEANED_DATASET_PATH,
    DEFAULT_BASE_YEAR,
    MODEL_FEATURES,
    TARGET_COL,
)


class DataLoader:
    """Handles loading, querying, and projecting electricity datasets."""

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
        self._country_cagrs: Dict[str, Dict[str, float]] = {}
        self.load_data()

    def load_data(self) -> None:
        """Loads sheets from Excel files and precomputes growth rates."""
        if self.augmented_path.exists():
            xl_aug = pd.ExcelFile(self.augmented_path)
            if "Demand_Model_Ready" in xl_aug.sheet_names:
                self._df_history = xl_aug.parse("Demand_Model_Ready")
            elif "OWID_Energy_History" in xl_aug.sheet_names:
                self._df_history = xl_aug.parse("OWID_Energy_History")

        if self.cleaned_path.exists():
            xl_clean = pd.ExcelFile(self.cleaned_path)
            if "ML_Ready_Cleaned" in xl_clean.sheet_names:
                self._df_ml_ready = xl_clean.parse("ML_Ready_Cleaned")

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

            # Latest profile per country
            self._df_latest = (
                self._df_history.sort_values("year")
                .groupby("country", as_index=False)
                .last()
            )

            # Compute historical growth trends per country (2010 to latest)
            self._compute_growth_rates()

    def _compute_growth_rates(self) -> None:
        """Computes CAGR for population, GDP, primary energy, and annual RE additions."""
        if self._df_history is None:
            return

        for country, group in self._df_history.groupby("country"):
            g_sorted = group.sort_values("year").dropna(
                subset=["primary_energy_consumption"]
            )
            if len(g_sorted) < 3:
                continue

            recent = g_sorted[g_sorted["year"] >= 2010]
            if len(recent) < 2:
                recent = g_sorted

            first = recent.iloc[0]
            last = recent.iloc[-1]
            dy = max(1, int(last["year"]) - int(first["year"]))

            # Population CAGR
            pop0, pop1 = first.get("population", 0), last.get("population", 0)
            pop_cagr = (
                float((pop1 / pop0) ** (1.0 / dy) - 1.0)
                if (pop0 > 0 and pop1 > 0)
                else 0.008
            )
            pop_cagr = max(-0.02, min(0.04, pop_cagr))  # bounded

            # GDP CAGR
            gdp0, gdp1 = first.get("gdp", 0), last.get("gdp", 0)
            gdp_cagr = (
                float((gdp1 / gdp0) ** (1.0 / dy) - 1.0)
                if (gdp0 > 0 and gdp1 > 0)
                else 0.025
            )
            gdp_cagr = max(-0.03, min(0.08, gdp_cagr))  # bounded

            # Primary Energy CAGR
            pe0, pe1 = (
                first.get("primary_energy_consumption", 0),
                last.get("primary_energy_consumption", 0),
            )
            pe_cagr = (
                float((pe1 / pe0) ** (1.0 / dy) - 1.0)
                if (pe0 > 0 and pe1 > 0)
                else 0.015
            )
            pe_cagr = max(-0.04, min(0.06, pe_cagr))

            # Annual Renewable Capacity Addition (MW/year)
            re0 = first.get("Total_RE_Capacity_MW_current", 0) or 0
            re1 = last.get("Total_RE_Capacity_MW_current", 0) or 0
            re_add = max(10.0, float(re1 - re0) / dy)

            self._country_cagrs[country] = {
                "pop_cagr": pop_cagr,
                "gdp_cagr": gdp_cagr,
                "pe_cagr": pe_cagr,
                "re_add_mw_per_year": re_add,
            }

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
        if self._df_latest is not None:
            return sorted(self._df_latest["country"].dropna().unique().tolist())
        return []

    def find_country_row(self, identifier: str) -> Optional[pd.Series]:
        if self._df_latest is None:
            return None

        q = identifier.strip().lower()
        matches = self._df_latest[
            (self._df_latest["country"].str.lower() == q)
            | (self._df_latest["iso_code"].str.lower() == q)
        ]
        if not matches.empty:
            return matches.iloc[0]

        sub_matches = self._df_latest[
            self._df_latest["country"].str.lower().str.contains(q, regex=False)
        ]
        if not sub_matches.empty:
            return sub_matches.iloc[0]

        return None

    def prepare_training_data(
        self,
    ) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
        """Prepares X, y, and metadata dataframe for ML model training."""
        if self._df_history is None:
            raise ValueError("History data is not loaded.")

        df_valid = self._df_history.dropna(subset=[TARGET_COL]).copy()

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
        """Extracts base features from a country Series."""
        feature_dict = {}
        for feat in MODEL_FEATURES:
            val = row.get(feat, np.nan)
            if pd.isnull(val):
                val = self._medians.get(feat, 0.0)
            feature_dict[feat] = float(val)
        return feature_dict

    def project_country_factors_to_year(
        self,
        row: pd.Series,
        target_year: int = DEFAULT_BASE_YEAR,
        factors_override: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """
        Projects a country's factors forward to any target year (2024-2050)
        using historical trends, compound growth rates, and clean energy additions.
        """
        base_features = self.extract_features_for_row(row)
        base_year = int(base_features.get("year", DEFAULT_BASE_YEAR))
        target_year = max(2000, min(2050, int(target_year)))
        dt = target_year - base_year

        country_name = str(row.get("country", ""))
        cagr = self._country_cagrs.get(
            country_name,
            {
                "pop_cagr": 0.008,
                "gdp_cagr": 0.025,
                "pe_cagr": 0.015,
                "re_add_mw_per_year": 500.0,
            },
        )

        projected = base_features.copy()
        projected["year"] = float(target_year)

        if dt > 0:
            # Future projection
            pop = projected["population"] * ((1.0 + cagr["pop_cagr"]) ** dt)
            projected["population"] = pop

            gdp = projected["gdp"] * ((1.0 + cagr["gdp_cagr"]) ** dt)
            projected["gdp"] = gdp
            if pop > 0:
                projected["gdp_per_capita"] = gdp / pop

            pe = projected["primary_energy_consumption"] * (
                (1.0 + cagr["pe_cagr"]) ** dt
            )
            projected["primary_energy_consumption"] = pe

            # Renewable capacity expansion
            re_add = cagr["re_add_mw_per_year"] * dt
            projected["Total_RE_Capacity_MW_current"] += re_add
            # Expand solar and wind proportionally
            projected["Solar_PV_MW_current"] += re_add * 0.55
            projected["Onshore_Wind_MW_current"] += re_add * 0.35

            # Gradual electrification expansion
            projected["electricity_access_pct"] = min(
                100.0, projected["electricity_access_pct"] + (0.5 * dt)
            )

        # Apply user overrides if specified
        if factors_override:
            for k, v in factors_override.items():
                if k in projected:
                    projected[k] = float(v)

        return projected
