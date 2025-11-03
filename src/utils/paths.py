from pathlib import Path

# Automatically resolve project root (assuming this file is within src/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

def get_data_dir(subfolder=None):
    base = PROJECT_ROOT / "data"
    return base / subfolder if subfolder else base

def get_wav_path(group, subfolder, filename):
    return get_data_dir("raw") / group / subfolder / filename

def get_metadata_path(filename):
    return get_data_dir("metadata") / filename

def get_processed_path(filename):
    return get_data_dir("processed") / filename
