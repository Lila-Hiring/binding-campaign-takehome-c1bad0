"""Request types for the digital twin (and, in the same shape, for real-lab batch requests)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AssayConditions:
    protein_nm: float = 20.0
    protein_lot: str = "L1"
    tracer_lot: str = "T1"
    tracer_nm: float = 5.0
    detergent: str = "tween20_0.01pct"  # "none", "tween20_0.01pct", or "triton_0.01pct"
    dmso_pct: float = 1.0
    incubation_min: float = 60.0


@dataclass(frozen=True)
class CurveRequest:
    compound_id: str
    top_um: float = 30.0
    dilution: float = 3.0
    n_points: int = 10
    replicates: int = 2
