"""Load the data, run the twin on a few compounds, and fit curves the way the team does."""

import numpy as np
import pandas as pd

from twin import AssayConditions, CurveRequest, Twin, fit_4pl, percent_inhibition

compounds = pd.read_csv("data/compounds.csv")
print(f"{len(compounds)} compounds in the library; {(compounds.availability == 'in_stock').sum()} in stock")

twin = Twin(world_seed=0)
rng = np.random.default_rng(0)
picks = compounds[compounds.availability == "in_stock"].compound_id.head(3).tolist()
wells = twin.run_fp(AssayConditions(), [CurveRequest(c) for c in picks], rng)

hi = wells.loc[wells.well_type == "high_control", "mp"].median()
lo = wells.loc[wells.well_type == "low_control", "mp"].median()
for cid, g in wells[wells.well_type.isin(["sample", "reference"])].groupby("compound_id"):
    fit = fit_4pl(g.conc_um.to_numpy(), percent_inhibition(g.mp.to_numpy(), hi, lo))
    print(f"{cid}: IC50 {fit['qualifier']} {fit['ic50_um']:.3g} uM, Hill {fit['hill']:.2f}")

print(twin.run_spr(picks, rng))
