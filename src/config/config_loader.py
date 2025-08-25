# config_loader.py

import yaml
from pathlib import Path

from src.config.project_paths import get_project_root

PROJECT_ROOT = get_project_root()
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"


# Fallback configuration used if the YAML file is missing or invalid
DEFAULT_CONFIG = {
    "audio": {
        "default_fs": 44100  # For common audio applications; overridden per file in practice
    },
    "processing": {
        "short_term_duration": 0.005,  # seconds
        "mid_term_duration": 1.0       # seconds
    },
    "detection": {
        "threshold": 0.005,
        "frequency_band": {
            "low": 5000,
            "high": 22050
        }
    },
    "aggregation": {
        "window_size": 1.0  # seconds
    }
}

def load_config(config_path: Path = CONFIG_PATH) -> dict:
    """
    Load project configuration from a YAML file.
    Falls back to DEFAULT_CONFIG if the file is missing, empty, or malformed.

    Args:
        config_path (Path): Path to YAML configuration file.

    Returns:
        dict: Loaded configuration.
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            if config is None:
                print(f"[ConfigLoader] Warning: {config_path} is empty. Using default configuration.")
                return DEFAULT_CONFIG
            return config
    except FileNotFoundError:
        print(f"[ConfigLoader] Warning: {config_path} not found. Using default configuration.")
        return DEFAULT_CONFIG
    except yaml.YAMLError as e:
        print(f"[ConfigLoader] Error parsing {config_path}: {e}. Using default configuration.")
        return DEFAULT_CONFIG

# Example usage
if __name__ == "__main__":
    config = load_config()
    print(config)
