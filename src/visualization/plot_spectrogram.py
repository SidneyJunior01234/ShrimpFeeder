# Used to plot spectrograms
import numpy as np

def plot_spectrogram(title, tt, ff, Sxx, cmap, ax,  Scale = True, clim=True):
    """
    Plot a spectrogram on a given axes and optionally add a colorbar.

    Parameters:
    - title (str): Title of the plot.
    - tt (array): Array of time bins for the spectrogram.
    - ff (array): Array of frequency bins for the spectrogram.
    - Sxx (array): Spectrogram of the signal.
    - cmap (str): Colormap for the spectrogram.
    - Scale (bool): If True, scale the spectrogram to decibel.
    - ax (matplotlib.axes.Axes): Axes object where the spectrogram is plotted.

    The color limits for the spectrogram are automatically set based on the 90th to 99th percentiles of the spectrogram values to better highlight relevant features.

    Returns:
    None
    """
    if Scale:
        Sxx = np.log10(Sxx + np.finfo(float).eps)  # Ensure no log(0) issue

    # Store the QuadMesh object returned by pcolormesh
    mesh = ax.pcolormesh(tt, ff/1000, Sxx, cmap=cmap, shading='gouraud')
    ax.set_title(title)
    ax.set_xlabel('Time (sec)')
    ax.set_ylabel('Frequency (kHz)')

    if clim:
        # Calculate 90th and 99th percentiles for color limit scaling
        vmin = np.percentile(Sxx, 90)
        vmax = np.percentile(Sxx, 99.99)

        # Set the color limits for the colormap using the calculated percentiles
        mesh.set_clim(vmin, vmax)