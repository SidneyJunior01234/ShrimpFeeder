import soundfile as sf
import numpy as np

def get_sample_rate(file_path):
    """
    Retrieve the sample rate from an audio file.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        int: The sample rate of the audio file (samples per second).
    """
    try:
        with sf.SoundFile(file_path) as file_info:
            return file_info.samplerate
    except Exception as e:
        print(f"Error retrieving sample rate from {file_path}: {e}")
        return None


def read_audio_segment(file_path, start_sample, num_samples):
    """
    Reads a specified segment from an audio file based on sample indices.

    Args:
        file_path (str): The path to the audio file.
        start_sample (int): The starting sample index to read from.
        num_samples (int): The number of samples to read.

    Returns:
        numpy.ndarray: The audio samples as a mono signal.
    """
    try:
        with sf.SoundFile(file_path) as file_info:
            # Ensure the start_sample is within bounds
            if start_sample + num_samples > file_info.frames:
                return None

            # Seek to the start sample
            file_info.seek(start_sample)
            # Read the desired number of samples
            data = file_info.read(num_samples, always_2d=True)

        # Extract the first channel if the audio is stereo
        data = data[:, 0]

        return data

    except Exception as e:
        print(f"Error reading segment from {file_path}: {e}")
        return None
