"""
Electricity Demand Intelligent Agent
Calculates and forecasts country electricity requirements using ML-trained models
and factors from the Energy Transition dataset.
"""

from .config import (
    CLEANED_DATASET_PATH,
    AUGMENTED_DATASET_PATH,
    MODEL_BUNDLE_PATH,
    MODEL_FEATURES,
    COUNTRY_GROUPS,
)
from .data_pipeline import DataLoader
from .model import ElectricityModel
from .agent import ElectricityDemandAgent

__version__ = "1.0.0"
__all__ = [
    "CLEANED_DATASET_PATH",
    "AUGMENTED_DATASET_PATH",
    "MODEL_BUNDLE_PATH",
    "MODEL_FEATURES",
    "COUNTRY_GROUPS",
    "DataLoader",
    "ElectricityModel",
    "ElectricityDemandAgent",
]
