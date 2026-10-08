"""The modeling team's digital twin of the FP and SPR assays (see TWIN.md for its assumptions)."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

from .conditions import AssayConditions, CurveRequest

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

TRACER_KD_NM = {"T1": 21.0, "T2": 40.0}
REF_PKI = 7.35
MP_HIGH, MP_LOW = 190.0, 35.0
MP_NOISE = 3.0
INTENSITY = 10_000.0
CURVES_PER_PLATE = 16
CONTROLS_PER_PLATE = 16


class Twin:
    """One plausible 'world' consistent with the modeling team's predictions.

    Each Twin draws a latent pKi for every compound from N(pred_pki, pred_sd) once,
    using `world_seed`. Measurements then add assay noise. Different world seeds
    give different, equally plausible worlds under the model.
    """

    def __init__(self, world_seed: int = 0, predictions_path: str | Path | None = None):
        preds = pd.read_csv(predictions_path or DATA_DIR / "model_predictions.csv")
        rng = np.random.default_rng(world_seed)
        latent = rng.normal(preds["pred_pki"].to_numpy(), preds["pred_sd"].to_numpy())
        self.world_seed = world_seed
        self._pki = dict(zip(preds["compound_id"], latent))
        self._pki["REF-1"] = REF_PKI

    @property
    def compound_ids(self) -> list[str]:
        return [c for c in self._pki if c != "REF-1"]

    def _latent(self, compound_id: str) -> float:
        if compound_id not in self._pki:
            raise KeyError(f"unknown compound_id {compound_id!r}")
        return float(self._pki[compound_id])

    def run_fp(self, conditions: AssayConditions, curves: Sequence[CurveRequest], rng: np.random.Generator) -> pd.DataFrame:
        """Simulate dose-response curves. Returns one row per well, including controls and a REF-1 curve per plate."""
        if conditions.tracer_lot not in TRACER_KD_NM:
            raise ValueError(f"unknown tracer lot {conditions.tracer_lot!r}")
        kd_t = TRACER_KD_NM[conditions.tracer_lot]
        rows: list[dict] = []
        curves = list(curves)
        n_plates = max(1, -(-len(curves) // CURVES_PER_PLATE))
        for p in range(n_plates):
            plate_id = f"TWIN-{p + 1:03d}"
            block = curves[p * CURVES_PER_PLATE:(p + 1) * CURVES_PER_PLATE]
            for k in range(CONTROLS_PER_PLATE):
                rows.append(self._control(plate_id, "high_control", MP_HIGH, rng))
                rows.append(self._control(plate_id, "low_control", MP_LOW, rng))
            ref = CurveRequest("REF-1", top_um=block[0].top_um if block else 30.0)
            for req, well_type in [(ref, "reference")] + [(c, "sample") for c in block]:
                ic50_nm = 10 ** (9.0 - self._latent(req.compound_id)) * (1.0 + conditions.tracer_nm / kd_t)
                conc = req.top_um / req.dilution ** np.arange(req.n_points)
                for rep in range(1, req.replicates + 1):
                    inhibition = 1.0 / (1.0 + ic50_nm / (conc * 1000.0))
                    mp = MP_HIGH - (MP_HIGH - MP_LOW) * inhibition + rng.normal(0.0, MP_NOISE, len(conc))
                    ti = INTENSITY * np.exp(rng.normal(0.0, 0.02, len(conc)))
                    for c, m, t in zip(conc, mp, ti):
                        rows.append({
                            "plate_id": plate_id, "well_type": well_type, "compound_id": req.compound_id,
                            "replicate": rep, "conc_um": float(c), "mp": round(float(m), 1), "total_intensity": round(float(t)),
                        })
        return pd.DataFrame(rows)

    def run_spr(self, compound_ids: Iterable[str], rng: np.random.Generator) -> pd.DataFrame:
        rows = []
        for cid in compound_ids:
            pkd = self._latent(cid) + rng.normal(0.0, 0.1)
            kon = 10 ** rng.uniform(5.0, 6.0)
            kd_m = 10 ** (-pkd)
            rows.append({
                "compound_id": cid, "kd_nm": round(kd_m * 1e9, 3), "kon_per_m_s": float(f"{kon:.3g}"),
                "koff_per_s": float(f"{kon * kd_m:.3g}"), "rmax_ratio": round(float(rng.normal(1.0, 0.05)), 2),
                "chi2_rel": 0.02,
            })
        return pd.DataFrame(rows)

    @staticmethod
    def _control(plate_id: str, well_type: str, mp: float, rng: np.random.Generator) -> dict:
        return {
            "plate_id": plate_id, "well_type": well_type, "compound_id": "", "replicate": 0, "conc_um": 0.0,
            "mp": round(float(mp + rng.normal(0.0, MP_NOISE)), 1),
            "total_intensity": round(float(INTENSITY * np.exp(rng.normal(0.0, 0.02)))),
        }
