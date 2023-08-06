import os
import json
from pathlib import Path
from enum import Enum
from pydantic import BaseModel

if os.name == 'nt':
  HOME = "%userprofile%"
else:
  HOME = "$HOME"

PREFERENCES_DIR =  os.path.expandvars(f"{HOME}/.stochastic")
PREFERENCES_PATH = os.path.expandvars(f"{HOME}/.stochastic/preferences.json")


class AppModes:
    LOCAL = "local"
    CLOUD = "cloud"


class Defaults:
    CLOUD_URL_PREFIX = "https://api-dev.stochastic.ai"
    LOCAL_URL_PREFIX = "http://127.0.0.1:3000"
    LOCAL_CONVERSION_URL = "http://localhost:5000"
    LOCAL_FINETUNING_URL = "http://localhost:5050"
    LOCAL_INFERENCE_URL = "http://localhost:9000"
    LOCAL_DEPLOYMENT_URL = "http://localhost:5051"
    LOCAL_BENCHMARK_URL = "http://localhost:5001"


class PreferencesItem(BaseModel):
    cloud_url: str = Defaults.CLOUD_URL_PREFIX
    local_url: str = Defaults.LOCAL_URL_PREFIX
    local_conversion_url: str = Defaults.LOCAL_CONVERSION_URL
    local_finetuning_url: str = Defaults.LOCAL_FINETUNING_URL
    local_inference_url: str = Defaults.LOCAL_INFERENCE_URL
    local_benchmark_url: str = Defaults.LOCAL_BENCHMARK_URL
    local_deployment_url: str = Defaults.LOCAL_DEPLOYMENT_URL
    current_mode: str = AppModes.CLOUD


class Preferences:
    """JSON config file representation in preferences"""

    @staticmethod
    def exists() -> bool:
        if Path(PREFERENCES_PATH).exists():
            return True
        return False

    @staticmethod
    def load() -> PreferencesItem:
        try:
            with open(PREFERENCES_PATH) as f:
                data = json.load(f)
            return PreferencesItem(**data)
        except Exception as e:
            # print("ERROR loading preferences", e)
            return PreferencesItem()

    @staticmethod
    def save(updated_preferences: PreferencesItem) -> None:
        if not Path(PREFERENCES_DIR).exists():
            os.makedirs(PREFERENCES_DIR)

        with open(PREFERENCES_PATH, "w") as f:
            f.write(updated_preferences.json())
