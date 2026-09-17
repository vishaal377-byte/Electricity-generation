"""
Export comprehensive country data, future forecast curves, and 80/20 ML metrics
for the modern AMOLED dashboard.
"""

import json
from pathlib import Path
from electricity_agent.agent import ElectricityDemandAgent
from electricity_agent.config import COUNTRY_GROUPS, MODEL_FEATURES

agent = ElectricityDemandAgent()
countries = agent.loader.get_all_countries()

export_data = {
    "groups": COUNTRY_GROUPS,
    "metrics": agent.model.metrics,
    "feature_importances": agent.model.feature_importances,
    "benchmark_years": [2024, 2026, 2028, 2030, 2035, 2040, 2050],
    "countries": []
}

for c in countries:
    row = agent.loader.find_country_row(c)
    if row is None:
        continue
    try:
        res_2024 = agent.calculate_country(c, target_year=2024)
        factors = res_2024["projected_factors"]
        cagr = agent.loader._country_cagrs.get(c, {
            "pop_cagr": 0.008, "gdp_cagr": 0.025, "pe_cagr": 0.015, "re_add_mw_per_year": 500.0
        })

        # Precompute forecast across benchmark years
        forecasts = {}
        for yr in export_data["benchmark_years"]:
            pred = agent.calculate_country(c, target_year=yr)
            forecasts[str(yr)] = {
                "demand_twh": pred["predicted_demand_twh"],
                "per_capita_kwh": pred["per_capita_kwh"],
                "re_capacity_mw": pred["total_re_capacity_mw"],
            }

        export_data["countries"].append({
            "name": res_2024["country"],
            "iso": res_2024["iso_code"],
            "baseline_demand_twh": res_2024["predicted_demand_twh"],
            "actual_demand_historical_twh": res_2024["actual_demand_historical_twh"],
            "per_capita_kwh": res_2024["per_capita_kwh"],
            "re_capacity_mw": res_2024["total_re_capacity_mw"],
            "re_share_pct": res_2024["re_generation_share_pct"],
            "gap_pct": res_2024["capacity_generation_gap_pct"],
            "population": factors.get("population", 0),
            "gdp": factors.get("gdp", 0),
            "gdp_per_capita": factors.get("gdp_per_capita", 0),
            "primary_energy": factors.get("primary_energy_consumption", 0),
            "electrification_pct": factors.get("electricity_access_pct", 100),
            "solar_mw": factors.get("Solar_PV_MW_current", 0),
            "wind_mw": factors.get("Onshore_Wind_MW_current", 0),
            "hydro_mw": factors.get("Hydropower_MW_current", 0),
            "cagr": cagr,
            "forecasts": forecasts,
        })
    except Exception as e:
        continue

output_path = Path("/Users/vishaal/.gemini/antigravity/scratch/electricity_agent/artifacts/dashboard_data.json")
with open(output_path, "w") as f:
    json.dump(export_data, f, indent=2)

print(f"Exported {len(export_data['countries'])} countries to {output_path}")
