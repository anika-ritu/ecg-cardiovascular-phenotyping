"""ECG fiducial detection and feature extraction."""

from __future__ import annotations

import numpy as np
from scipy.signal import find_peaks


def detect_r_peaks(
    signal: np.ndarray,
    sampling_rate: float,
    min_distance_seconds: float = 0.35,
    prominence: float | None = None,
) -> np.ndarray:
    """Detect R peaks from a filtered ECG signal using scipy peak detection."""

    x = np.asarray(signal, dtype=float)
    distance = max(1, int(min_distance_seconds * sampling_rate))
    kwargs = {"distance": distance}
    if prominence is not None:
        kwargs["prominence"] = prominence
    peaks, _ = find_peaks(x, **kwargs)
    return peaks


def rr_intervals_ms(r_peaks: np.ndarray, sampling_rate: float) -> np.ndarray:
    """Convert R-peak sample positions to RR intervals in milliseconds."""

    peaks = np.asarray(r_peaks, dtype=float)
    return np.diff(peaks) / sampling_rate * 1000.0


def hrv_features(r_peaks: np.ndarray, sampling_rate: float) -> dict[str, float]:
    """Compute time-domain HRV features used in the phenotype analysis."""

    rr = rr_intervals_ms(r_peaks, sampling_rate)
    if len(rr) == 0:
        return {"heart_rate": np.nan, "sdnn": np.nan, "rmssd": np.nan, "pnn50": np.nan}

    diff_rr = np.diff(rr)
    mean_rr = float(np.mean(rr))
    return {
        "heart_rate": 60000.0 / mean_rr if mean_rr else np.nan,
        "sdnn": float(np.std(rr, ddof=1)) if len(rr) > 1 else 0.0,
        "rmssd": float(np.sqrt(np.mean(diff_rr**2))) if len(diff_rr) else 0.0,
        "pnn50": float(np.mean(np.abs(diff_rr) > 50.0) * 100.0) if len(diff_rr) else 0.0,
    }


def amplitude_features(signal: np.ndarray, r_peaks: np.ndarray) -> dict[str, float]:
    """Compute compact ECG amplitude descriptors around detected R peaks."""

    x = np.asarray(signal, dtype=float)
    peaks = np.asarray(r_peaks, dtype=int)
    if len(peaks) == 0:
        return {"mean_r_amplitude": np.nan, "rms_amplitude": np.nan}

    r_values = x[peaks]
    return {
        "mean_r_amplitude": float(np.mean(r_values)),
        "rms_amplitude": float(np.sqrt(np.mean(x**2))),
        "peak_to_peak_amplitude": float(np.ptp(x)),
    }


def extract_ecg_features(signal: np.ndarray, sampling_rate: float) -> dict[str, float]:
    """Extract the core ECG features used by the downstream analysis."""

    peaks = detect_r_peaks(signal, sampling_rate)
    features = {}
    features.update(hrv_features(peaks, sampling_rate))
    features.update(amplitude_features(signal, peaks))
    features["n_r_peaks"] = int(len(peaks))
    return features
