import subprocess
import sys

def run_pipeline():
    print("[1/4] Detecting clicks in raw WAV files...")
    subprocess.run([sys.executable, "src/detection/click_detection_batch.py"], check=True)

    print("[2/4] Aggregating detections for reference and model...")
    subprocess.run([sys.executable, "src/aggregation/aggregate_detections_batch.py", "reference_detections"], check=True)
    subprocess.run([sys.executable, "src/aggregation/aggregate_detections_batch.py", "model_detections"], check=True)

    print("[3/4] Concatenating aggregated results with time continuity...")
    subprocess.run([sys.executable, "src/aggregation/join_aggregated_files.py", "reference_detections"], check=True)
    subprocess.run([sys.executable, "src/aggregation/join_aggregated_files.py", "model_detections"], check=True)

    print("[4/4] Generating comparison plots...")
    subprocess.run([sys.executable, "src/visualization/plot_detection_comparison.py"], check=True)

if __name__ == "__main__":
    run_pipeline()
