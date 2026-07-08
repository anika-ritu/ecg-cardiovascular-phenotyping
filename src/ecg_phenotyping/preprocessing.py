"""ECG preprocessing utilities.

The functions here mirror the preprocessing used in the cleaned thesis notebook:
bandpass filtering for ECG morphology preservation, optional 50 Hz notch
filtering, and simple signal-quality summaries.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.signal import butter, filtfilt, iirnotch, welch


@dataclass(frozen=True)
class ECGPreprocessConfig:
    """Configuration for ECG filtering."""

    sampling_rate: float
    lowcut: float = 0.5
    highcut: float = 40.0
    notch_freq: float = 50.0
    notch_quality: float = 30.0
    filter_order: int = 4


def bandpass_filter(
    signal: np.ndarray,
    sampling_rate: float,
    lowcut: float = 0.5,
    highcut: float = 40.0,
    order: int = 4,
) -> np.ndarray:
    """Apply a zero-phase Butterworth bandpass filter to a 1-D ECG signal."""

    nyquist = 0.5 * sampling_rate
    b, a = butter(order, [lowcut / nyquist, highcut / nyquist], btype="band")
    return filtfilt(b, a, np.asarray(signal, dtype=float))


def notch_filter(
    signal: np.ndarray,
    sampling_rate: float,
    notch_freq: float = 50.0,
    quality: float = 30.0,
) -> np.ndarray:
    """Apply a zero-phase notch filter for power-line interference."""

    b, a = iirnotch(w0=notch_freq / (sampling_rate / 2), Q=quality)
    return filtfilt(b, a, np.asarray(signal, dtype=float))


def preprocess_ecg(signal: np.ndarray, config: ECGPreprocessConfig) -> np.ndarray:
    """Run bandpass filtering followed by notch filtering."""

    filtered = bandpass_filter(
        signal,
        sampling_rate=config.sampling_rate,
        lowcut=config.lowcut,
        highcut=config.highcut,
        order=config.filter_order,
    )
    return notch_filter(
        filtered,
        sampling_rate=config.sampling_rate,
        notch_freq=config.notch_freq,
        quality=config.notch_quality,
    )


def signal_quality_summary(signal: np.ndarray, sampling_rate: float) -> dict[str, float]:
    """Compute compact signal-quality descriptors for an ECG segment."""

    x = np.asarray(signal, dtype=float)
    freqs, power = welch(x, fs=sampling_rate, nperseg=min(len(x), 1024))
    total_power = float(np.trapz(power, freqs))
    qrs_band = (freqs >= 5.0) & (freqs <= 20.0)
    qrs_power = float(np.trapz(power[qrs_band], freqs[qrs_band])) if qrs_band.any() else 0.0

    return {
        "mean": float(np.mean(x)),
        "std": float(np.std(x, ddof=1)) if len(x) > 1 else 0.0,
        "rms": float(np.sqrt(np.mean(x**2))),
        "peak_to_peak": float(np.ptp(x)),
        "qrs_band_power_ratio": qrs_power / total_power if total_power else 0.0,
    }
