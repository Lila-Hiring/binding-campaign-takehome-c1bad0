"""The team's standard dose-response fit (used to produce data/fp_results_reported.csv).

Four-parameter logistic on percent inhibition, all points included, one fit per
compound per plate. Kept here so you can see exactly how the reported numbers
were made.
"""

from __future__ import annotations

import warnings

import numpy as np
from scipy.optimize import curve_fit


def four_pl(x: np.ndarray, bottom: float, top: float, ic50: float, hill: float) -> np.ndarray:
    return bottom + (top - bottom) / (1.0 + (ic50 / x) ** hill)


def percent_inhibition(mp: np.ndarray, high_control_mp: float, low_control_mp: float) -> np.ndarray:
    """0% = high control (protein + tracer), 100% = low control (tracer only)."""
    return 100.0 * (high_control_mp - np.asarray(mp, float)) / (high_control_mp - low_control_mp)


def fit_4pl(conc_um: np.ndarray, pct_inhibition: np.ndarray, top_conc_um: float | None = None) -> dict:
    """Fit a 4PL curve. Returns ic50_um, qualifier ('=' or '>'), hill, top, bottom, r2."""
    x = np.asarray(conc_um, float)
    y = np.asarray(pct_inhibition, float)
    keep = np.isfinite(x) & np.isfinite(y) & (x > 0)
    x, y = x[keep], y[keep]
    top_conc = float(top_conc_um if top_conc_um is not None else x.max())
    p0 = [min(y.min(), 0.0), max(y.max(), 50.0), float(np.median(x)), 1.0]
    bounds = ([-50.0, 20.0, 1e-5, 0.3], [60.0, 150.0, 1e4, 5.0])
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            popt, _ = curve_fit(four_pl, x, y, p0=p0, bounds=bounds, maxfev=20000)
    except (RuntimeError, ValueError):
        return {"ic50_um": top_conc, "qualifier": ">", "hill": np.nan, "top": np.nan, "bottom": np.nan, "r2": np.nan}
    bottom, top, ic50, hill = popt
    pred = four_pl(x, *popt)
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2)) or 1.0
    r2 = 1.0 - ss_res / ss_tot
    if ic50 > top_conc or y.max() < 50.0:
        return {"ic50_um": top_conc, "qualifier": ">", "hill": float(hill), "top": float(top), "bottom": float(bottom), "r2": r2}
    return {"ic50_um": float(ic50), "qualifier": "=", "hill": float(hill), "top": float(top), "bottom": float(bottom), "r2": r2}
