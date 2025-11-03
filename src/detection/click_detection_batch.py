# src/detection/click_detection_batch.py

import sys
from pathlib import Path
import argparse
import os

# === Step 1: Dynamically detect project root ===
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# === Step 2: Add project root to sys.path if not already present ===
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pathlib import Path
from src.config.config_loader import load_config
from src.detection.click_detection_utils import detect_clicks, save_detection_results
import soundfile as sf

def parse_args():
    """Parses command-line arguments for the click detection script."""
    parser = argparse.ArgumentParser(description="Process a batch of WAV files for a given experiment.")
    parser.add_argument(
        "source_path",
        type=str,
        help="Path to the experiment folder containing subdirectories with the .wav audio files."
    )
    return parser.parse_args()


def process_all_wav_files(experiment_path: Path, output_root: Path):
    """
    Process all WAV files under the given experiment folder and save click detection results.

    Args:
        experiment_path (Path): Full path to the experiment folder.
        output_root (Path): Root directory to save detection results (e.g., data/metadata/model_detections).
    """
    config = load_config()

    if not experiment_path.exists():
        print(f"Experiment folder not found: {experiment_path}")
        return

    # O nome do experimento é o nome da pasta
    experiment_name = experiment_path.name

    for trial_folder in experiment_path.iterdir():
        if not trial_folder.is_dir():
            continue

        for wav_file in trial_folder.glob("*.WAV"):
            print(f"🔍 Processing: {wav_file.name}")

            # Run detection
            df_events = detect_clicks(wav_file, config)

            # Build output path
            relative_subfolder = Path(experiment_name) / trial_folder.name
            output_filename = wav_file.stem + "_events.csv"
            output_path = output_root / relative_subfolder / output_filename

            # Save detection CSV
            save_detection_results(df_events, output_path, wav_path=wav_file)
            print(f"\n✅ Detection complete for: {trial_folder / wav_file}")

    print(f"\n✅ Detection complete. Results saved to: {output_root / experiment_name}")


if __name__ == "__main__":
    args = parse_args()
    
    # Define paths relative to project structure
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    
    # Converte o argumento de string para um objeto Path
    experiment_path_from_arg = Path(args.source_path)

    # Define o caminho de saída
    output_root = PROJECT_ROOT / "data" / "metadata" / "model_detections"
    
    # Inicia a detecção em lote
    process_all_wav_files(experiment_path_from_arg, output_root)
