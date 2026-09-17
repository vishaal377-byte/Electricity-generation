"""
Quickstart Example: How to load and use the trained Electricity Demand Model
Supports future year forecasting and demonstrates 80/20 split metrics.
"""

from pathlib import Path
import joblib
import pandas as pd
from electricity_agent import ElectricityDemandAgent

# 1. Path to the trained model bundle
MODEL_PATH = Path(__file__).resolve().parent / "electricity_agent" / "artifacts" / "electricity_demand_model.joblib"

print(f"Loading model from: {MODEL_PATH} ...")
bundle = joblib.load(MODEL_PATH)

metrics = bundle["metrics"]
print("\n📊 Model Performance Metrics (Strict 80% Train / 20% Test Split):")
for k, v in metrics.items():
    print(f"  • {k}: {v}")

# 2. Using the Agent to forecast future electricity demand for a country
agent = ElectricityDemandAgent()

print("\n⚡ Forecasting Electricity Demand for India across Future Years:")
for yr in [2024, 2030, 2035, 2040, 2050]:
    res = agent.calculate_country("India", target_year=yr)
    print(f"  • Year {yr}: {res['predicted_demand_twh']:,.2f} TWh ({res['per_capita_kwh']:,.1f} kWh/person) | Proj. RE: {res['total_re_capacity_mw']:,.0f} MW")

# 3. Forecasting for a bunch of countries (e.g. G7 in 2035)
g7_2035 = agent.calculate_bunch("G7", target_year=2035)
print(f"\n⚡ G7 Combined Electricity Needed in 2035: {g7_2035['total_electricity_needed_twh']:,.2f} TWh across {g7_2035['country_count']} nations")
