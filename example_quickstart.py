"""
Quickstart Example: How to load and use the trained Electricity Demand Model
"""

from pathlib import Path
import joblib
import pandas as pd

# 1. Path to the trained model bundle
MODEL_PATH = Path(__file__).resolve().parent / "electricity_agent" / "artifacts" / "electricity_demand_model.joblib"

print(f"Loading model from: {MODEL_PATH} ...")
bundle = joblib.load(MODEL_PATH)

model = bundle["model"]
features = bundle["feature_names"]
metrics = bundle["metrics"]

print("\n Model Performance Metrics:")
for k, v in metrics.items():
    print(f"  • {k}: {v}")

print("\n Features used by the model:")
for i, f in enumerate(features, 1):
    print(f"  {i:2d}. {f}")

# 2. Example: Predict electricity for a custom/hypothetical country
# Provide the factors:
sample_country_factors = {
    "primary_energy_consumption": 2500.0,   # TWh
    "population": 85_000_000,              # 85 Million people
    "gdp": 4_000_000_000_000,              # $4.0 Trillion USD
    "gdp_per_capita": 47_000.0,            # $47,000 / person
    "electricity_access_pct": 100.0,       # 100% electrified
    "urban_pop_growth": 0.25,              # 0.25% urban growth
    "Total_RE_Capacity_MW_current": 120_000, # 120 GW renewables
    "Solar_PV_MW_current": 50_000,
    "Onshore_Wind_MW_current": 50_000,
    "Hydropower_MW_current": 15_000,
    "Bioenergy_MW_current": 5_000,
    "RE_Generation_Share_pct": 45.0,
    "RE_Capacity_Share_pct": 55.0,
    "Capacity_Generation_Gap_pct": 10.0,
    "Solar_Wind_Share_pct": 83.3,
}

df_input = pd.DataFrame([sample_country_factors])[features]
predicted_demand_twh = model.predict(df_input)[0]

print("\n Prediction on Hypothetical Country:")
print(f"  • Electricity Needed: {predicted_demand_twh:,.2f} TWh")
per_capita = (predicted_demand_twh * 1e9) / sample_country_factors["population"]
print(f"  • Per-Capita Demand:  {per_capita:,.1f} kWh / person")
