"""
Intelligent Agent for calculating and forecasting electricity demand
for countries, regional bunches, future years, and what-if policy scenarios.
"""

from typing import Any, Dict, List, Optional, Union
import numpy as np
import pandas as pd

from .config import COUNTRY_GROUPS, DEFAULT_BASE_YEAR, MODEL_FEATURES
from .data_pipeline import DataLoader
from .model import ElectricityModel


class ElectricityDemandAgent:
    """
    Intelligent Agent that calculates and forecasts electricity demand for
    individual countries, regional clusters, future years (2024-2050),
    and what-if policy scenarios.
    """

    def __init__(
        self,
        loader: Optional[DataLoader] = None,
        model: Optional[ElectricityModel] = None,
        auto_train: bool = True,
    ):
        self.loader = loader or DataLoader()
        self.model = model or ElectricityModel()

        # Load pre-trained model or train if not present or needs update
        if not self.model.load():
            if auto_train:
                print("No trained model artifact found. Training new model (80% Train / 20% Test)...")
                X, y, _ = self.loader.prepare_training_data()
                self.model.train(X, y, medians=self.loader.feature_medians, test_size=0.20)
                self.model.save()
                print("Model trained and saved successfully.")

    def retrain_model(self, test_size: float = 0.20) -> Dict[str, Any]:
        """Explicitly retrain the model with the given train/test split."""
        X, y, _ = self.loader.prepare_training_data()
        metrics = self.model.train(
            X, y, medians=self.loader.feature_medians, test_size=test_size
        )
        self.model.save()
        return metrics

    def get_supported_groups(self) -> List[str]:
        return list(COUNTRY_GROUPS.keys())

    def get_countries_in_group(self, group_name: str) -> List[str]:
        return COUNTRY_GROUPS.get(group_name.upper(), [])

    def calculate_country(
        self,
        country_identifier: str,
        target_year: int = DEFAULT_BASE_YEAR,
        factors_override: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Calculates or forecasts electricity demand for a single country at a specified year.
        Projects factors forward if target_year > base_year (e.g. 2030, 2040, 2050).
        """
        row = self.loader.find_country_row(country_identifier)
        if row is None:
            raise ValueError(f"Country '{country_identifier}' not found in dataset.")

        country_name = str(row.get("country", country_identifier))
        iso_code = str(row.get("iso_code", ""))
        actual_demand = float(row.get("electricity_demand", 0.0))

        # Project factors to the target year (or baseline year)
        projected_factors = self.loader.project_country_factors_to_year(
            row, target_year=target_year, factors_override=factors_override
        )

        # Baseline features without override (for delta comparison)
        baseline_factors = self.loader.project_country_factors_to_year(
            row, target_year=target_year, factors_override=None
        )

        baseline_pred = self.model.predict_single(baseline_factors)
        scenario_pred = self.model.predict_single(projected_factors)

        pop = projected_factors.get("population", 0.0)
        per_capita_kwh = (scenario_pred * 1e9) / pop if pop > 0 else 0.0

        re_capacity_mw = projected_factors.get("Total_RE_Capacity_MW_current", 0.0)
        re_share_pct = projected_factors.get("RE_Generation_Share_pct", 0.0)
        gap_pct = projected_factors.get("Capacity_Generation_Gap_pct", 0.0)

        return {
            "country": country_name,
            "iso_code": iso_code,
            "target_year": int(target_year),
            "actual_demand_historical_twh": round(actual_demand, 2),
            "predicted_demand_twh": round(scenario_pred, 2),
            "baseline_predicted_twh": round(baseline_pred, 2),
            "delta_twh": round(scenario_pred - baseline_pred, 2),
            "delta_pct": round(
                ((scenario_pred - baseline_pred) / baseline_pred * 100)
                if baseline_pred > 0
                else 0.0,
                2,
            ),
            "per_capita_kwh": round(per_capita_kwh, 1),
            "total_re_capacity_mw": round(re_capacity_mw, 1),
            "re_generation_share_pct": round(re_share_pct, 1),
            "capacity_generation_gap_pct": round(gap_pct, 1),
            "projected_factors": projected_factors,
        }

    def calculate_bunch(
        self,
        countries_or_group: Union[str, List[str]],
        target_year: int = DEFAULT_BASE_YEAR,
        factors_override: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Calculates/forecasts electricity demand for a bunch of countries at a given year.
        """
        if isinstance(countries_or_group, str):
            group_key = countries_or_group.upper()
            if group_key in COUNTRY_GROUPS:
                country_list = COUNTRY_GROUPS[group_key]
                group_title = group_key
            else:
                country_list = [c.strip() for c in countries_or_group.split(",")]
                group_title = "Custom Selection"
        else:
            country_list = countries_or_group
            group_title = "Custom Selection"

        results = []
        not_found = []

        for c in country_list:
            try:
                res = self.calculate_country(
                    c, target_year=target_year, factors_override=factors_override
                )
                results.append(res)
            except ValueError:
                not_found.append(c)

        if not results:
            raise ValueError(
                f"None of the specified countries were found: {country_list}"
            )

        df_res = pd.DataFrame(results)
        total_predicted_twh = float(df_res["predicted_demand_twh"].sum())
        total_baseline_twh = float(df_res["baseline_predicted_twh"].sum())

        return {
            "group_name": group_title,
            "target_year": int(target_year),
            "country_count": len(results),
            "total_electricity_needed_twh": round(total_predicted_twh, 2),
            "total_baseline_twh": round(total_baseline_twh, 2),
            "total_delta_twh": round(total_predicted_twh - total_baseline_twh, 2),
            "not_found_countries": not_found,
            "countries": results,
            "summary_table": df_res[
                [
                    "country",
                    "iso_code",
                    "predicted_demand_twh",
                    "per_capita_kwh",
                    "total_re_capacity_mw",
                    "re_generation_share_pct",
                ]
            ],
        }

    def forecast_trajectory(
        self,
        countries_or_group: Union[str, List[str]],
        start_year: int = 2024,
        end_year: int = 2050,
        step: int = 1,
    ) -> Dict[str, Any]:
        """
        Computes year-by-year electricity demand forecasts from start_year to end_year.
        """
        years = list(range(start_year, end_year + 1, step))
        if isinstance(countries_or_group, str):
            group_key = countries_or_group.upper()
            country_list = (
                COUNTRY_GROUPS[group_key]
                if group_key in COUNTRY_GROUPS
                else [c.strip() for c in countries_or_group.split(",")]
            )
        else:
            country_list = countries_or_group

        trajectory_by_year = []
        for yr in years:
            bunch_res = self.calculate_bunch(country_list, target_year=yr)
            trajectory_by_year.append(
                {
                    "year": yr,
                    "total_twh": bunch_res["total_electricity_needed_twh"],
                    "country_demands": {
                        c["country"]: c["predicted_demand_twh"]
                        for c in bunch_res["countries"]
                    },
                }
            )

        return {
            "countries": country_list,
            "start_year": start_year,
            "end_year": end_year,
            "trajectory": trajectory_by_year,
        }

    def simulate_scenario(
        self,
        countries_or_group: Union[str, List[str]],
        target_year: int = DEFAULT_BASE_YEAR,
        gdp_growth_pct: float = 0.0,
        pop_growth_pct: float = 0.0,
        primary_energy_growth_pct: float = 0.0,
        re_capacity_expansion_pct: float = 0.0,
        target_electrification_pct: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Runs policy & economic scenario simulations across a bunch of countries
        at a specific target year.
        """
        if isinstance(countries_or_group, str):
            group_key = countries_or_group.upper()
            country_list = (
                COUNTRY_GROUPS[group_key]
                if group_key in COUNTRY_GROUPS
                else [c.strip() for c in countries_or_group.split(",")]
            )
            group_title = group_key if group_key in COUNTRY_GROUPS else "Custom Selection"
        else:
            country_list = countries_or_group
            group_title = "Custom Selection"

        simulated_countries = []

        for c in country_list:
            row = self.loader.find_country_row(c)
            if row is None:
                continue

            base_proj = self.loader.project_country_factors_to_year(
                row, target_year=target_year, factors_override=None
            )
            modified = base_proj.copy()

            if gdp_growth_pct != 0.0:
                modified["gdp"] *= 1.0 + (gdp_growth_pct / 100.0)
                modified["gdp_per_capita"] *= 1.0 + (gdp_growth_pct / 100.0)

            if pop_growth_pct != 0.0:
                modified["population"] *= 1.0 + (pop_growth_pct / 100.0)
                if gdp_growth_pct == 0.0 and modified["population"] > 0:
                    modified["gdp_per_capita"] = modified["gdp"] / modified["population"]

            if primary_energy_growth_pct != 0.0:
                modified["primary_energy_consumption"] *= 1.0 + (
                    primary_energy_growth_pct / 100.0
                )

            if re_capacity_expansion_pct != 0.0:
                mult = 1.0 + (re_capacity_expansion_pct / 100.0)
                modified["Total_RE_Capacity_MW_current"] *= mult
                modified["Solar_PV_MW_current"] *= mult
                modified["Onshore_Wind_MW_current"] *= mult
                modified["Hydropower_MW_current"] *= mult
                modified["Bioenergy_MW_current"] *= mult
                modified["RE_Capacity_Share_pct"] = min(
                    100.0, modified["RE_Capacity_Share_pct"] * mult
                )
                modified["RE_Generation_Share_pct"] = min(
                    100.0, modified["RE_Generation_Share_pct"] * mult
                )

            if target_electrification_pct is not None:
                modified["electricity_access_pct"] = max(
                    modified["electricity_access_pct"],
                    min(100.0, target_electrification_pct),
                )

            baseline_pred = self.model.predict_single(base_proj)
            scenario_pred = self.model.predict_single(modified)

            pop = modified.get("population", 1.0)
            per_capita_kwh = (scenario_pred * 1e9) / pop if pop > 0 else 0.0

            simulated_countries.append(
                {
                    "country": str(row.get("country", c)),
                    "iso_code": str(row.get("iso_code", "")),
                    "baseline_twh": round(baseline_pred, 2),
                    "scenario_twh": round(scenario_pred, 2),
                    "delta_twh": round(scenario_pred - baseline_pred, 2),
                    "delta_pct": round(
                        ((scenario_pred - baseline_pred) / baseline_pred * 100)
                        if baseline_pred > 0
                        else 0.0,
                        2,
                    ),
                    "per_capita_kwh": round(per_capita_kwh, 1),
                    "re_capacity_mw": round(
                        modified.get("Total_RE_Capacity_MW_current", 0.0), 1
                    ),
                }
            )

        df_sim = pd.DataFrame(simulated_countries)
        base_sum = float(df_sim["baseline_twh"].sum())
        scen_sum = float(df_sim["scenario_twh"].sum())

        return {
            "group_name": group_title,
            "target_year": int(target_year),
            "scenario_params": {
                "gdp_growth_pct": gdp_growth_pct,
                "pop_growth_pct": pop_growth_pct,
                "primary_energy_growth_pct": primary_energy_growth_pct,
                "re_capacity_expansion_pct": re_capacity_expansion_pct,
                "target_electrification_pct": target_electrification_pct,
            },
            "total_baseline_twh": round(base_sum, 2),
            "total_scenario_twh": round(scen_sum, 2),
            "total_delta_twh": round(scen_sum - base_sum, 2),
            "total_delta_pct": round(
                ((scen_sum - base_sum) / base_sum * 100) if base_sum > 0 else 0.0,
                2,
            ),
            "countries": simulated_countries,
            "table": df_sim,
        }

    def explain_country_factors(
        self, country_identifier: str, target_year: int = DEFAULT_BASE_YEAR
    ) -> Dict[str, Any]:
        """
        Explains which factors have the highest influence on electricity demand
        for the given country at the target year.
        """
        row = self.loader.find_country_row(country_identifier)
        if row is None:
            raise ValueError(f"Country '{country_identifier}' not found.")

        country_name = str(row.get("country", country_identifier))
        features = self.loader.project_country_factors_to_year(
            row, target_year=target_year
        )
        base_demand = self.model.predict_single(features)

        sensitivities = {}
        for feat in MODEL_FEATURES:
            if feat == "year":
                continue
            val = features[feat]
            perturbed = val + 1.0 if val == 0 else val * 1.10

            feat_copy = features.copy()
            feat_copy[feat] = perturbed
            new_pred = self.model.predict_single(feat_copy)
            diff = new_pred - base_demand
            sensitivities[feat] = {
                "current_value": round(val, 2),
                "sensitivity_impact_twh": round(diff, 4),
                "global_importance": round(
                    self.model.feature_importances.get(feat, 0.0), 4
                ),
            }

        sorted_sens = dict(
            sorted(
                sensitivities.items(),
                key=lambda item: abs(item[1]["sensitivity_impact_twh"]),
                reverse=True,
            )
        )

        return {
            "country": country_name,
            "target_year": int(target_year),
            "predicted_demand_twh": round(base_demand, 2),
            "factor_sensitivities": sorted_sens,
        }
