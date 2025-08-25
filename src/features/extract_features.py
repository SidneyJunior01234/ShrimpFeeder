import numpy as np

def _sigm(x):
    """ sigmoid function. """
    k = np.exp(-x)
    return 1 / (1 + k)

def _tanh(x):
    """ Hyperbolic tangent function. """
    return np.tanh(x)


def compute_cd(X, method="phase_init"):
    """
    Compute Complex Domain (CD) Onset Detection function from the one-sided STFT.
    """
    phi = np.angle(X)
    phi_prime = np.zeros_like(phi)
    phi_prime[:, 1:] = phi[:, 1:] - phi[:, :-1]
    phi_prime = np.mod(phi_prime + np.pi, 2 * np.pi) - np.pi

    if method == "phase_init":
        phi_prime[:, 0] = phi_prime[:, 1]

    phi_sum = np.zeros_like(phi)
    phi_sum[:, 1:] = phi_prime[:, 1:] + phi_prime[:, :-1]

    if method == "phase_init":
        phi_sum[:, 0] = phi_prime[:, 0]

    X_T = np.abs(X) * np.exp(1j * phi_sum)
    CD = np.sum(_tanh(np.abs(X - X_T)), axis=0)

    return np.log10(CD + 1)


def compute_wpd(X, method="phase_init"):
    """
    Compute Weighted Phase Deviation (WPD) from the one-sided STFT.
    """
    phi = np.angle(X)
    phi_prime = np.zeros_like(phi)
    phi_prime[:, 1:] = phi[:, 1:] - phi[:, :-1]
    phi_prime = np.mod(phi_prime + np.pi, 2 * np.pi) - np.pi

    phi_2prime = np.zeros_like(phi)
    if method == "phase_init":
        phi_prime[:, 0] = phi_prime[:, 1]
        phi_2prime[:, 1:] = phi_prime[:, 1:] - phi_prime[:, :-1]
        phi_2prime[:, 0] = phi_2prime[:, 1]

    WPD = (2 / X.shape[0]) * np.sum(_sigm(np.abs(X * phi_2prime)), axis=0)

    return np.log2(WPD + 1)


def compute_spectral_flux(X):#, freqs, f_low, f_high):
    """
    Compute Spectral Flux (SF) for a selected frequency band.
    """
    # freq_indices = np.where((freqs >= f_low) & (freqs <= f_high))[0]
    # X = _sigm(X)

    delta_X = np.zeros_like(X)
    delta_X[:, 1:] = np.abs(X[:, 1:]) - np.abs(X[:, :-1])
    delta_X[:, 0] = delta_X[:, 1]

    H = (delta_X + np.abs(delta_X)) / 2
    SF = np.sum(H, axis=0)

    return np.log10(SF + 1)

def compute_hfc(X):#, freqs, f_low, f_hig):
    """
    Compute High-Frequency Content (HFC) and its difference (ΔHFC) for a selected frequency band.
    """
    # freq_indices = np.where((freqs >= f_low) & (freqs <= f_hig))[0]
    # X = _sigm(X)
    magnitude = np.abs(X)

    HFC = np.sum(magnitude, axis=0)

    delta_HFC = np.zeros_like(HFC)
    delta_HFC[1:] = HFC[1:] - HFC[:-1]
    delta_HFC[0] = delta_HFC[1]

    delta_HFC = (delta_HFC + np.abs(delta_HFC)) / 2

    return np.log10(delta_HFC + 1)

# Define the public API
__all__ = ["compute_cd", "compute_wpd", "compute_spectral_flux", "compute_hfc"]
