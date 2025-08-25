# plot_setup.py

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from matplotlib import rc

import numpy as np

def configure_plots(context="paper", figure_size=(8, 6), usetex=True):
    """
    Configures the plotting environment for scientific and publication-quality plots.

    Parameters:
        context (str): Seaborn context (e.g., "paper", "talk", "poster", "notebook").
        figure_size (tuple): Size of the figure in inches (width, height).
        usetex (bool): Whether to use LaTeX for rendering text. If LaTeX is not available,
                       the function will fall back to default text rendering.

    Returns:
        dict: Annotation style settings (e.g., fontsize, fontfamily, color) 
              for consistent labeling in visualizations.
    """

    # Seaborn styling with grid
    sns.set_style("whitegrid", {
        'grid.linestyle': '--',
        'grid.color': '0.7',
        'grid.linewidth': 0.5
    })
    sns.set_context(context)

    # Use LaTeX for text rendering if available
    try:
        if usetex:
            rc('text', usetex=True)
    except Exception:
        print("Warning: LaTeX rendering not available. Using default text rendering.")
        rc('text', usetex=False)

    rc('font', family='serif')

    # DPI and figure size
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['figure.figsize'] = figure_size

    # Font sizes
    plt.rcParams['xtick.labelsize'] = 7
    plt.rcParams['ytick.labelsize'] = 7
    plt.rcParams['axes.labelsize'] = 8
    plt.rcParams['axes.titlesize'] = 9

    # Legend
    plt.rcParams["legend.facecolor"] = "white"
    plt.rcParams["legend.edgecolor"] = "black"
    mpl.rcParams['legend.fontsize'] = 6
    mpl.rcParams['legend.framealpha'] = 1

    # Color palette and styling
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=mpl.cm.tab10.colors)
    mpl.rcParams['errorbar.capsize'] = 2
    mpl.rcParams['lines.linewidth'] = 2
    mpl.rcParams['agg.path.chunksize'] = 10000
    mpl.rcParams['savefig.dpi'] = 300

    # Axes styling
    mpl.rcParams['axes.edgecolor'] = 'black'
    mpl.rcParams['axes.linewidth'] = 0.7

    # Annotation styling returned for user customization
    annotation_style = {
        'fontsize': 6,
        'fontfamily': 'serif',
        'color': 'black',
        'backgroundcolor': 'white'
    }

    return annotation_style

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
        vmin = np.percentile(Sxx, 80)
        vmax = np.percentile(Sxx, 99.99)

        # Set the color limits for the colormap using the calculated percentiles
        mesh.set_clim(vmin, vmax)
