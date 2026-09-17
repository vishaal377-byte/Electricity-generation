# ⚡ Electricity Demand Intelligent Agent

An intelligent, Machine Learning-trained agent that predicts, forecasts, and calculates the amount of electricity needed for countries and country clusters ("bunches") at any target year (2024–2050) using demographic, macroeconomic, and energy transition factors.

Trained on master energy transition datasets combining IRENA renewable capacity data, IMF subsidy statistics, and Our World in Data (OWID) historical energy metrics across 218 countries.

---

## 🌟 Key Features

- **Strict 80% Train / 20% Test ML Model ($R^2 = 0.9979$, MAE = $4.31\text{ TWh}$)**:
  - Trained strictly on an 80% data split (4,118 records) and evaluated on a 20% unseen holdout test set (1,030 records).
- **Future Year Forecasting (2024–2050)**:
  - Forecast electricity consumption for any specific target year (e.g. 2025, 2030, 2035, 2040, 2050).
  - Uses country-specific compound annual growth rates (CAGRs) for population, GDP, primary energy, and annual renewable capacity additions.
- **Multi-Country "Bunch" Calculations**:
  - Compute aggregate electricity demand across country clusters (e.g. `G7`, `BRICS`, `EU_TOP`, `LATAM_TOP`, `ASIA_PACIFIC`, `GLOBAL_TOP_10`) or custom country lists.
- **Modern AMOLED Dark & Light Mode Web Dashboard (`dashboard.html`)**:
  - True pitch-black AMOLED dark theme with glowing neon cyan/emerald accents and clean modern light mode.
  - Interactive future year slider ($2024$ to $2050$), quick year presets, and interactive SVG trajectory curve (2024–2050).
- **Full CLI with Future Trajectory Support**:
  - Command-line agent supporting `--year` and `trajectory` forecasting.

---

## 📁 Repository Structure

```
.
├── electricity_agent/                  # Core package
│   ├── __init__.py                     # Package exports
│   ├── config.py                       # Configuration & country clusters
│   ├── data_pipeline.py                # DataLoader & future factor projection engine
│   ├── model.py                        # 80/20 train/test ML model pipeline
│   ├── agent.py                        # ElectricityDemandAgent core logic
│   ├── cli.py                          # CLI with --year & trajectory forecasting
│   └── artifacts/
│       ├── electricity_demand_model.joblib  # Trained model bundle (R²=0.9979)
│       └── dashboard_data.json              # Precomputed multi-country factor database
├── data/                               # Dataset files
│   ├── Energy_Transition_Master_Dataset_cleaned.xlsx
│   └── Energy_Transition_Master_Dataset_augmented.xlsx
├── tests/                              # Automated test suite (12 tests)
│   ├── test_data_pipeline.py
│   ├── test_model.py
│   └── test_agent.py
├── dashboard.html                      # Modern AMOLED dashboard with Light/Dark toggle
├── example_quickstart.py               # Standalone Python quickstart example
├── requirements.txt                    # Project dependencies
└── README.md                           # Documentation
```

---

## 🚀 Quickstart

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/vishaal377-byte/Electricity-generation.git
cd Electricity-generation

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the AMOLED Web Dashboard

Open `dashboard.html` in any web browser:
```bash
open dashboard.html
```

---

## 💻 Using the Command-Line Agent (CLI)

### Future Year Forecasts:
```bash
# Calculate electricity needed for India in 2030:
python3 -m electricity_agent.cli calculate --country "India" --year 2030

# Calculate for G7 in 2035:
python3 -m electricity_agent.cli bunch --group G7 --year 2035

# View annual trajectory curve (2024 to 2040) for BRICS:
python3 -m electricity_agent.cli trajectory --group BRICS --start-year 2024 --end-year 2040 --step 2
```

### Policy Scenario Simulations:
```bash
python3 -m electricity_agent.cli scenario --group BRICS --year 2030 --gdp-growth 10 --re-expansion 25
```

### Factor Sensitivity Analysis:
```bash
python3 -m electricity_agent.cli explain --country "Germany" --year 2030
```

### Launch Interactive REPL:
```bash
python3 -m electricity_agent.cli interactive
```

---

## 🐍 Python API Usage

```python
from electricity_agent import ElectricityDemandAgent

agent = ElectricityDemandAgent()

# 1. Forecast for a country at a specific future year (e.g. 2030)
india_2030 = agent.calculate_country("India", target_year=2030)
print(f"India 2030 Forecast: {india_2030['predicted_demand_twh']} TWh ({india_2030['per_capita_kwh']} kWh/person)")

# 2. Forecast for a bunch of countries in 2035
g7_2035 = agent.calculate_bunch("G7", target_year=2035)
print(f"G7 2035 Total: {g7_2035['total_electricity_needed_twh']} TWh")

# 3. Forecast year-by-year trajectory
traj = agent.forecast_trajectory("BRICS", start_year=2024, end_year=2035)
for pt in traj["trajectory"]:
    print(f"Year {pt['year']}: {pt['total_twh']} TWh")
```

---

## 📊 Model Performance (Strict 80% Train / 20% Test Split)

| Metric | Score | Note |
| :--- | :--- | :--- |
| **Split Ratio** | **80% Train / 20% Test** | 4,118 training records / 1,030 test records |
| **Test $R^2$ Score** | **0.9979** | Evaluated on unseen 20% holdout test set |
| **Test MAE** | **4.31 TWh** | Mean absolute error on test set |
| **Test RMSE** | **23.19 TWh** | Root mean squared error on test set |
| **Test MAPE** | **7.01%** | Mean absolute percentage error |
