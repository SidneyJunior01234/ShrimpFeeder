# src/detection/click_detection_utils.py

from pathlib import Path
import pandas as pd
import numpy as np
import soundfile as sf
from scipy.signal import ShortTimeFFT, windows


from src.data.preprocess import read_audio_segment, get_sample_rate
from src.features.extract_features import (
    compute_spectral_flux,
    compute_hfc,
    # compute_wpd,
    # compute_cd
)

def detect_clicks(file_path: Path, config: dict) -> pd.DataFrame:
    fs = get_sample_rate(file_path)
    if fs is None:
        print(f"Error: Could not read sampling rate for {file_path}")
        return pd.DataFrame()

    # Parameters from config
    short_term_duration = config["processing"]["short_term_duration"]
    mid_term_duration = config["processing"]["mid_term_duration"]
    threshold = config["detection"]["threshold"]
    f_low = config["detection"]["frequency_band"]["low"]
    f_high = config["detection"]["frequency_band"]["high"]

    W = int(short_term_duration * fs)
    nfft = W
    window = windows.hann(W, sym=False)

    # One-sided Frequency Vector
    freqs_onesided = np.linspace(0,fs/2,nfft//2 + 1)
    band_mask = (freqs_onesided >= f_low) & (freqs_onesided <= f_high)

    stft_transform = ShortTimeFFT(mfft=nfft, hop=W, win=window, fft_mode='onesided', fs=fs)

    num_samples_mid = int(mid_term_duration * fs)
    start_sample = 0
    time_sec_list = []

    while True:
        audio_segment = read_audio_segment(file_path, start_sample, num_samples_mid)
        if audio_segment is None or len(audio_segment) < W:
            break

        num_samples = len(audio_segment)
        STFT_oneside = stft_transform.stft(audio_segment, p0=0, p1=num_samples // W, k_offset=0)
        Sxx = np.abs(STFT_oneside)
        Sxx_band = Sxx[band_mask, :]  # Shape: [num_selected_freqs, num_frames]

        # ----- ALGORITMOS -----
        SF = compute_spectral_flux(Sxx_band)
        HFC = compute_hfc(Sxx_band)
        # WPD = compute_wpd(STFT_oneside)
        # CD = compute_cd(STFT_oneside)

        odf = np.log10(SF * HFC + 1)
        click_events = (odf >= threshold)

        time_offset = start_sample / fs
        time_chunk = time_offset + np.arange(len(odf)) * short_term_duration

        time_sec_list.extend(time_chunk[click_events])
        start_sample += num_samples_mid

    return pd.DataFrame({"Event_Time_Seconds": time_sec_list})



def save_detection_results(df: pd.DataFrame, output_file: Path, wav_path: Path):
    """
    Saves detected event timestamps to a CSV file, along with the duration of the original WAV file.

    Args:
        df (pd.DataFrame): DataFrame with click event time stamps.
        output_file (Path): Destination path for CSV output.
        wav_path (Path): Path to the original .wav file (to compute its duration).
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)

    try:
        info = sf.info(wav_path)
        duration_sec = info.frames / info.samplerate
        metadata_file = output_file.with_suffix('.meta')
        with open(metadata_file, 'w') as meta_f:
            meta_f.write(f"Duration_Seconds: {duration_sec:.3f}\n")
    except Exception as e:
        print(f"Warning: Could not extract WAV duration for {wav_path.name}: {e}")
