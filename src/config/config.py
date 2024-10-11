import os
from pathlib import Path

CURR_DIR = os.getcwd()

MODELS_DIR = Path(CURR_DIR, "models")
TRAINING_DATA_DIR = Path(CURR_DIR, "training_data")