"""
Configuration settings, dataset paths, feature lists, and regional groupings.
"""

from pathlib import Path

# Base Paths
PACKAGE_DIR = Path(__file__).resolve().parent
SCRATCH_DIR = PACKAGE_DIR.parent
DATA_DIR = SCRATCH_DIR / "data"
ARTIFACTS_DIR = PACKAGE_DIR / "artifacts"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

# Datasets
CLEANED_DATASET_PATH = DATA_DIR / "Energy_Transition_Master_Dataset_cleaned.xlsx"
AUGMENTED_DATASET_PATH = DATA_DIR / "Energy_Transition_Master_Dataset_augmented.xlsx"
MODEL_BUNDLE_PATH = ARTIFACTS_DIR / "electricity_demand_model.joblib"

# Feature definitions for ML model
MODEL_FEATURES = [
    "primary_energy_consumption",    # Total primary energy consumed (TWh)
    "population",                    # Country population
    "gdp",                           # Gross domestic product (USD)
    "gdp_per_capita",                # GDP per person (USD)
    "electricity_access_pct",        # Electrification rate (% of population)
    "urban_pop_growth",              # Annual urban population growth (%)
    "Total_RE_Capacity_MW_current",  # Total installed renewable capacity (MW)
    "Solar_PV_MW_current",           # Solar PV capacity (MW)
    "Onshore_Wind_MW_current",       # Onshore wind capacity (MW)
    "Hydropower_MW_current",         # Hydropower capacity (MW)
    "Bioenergy_MW_current",          # Bioenergy capacity (MW)
    "RE_Generation_Share_pct",       # Renewable share of electricity generation (%)
    "RE_Capacity_Share_pct",         # Renewable share of total capacity (%)
    "Capacity_Generation_Gap_pct",   # Gap between capacity share and actual generation share (%)
    "Solar_Wind_Share_pct",          # Variable RE (solar + wind) share (%)
]

LOG_TRANSFORM_FEATURES = [
    "primary_energy_consumption",
    "population",
    "gdp",
    "gdp_per_capita",
    "Total_RE_Capacity_MW_current",
]

TARGET_COL = "electricity_demand"  # Target in TWh

# Pre-defined Country Groupings / "Bunches"
COUNTRY_GROUPS = {
    "G7": [
        "United States", "Japan", "Germany", "United Kingdom",
        "France", "Italy", "Canada"
    ],
    "BRICS": [
        "Brazil", "Russia", "India", "China", "South Africa"
    ],
    "EU_TOP": [
        "Germany", "France", "Italy", "Spain", "Poland",
        "Netherlands", "Belgium", "Sweden"
    ],
    "LATAM_TOP": [
        "Brazil", "Mexico", "Argentina", "Colombia", "Chile", "Peru"
    ],
    "ASIA_PACIFIC": [
        "China", "India", "Japan", "South Korea", "Australia",
        "Indonesia", "Vietnam", "Thailand", "Malaysia"
    ],
    "AFRICA_TOP": [
        "South Africa", "Egypt", "Nigeria", "Algeria", "Morocco",
        "Kenya", "Ethiopia"
    ],
    "GLOBAL_TOP_10": [
        "China", "United States", "India", "Russia", "Japan",
        "Brazil", "Canada", "South Korea", "Germany", "France"
    ],
}
