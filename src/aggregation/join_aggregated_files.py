# src/aggregation/join_aggregated_files.py

from pathlib import Path
import sys
import pandas as pd
import numpy as np

# === Step 1: Detect and register project root ===
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# === Step 2: Imports after sys.path update ===
from src.config.config_loader import load_config
from src.utils.paths import get_metadata_path

def join_aggregated_files(metadata_type: str, window_size: float):
    """
    Join all *_aggregated.csv files for each trial folder within a metadata_type directory.

    Args:
        metadata_type (str): 'model_detections' or 'reference_detections'
        window_size (float): Aggregation window size in seconds.
    """
    base_path = get_metadata_path(metadata_type)
    if not base_path.exists():
        print(f"[Error] Path does not exist: {base_path}")
        return

    # Traverse subfolders (e.g., Freq_Feeding/8x_Rep01)
    for trial_folder in sorted(base_path.glob("*/*")):
        if not trial_folder.is_dir():
            continue

        aggregated_files = sorted(trial_folder.glob("*_aggregated.csv"))
        if not aggregated_files:
            continue

        print(f"\nJoining {len(aggregated_files)} files in {trial_folder.name}...")
        time_offset = 0.0
        joint_data = []

        for file_path in aggregated_files:
            df = pd.read_csv(file_path)
            segment_name = file_path.stem.replace("_aggregated", "")

            # Adjust time
            df["start_time_sec"] += time_offset
            df["segment"] = segment_name

            # Mark last time bin as incomplete for possible interpolation in visualization
            df.loc[df.index[-1], 'event_count'] = np.nan

            joint_data.append(df)

            # Update offset: last start_time + window_size
            last_time = df["start_time_sec"].iloc[-1]
            time_offset = last_time + window_size

        # Concatenate all adjusted DataFrames
        df_joint = pd.concat(joint_data, ignore_index=True)

        # Save to same trial folder
        output_filename = f"{trial_folder.name}_joint.csv"
        output_path = trial_folder / output_filename
        df_joint.to_csv(output_path, index=False)
        print(f"[Info] Saved joint CSV to: {output_path}")

def main():
    import argparse
    config = load_config()
    window_size = config["aggregation"]["window_size"]

    parser = argparse.ArgumentParser(description="Join aggregated detection files.")
    parser.add_argument("metadata_type", choices=["model_detections", "reference_detections"],
                        help="Specify folder under metadata (e.g., model_detections)")
    args = parser.parse_args()

    join_aggregated_files(args.metadata_type, window_size)

if __name__ == "__main__":
    main()
