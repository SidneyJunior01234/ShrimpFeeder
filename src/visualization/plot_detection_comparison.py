# src/visualization/plot_detection_comparison.py

#Matplotlib não tentar inicializar uma interface gráfica
import matplotlib as mpl
mpl.use('Agg')

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
from scipy.signal import filtfilt

def impute_missing_values(df, cols_to_impute, order=2):
    """
    Fill missing values in selected columns using polynomial interpolation.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing time series data.
    cols_to_impute : list
        List of column names to apply interpolation.
    order : int, optional
        Order of polynomial interpolation (default is 2).
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with missing values filled.
    """
    df_imputed = df.copy()  # Avoid modifying original data
    
    for col in cols_to_impute:
        # Apply polynomial interpolation for NaNs
        df_imputed[col] = df_imputed[col].interpolate(method='polynomial', order=order, limit_direction='both')

        # Fallback for any remaining NaNs (start/end edges)
        df_imputed[col] = df_imputed[col].bfill().ffill()


    return df_imputed

def apply_filtfilt_smoothing(df, cols_to_smooth, window_size=5):
    """
    Apply a zero-phase moving average filter using filtfilt from SciPy.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing time series data.
    cols_to_smooth : list
        List of column names to apply smoothing.
    window_size : int
        The size of the moving average window (default is 5).
    
    Returns:
    --------
    pd.DataFrame
        A DataFrame with smoothed numerical columns.
    """
    df_smoothed = df.copy()  # Avoid modifying original data
    
    # Define the moving average filter kernel (h)
    h = np.ones(window_size) / window_size

    # Apply filtfilt smoothing to each column
    for col in cols_to_smooth:
        df_smoothed[col] = filtfilt(h, 1, df[col], padlen=0)  # padlen=0 avoids edge artifacts

    return df_smoothed

if __name__ == '__main__':
    # === Step 1: Detect and register project root ===
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    print(f"[Debug] Project root: {PROJECT_ROOT}")
    # === Step 2: Define paths ===
    # REFERENCE_DIR = PROJECT_ROOT / "data" / "metadata" / "reference_detections"
    REFERENCE_DIR = PROJECT_ROOT / "data" / "reference_detections"
    MODEL_DIR = PROJECT_ROOT / "data" / "metadata" / "model_detections"
    FIGURE_DIR = PROJECT_ROOT / "data" / "figures" / "comparison"
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[Debug] Figures will be saved to: {FIGURE_DIR}")

    # === Step 3: Find joint CSV files in both reference and model folders ===
    reference_files = list(REFERENCE_DIR.rglob("*_joint.csv"))
    model_files = list(MODEL_DIR.rglob("*_joint.csv"))

    # Create a mapping from stem to path for matching
    reference_map = {f.stem: f for f in reference_files}
    model_map = {f.stem: f for f in model_files}

    print(f"[Debug] Found {len(reference_files)} reference files and {len(model_files)} model files.")

    # === Step 4: Match and plot ===
    for stem, ref_path in reference_map.items():
        if stem in model_map:
            model_path = model_map[stem]
            print(f"[Info] Plotting comparison for: {stem}")

            # Load CSV files
            df_ref = pd.read_csv(ref_path)
            df_model = pd.read_csv(model_path)

            t_ref = df_ref["start_time_sec"]/3600
            t_model = df_model["start_time_sec"]/3600

            y_ref = df_ref["event_count"].values
            y_model = df_model["event_count"].values

            # Define the columns to smooth (excluding 'created_date' and 'id')
            cols_to_smooth = ['event_count']

            # Select columns to impute (numerical only)
            cols_to_impute = ['event_count']

            # Apply polynomial interpolation (order=2)
            df_ref = impute_missing_values(df_ref, cols_to_impute, order=2)
            df_model = impute_missing_values(df_model, cols_to_impute, order=2)

            # Apply smoothing with filtfilt
            df_ref = apply_filtfilt_smoothing(df_ref, cols_to_smooth, window_size=5)
            df_model = apply_filtfilt_smoothing(df_model, cols_to_smooth, window_size=5)

            y_ref = df_ref["event_count"].values
            y_model = df_model["event_count"].values

            # Create 1x2 subplot
            fig, axs = plt.subplots(1, 2, figsize=(10, 4))#, sharey=True, sharex=True)
            
            axs[0].plot(t_ref, y_ref, label="Reference", color="black")
            axs[0].set_title("Reference Detections")
            axs[0].set_xlabel("Time (h)")
            axs[0].set_ylabel("Event Count")

            axs[1].plot(t_model, y_model, label="Model", color="tab:blue")
            axs[1].set_title("Model Detections")
            axs[1].set_xlabel("Time (h)")

            for ax in axs:
                ax.grid(True)

            fig.suptitle(f"Click Activity Comparison: {stem}")
            fig.tight_layout()

            # Save figure
            fig_path = FIGURE_DIR / f"{stem}_comparison.png"
            fig.savefig(fig_path, dpi=300)
            plt.close(fig)
        else:
            print(f"[Warning] No matching model file found for: {stem}")
