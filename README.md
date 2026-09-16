# ⚡ Electricity Demand Intelligent Agent

An intelligent, Machine Learning-trained agent that predicts, forecasts, and calculates the amount of electricity needed for countries and country clusters ("bunches") using key demographic, macroeconomic, and energy transition factors.

Trained on master energy transition datasets combining IRENA renewable capacity data, IMF subsidy statistics, and Our World in Data (OWID) historical energy metrics across 218 countries.

---

## 🌟 Key Features

- **ML-Trained Model Pipeline ($R^2 = 0.9941$, MAE = $4.58\text{ TWh}$)**:
  - Predicts country electricity demand based on primary energy consumption, GDP, population, urbanization, electrification rates, and renewable capacity mixes.
- **Multi-Country "Bunch" Calculations**:
  - Compute aggregate electricity demand across country clusters (e.g. `G7`, `BRICS`, `EU_TOP`, `LATAM_TOP`, `ASIA_PACIFIC`, `GLOBAL_TOP_10`) or custom country lists.
- **What-If Policy & Scenario Simulations**:
  - Simulate macroeconomic changes (e.g., $+15\%$ GDP growth) and renewable transition targets (e.g., $+30\%$ solar/wind expansion).
- **Factor Sensitivity & Attribution**:
  - Analyze the elasticity and influence of individual factors on country electricity requirements.
- **Interactive Web Dashboard (`dashboard.html`)**:
  - Live interactive sliders, comparative SVG charts, country filters, and CSV export.
- **Full CLI & Interactive REPL**:
  - Command-line agent for rapid querying and scenario modeling.

---

## 📁 Repository Structure

```
.
├── electricity_agent/                  # Core package
│   ├── __init__.py                     # Package exports
│   ├── config.py                       # Configuration & country clusters
│   ├── data_pipeline.py                # DataLoader & feature engineering
│   ├── model.py                        # Scikit-learn Random Forest model wrapper
│   ├── agent.py                        # ElectricityDemandAgent core logic
│   ├── cli.py                          # CLI & interactive REPL interface
│   └── artifacts/
│       ├── electricity_demand_model.joblib  # Trained model bundle
│       └── dashboard_data.json              # Precomputed multi-country factor database
├── data/                               # Dataset files
│   ├── Energy_Transition_Master_Dataset_cleaned.xlsx
│   └── Energy_Transition_Master_Dataset_augmented.xlsx
├── tests/                              # Automated test suite
│   ├── test_data_pipeline.py
│   ├── test_model.py
│   └── test_agent.py
├── dashboard.html                      # Standalone interactive dashboard
├── example_quickstart.py               # Minimal Python quickstart example
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

### 2. Run the Interactive Web Dashboard

Open `dashboard.html` in any web browser:
```bash
open dashboard.html
```

---

## 💻 Using the Command-Line Agent (CLI)

### Calculate for a bunch of countries:
```bash
# Predefined group (e.g. G7, BRICS, EU_TOP):
python3 -m electricity_agent.cli bunch --group G7
python3 -m electricity_agent.cli bunch --group BRICS

# Custom list of countries:
python3 -m electricity_agent.cli bunch --countries "Australia,Brazil,South Africa,Norway"
```

### Calculate for a single country:
```bash
python3 -m electricity_agent.cli calculate --country "India"
```

### Run policy scenario simulations:
```bash
python3 -m electricity_agent.cli scenario --group BRICS --gdp-growth 10 --re-expansion 25
```

### Explain factor drivers:
```bash
python3 -m electricity_agent.cli explain --country "Germany"
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

# 1. Calculate for a single country
result = agent.calculate_country("India")
print(f"Predicted Demand: {result['predicted_demand_twh']} TWh")
print(f"Per-Capita: {result['per_capita_kwh']} kWh/person")

# 2. Calculate for a bunch of countries
g7 = agent.calculate_bunch("G7")
print(f"Total Electricity Needed: {g7['total_electricity_needed_twh']} TWh")

# 3. Simulate scenario
sim = agent.simulate_scenario("BRICS", gdp_growth_pct=10.0, re_capacity_expansion_pct=25.0)
print(f"Baseline: {sim['total_baseline_twh']} TWh -> Scenario: {sim['total_scenario_twh']} TWh")
```

---

## 🧪 Testing

Run the automated test suite:
```bash
python3 -m unittest discover -s tests
```

---

## 📊 Model Performance

| Metric | Score |
| :--- | :--- |
| **$R^2$ Score** | **0.9941** |
| **Mean Absolute Error (MAE)** | **4.58 TWh** |
| **RMSE** | **39.13 TWh** |
| **MAPE** | **9.19%** |
| **Training Records** | **5,148 country-years** |
