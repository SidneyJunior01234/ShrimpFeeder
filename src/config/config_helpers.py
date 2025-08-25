# config_helpers.py
from typing import Tuple, Dict

def get_band_limits(config: dict) -> Tuple[float, float]:
    """
    Retrieve low and high frequency band limits for ODFs.

    Args:
        config (dict): Loaded configuration dictionary.

    Returns:
        Tuple[float, float]: (low_freq, high_freq) in Hz
    """
    band = config.get("detection", {}).get("frequency_band", {})
    return band.get("low", 5000), band.get("high", 22050)

def get_dsp_params(config: dict) -> Dict[str, float]:
    """
    Retrieve DSP-related parameters: short/mid durations and threshold.

    Args:
        config (dict): Loaded configuration dictionary.

    Returns:
        Dict[str, float]: Dictionary with keys 'short_term', 'mid_term', and 'threshold'
    """
    processing = config.get("processing", {})
    detection = config.get("detection", {})

    return {
        "short_term": processing.get("short_term_duration", 0.005),
        "mid_term": processing.get("mid_term_duration", 1.0),
        "threshold": detection.get("threshold", 0.005)
    }

def get_aggregation_window(config: dict) -> float:
    """
    Get the aggregation window size in seconds.

    Args:
        config (dict): Loaded configuration dictionary.

    Returns:
        float: Aggregation window size.
    """
    return config.get("aggregation", {}).get("window_size", 1.0)

def get_default_fs(config: dict) -> int:
    """
    Get the default sampling frequency.

    Note: Actual fs should usually be read from file metadata (e.g., with soundfile.info).

    Args:
        config (dict): Loaded configuration dictionary.

    Returns:
        int: Sampling rate in Hz.
    """
    return config.get("audio", {}).get("default_fs", 44100)
