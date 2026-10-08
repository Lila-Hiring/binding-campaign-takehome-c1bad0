# Digital twin v1: notes from the modeling team

## Affinity model

- **Training data.** Reported FP results from runs R1–R3 with qualifier `=`. Results reported as `>` were excluded. For compounds measured more than once, pIC50 values were averaged. 280 compounds.
- **Target variable.** We treat pIC50 as pKi; the Cheng–Prusoff correction is small under our conditions.
- **Features.** Morgan fingerprints (radius 2, 2048 bits), with counter-ions removed.
- **Model.** An ensemble of 25 ridge regressions, each fit on a bootstrap resample. `pred_pki` is the ensemble mean. `pred_sd` combines the ensemble spread with the residual error.
- **Validation.** On a random 80/20 split of compounds, R² = 0.46 and RMSE = 0.56 pIC50 units.
- **Docking scores.** From docking against a homology model; there is no crystal structure yet. These are reported but not used by the model.

## Assay simulation

| Aspect | How the twin handles it |
|---|---|
| Competition | Cheng–Prusoff: IC50 = Ki × (1 + [tracer] / Kd,tracer), with Kd,tracer = 21 nM for T1 and 40 nM for T2 |
| Curve shape | Hill slope 1; window fixed at 190 mP (high control) and 35 mP (low control); noise 3 mP |
| Total intensity | Constant (10,000 ± 2%) |
| Protein concentration, protein lot, detergent, DMSO, incubation time | No effect |
| REF-1 | pKi 7.35 |
| Plates | One virtual plate per 16 curves, each with 16 high controls, 16 low controls, and a REF-1 curve; well positions are not modeled |
| SPR | Kd = 10^−pKi with 0.1 log units of noise; Rmax ratio about 1.0 |
| Uncertainty | Each `Twin(world_seed)` draws one latent pKi per compound from N(`pred_pki`, `pred_sd`), giving one plausible world. Measurements then add assay noise on top. |

## Usage

```python
import numpy as np
from twin import AssayConditions, CurveRequest, Twin

twin = Twin(world_seed=0)
rng = np.random.default_rng(1)
wells = twin.run_fp(AssayConditions(protein_nm=20, tracer_lot="T1"), [CurveRequest("B-0012", top_um=30)], rng)
spr = twin.run_spr(["B-0012"], rng)
```

`run_fp` returns one row per well, with columns `plate_id`, `well_type`, `compound_id`, `replicate`, `conc_um`, `mp`, and `total_intensity`. `twin.fitting.fit_4pl` is the same fit used for the reported results.
