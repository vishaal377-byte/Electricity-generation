"""
Intelligent Agent for calculating electricity demand for countries and scenarios.
"""

from typing import Any, Dict, List, Optional, Union
import numpy as np
import pandas as pd

from .config import COUNTRY_GROUPS, MODEL_FEATURES
from .data_pipeline import DataLoader
from .model import ElectricityModel


class ElectricityDemandAgent:
    """
    Intelligent Agent that calculates and forecasts electricity demand for
    individual countries, regional clusters, and what-if policy scenarios.
    """

    def __init__(
        self,
        loader: Optional[DataLoader] = None,
        model: Optional[ElectricityModel] = None,
        auto_train: bool = True,
    ):
        self.loader = loader or DataLoader()
        self.model = model or ElectricityModel()

        # Load pre-trained model or train if not present
        if not self.model.load():
            if auto_train:
                print("No trained model artifact found. Training new model...")
                X, y, _ = self.loader.prepare_training_data()
                self.model.train(X, y, medians=self.loader.feature_medians)
                self.model.save()
                print("Model trained and saved successfully.")

    def get_supported_groups(self) -> List[str]:
        """Returns pre-configured groups of countries."""
        return list(COUNTRY_GROUPS.keys())

    def get_countries_in_group(self, group_name: str) -> List[str]:
        """Returns the list of country names in a group."""
        return COUNTRY_GROUPS.get(group_name.upper(), [])

    def calculate_country(
        self,
        country_identifier: str,
        factors_override: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Calculates electricity demand for a single country.
        Allows overriding any factor (e.g. GDP, population, RE capacity).
        """
        row = self.loader.find_country_row(country_identifier)
        if row is None:
            raise ValueError(f"Country '{country_identifier}' not found in dataset.")

        country_name = str(row.get("country", country_identifier))
        iso_code = str(row.get("iso_code", ""))
        year = int(row.get("year", 2022)) if pd.notnull(row.get("year")) else 2022
        actual_demand = float(row.get("electricity_demand", 0.0))

        # Base features
        features = self.loader.extract_features_for_row(row)

        # Baseline prediction
        baseline_pred = self.model.predict_single(features)

        # Apply overrides if provided
        overridden_features = features.copy()
        if factors_override:
            for k, v in factors_override.items():
                if k in overridden_features:
                    overridden_features[k] = float(v)

            scenario_pred = self.model.predict_single(overridden_features)
        else:
            scenario_pred = baseline_pred

        # Population and per-capita metrics
        pop = overridden_features.get("population", 0.0)
        per_capita_kwh = (
            (scenario_pred * 1e9) / pop if pop > 0 else 0.0
        )

        # Energy transition context
        re_capacity_mw = overridden_features.get("Total_RE_Capacity_MW_current", 0.0)
        re_share_pct = overridden_features.get("RE_Generation_Share_pct", 0.0)
        gap_pct = overridden_features.get("Capacity_Generation_Gap_pct", 0.0)

        return {
            "country": country_name,
            "iso_code": iso_code,
            "reference_year": year,
            "actual_demand_twh": round(actual_demand, 2),
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
            "applied_factors": overridden_features,
        }

    def calculate_bunch(
        self,
        countries_or_group: Union[str, List[str]],
        factors_override: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Calculates electricity demand for a bunch of countries.
        Can be a group key (e.g. 'G7', 'BRICS') or an explicit list of country names/ISO codes.
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
                res = self.calculate_country(c, factors_override=factors_override)
                results.append(res)
            except ValueError:
                not_found.append(c)

        if not results:
            raise ValueError(
                f"None of the specified countries were found: {country_list}"
            )

        df_res = pd.DataFrame(results)

        total_actual_twh = float(df_res["actual_demand_twh"].sum())
        total_predicted_twh = float(df_res["predicted_demand_twh"].sum())
        total_baseline_twh = float(df_res["baseline_predicted_twh"].sum())

        return {
            "group_name": group_title,
            "country_count": len(results),
            "total_electricity_needed_twh": round(total_predicted_twh, 2),
            "total_baseline_twh": round(total_baseline_twh, 2),
            "total_delta_twh": round(total_predicted_twh - total_baseline_twh, 2),
            "total_actual_twh": round(total_actual_twh, 2),
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

    def simulate_scenario(
        self,
        countries_or_group: Union[str, List[str]],
        gdp_growth_pct: float = 0.0,
        pop_growth_pct: float = 0.0,
        primary_energy_growth_pct: float = 0.0,
        re_capacity_expansion_pct: float = 0.0,
        target_electrification_pct: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Runs policy & economic scenario simulations across a bunch of countries.
        Simulates proportional changes to GDP, population, renewable capacity, etc.
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

        simulated_countries = []

        for c in country_list:
            row = self.loader.find_country_row(c)
            if row is None:
                continue

            base_features = self.loader.extract_features_for_row(row)
            modified = base_features.copy()

            # Apply proportional changes
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
                # Boost renewable generation share proportionally up to 100%
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

            baseline_pred = self.model.predict_single(base_features)
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

    def explain_country_factors(self, country_identifier: str) -> Dict[str, Any]:
        """
        Explains which factors have the highest influence on electricity demand
        for the given country.
        """
        row = self.loader.find_country_row(country_identifier)
        if row is None:
            raise ValueError(f"Country '{country_identifier}' not found.")

        country_name = str(row.get("country", country_identifier))
        features = self.loader.extract_features_for_row(row)
        base_demand = self.model.predict_single(features)

        # Sensitivity analysis: perturb each factor by +10% and see response
        sensitivities = {}
        for feat in MODEL_FEATURES:
            val = features[feat]
            if val == 0:
                perturbed = val + 1.0
            else:
                perturbed = val * 1.10

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

        # Sort by sensitivity impact
        sorted_sens = dict(
            sorted(
                sensitivities.items(),
                key=lambda item: abs(item[1]["sensitivity_impact_twh"]),
                reverse=True,
            )
        )

        return {
            "country": country_name,
            "predicted_demand_twh": round(base_demand, 2),
            "factor_sensitivities": sorted_sens,
        }
