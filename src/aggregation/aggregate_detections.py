# src/aggregation/aggregate_detections.py

from pathlib import Path
import pandas as pd
import numpy as np
from src.config.config_loader import load_config

def aggregate_event_file(events_csv_path: Path, window_size: float, output_csv_path: Path = None):
    """
    Aggregates click events over a defined window and saves to CSV.

    Args:
        events_csv_path (Path): Path to *_events.csv file.
        window_size (float): Time window size for aggregation (in seconds).
        output_csv_path (Path, optional): If not provided, replaces '_events.csv' with '_aggregated.csv'
                                          in the same directory.
    """
    if not events_csv_path.exists():
        print(f"[Warning] File not found: {events_csv_path}")
        return

    df = pd.read_csv(events_csv_path)

    if "Event_Time_Seconds" not in df.columns:
        print(f"[Error] Column 'Event_Time_Seconds' not found in {events_csv_path.name}")
        return

    # Assign each event to a time window
    df["window_index"] = (df["Event_Time_Seconds"] // window_size).astype(int)

    # Count number of events per window
    agg_df = df.groupby("window_index").size().reset_index(name="event_count")
    agg_df["start_time_sec"] = agg_df["window_index"] * window_size

    # Create a complete index of all possible windows from min to max
    min_index = 0 #df["window_index"].min()
    max_index = df["window_index"].max()
    full_index = pd.DataFrame({"window_index": range(min_index, max_index + 1)})
    full_index["start_time_sec"] = full_index["window_index"] * window_size

    # Merge with actual data and fill missing windows with event_count = 0
    agg_df = pd.merge(full_index, agg_df, on=["window_index", "start_time_sec"], how="left")
    agg_df["event_count"] = agg_df["event_count"].fillna(0).astype(int)

    # Order and format
    agg_df = agg_df[["start_time_sec", "event_count"]]

    # Default output path
    if output_csv_path is None:
        output_csv_path = events_csv_path.with_name(events_csv_path.name.replace("_events.csv", "_aggregated.csv"))

    output_csv_path.parent.mkdir(parents=True, exist_ok=True)
    agg_df.to_csv(output_csv_path, index=False)
    print(f"[Info] Aggregated file saved to: {output_csv_path}")
