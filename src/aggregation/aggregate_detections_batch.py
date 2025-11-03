# src/aggregation/aggregate_detections_batch.py

import sys
import argparse
from pathlib import Path
import pandas as pd

# === Step 1: Detect project root and add to sys.path ===
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# === Step 2: Project imports ===
from src.config.config_loader import load_config
from src.aggregation.aggregate_detections import aggregate_event_file

# === Step 3: CLI argument parser ===
def parse_args():
    parser = argparse.ArgumentParser(description="Aggregate shrimp click detections by time window.")
    parser.add_argument(
        "source_folder",
        type=str,
        choices=["model_detections", "reference_detections"],
        help="Name of the folder under data/metadata/ containing *_events.csv files to aggregate."
    )
    return parser.parse_args()

# === Step 4: Main logic ===
def main():
    args = parse_args()
    config = load_config()
    window_size = config["aggregation"]["window_size"]

    # Resolve input directory based on user argument
    base_dir = PROJECT_ROOT / "data" / "metadata" / args.source_folder
    event_files = list(base_dir.rglob("*_events.csv"))

    if not event_files:
        print(f"No *_events.csv files found in {base_dir}.")
        return

    print(f"Found {len(event_files)} event files in {args.source_folder}...\n")

    for file_path in event_files:
        print(f"Aggregating {file_path.name}")
        # aggregated_df = aggregate_event_file(file_path, window_size)
        aggregate_event_file(file_path, window_size)

        # Save output with _aggregated suffix
        output_path = file_path.with_name(file_path.stem.replace("_events", "_aggregated") + ".csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # aggregated_df.to_csv(output_path, index=False)
        print(f"Saved to: {output_path}\n")


if __name__ == "__main__":
    main()
