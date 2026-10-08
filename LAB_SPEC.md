# Lab specification

## Target and assay

- **Target.** K-17, a 32 kDa soluble ligand-binding domain expressed in *E. coli*.
- **FP competition assay.** A fluorescein-labeled tracer binds K-17, and test compounds compete with it for the binding site. The plate reader measures parallel and perpendicular emission (excitation 485 nm, emission 535 nm) and reports polarization in mP plus total intensity.
- **Plates.** 384-well, black, low volume, 20 µL final volume, read at room temperature.
- **Controls.**
  - High control: protein + tracer + DMSO, defined as 0% inhibition.
  - Low control: tracer + DMSO with no protein, defined as 100% inhibition.
- **Reference compound.** REF-1, run on every plate. Its Ki is 45 nM, measured by ITC with protein lot L1.
- **Standard layout**, used in every run so far:

| Wells | Contents |
|---|---|
| Column 1 | High controls |
| Column 2 | Low controls |
| Columns 3–12 | Replicate 1 of one compound per row (A–P), highest concentration first |
| Columns 13–22 | Replicate 2 of the same compounds |
| Columns 23–24, rows A–J | REF-1, duplicate 10-point curve |
| Columns 23–24, rows K–P | Additional high and low controls |

## Reagents

| Reagent | Lot | Notes |
|---|---|---|
| K-17 protein | L1 | Used in runs R1 and R3. Enough remains for roughly 20 plates at 20 nM. |
| K-17 protein | L2 | Used in run R2. Used up. |
| Tracer | T1 | Kd 21 nM, from saturation binding with lot L1 (experiment SAT1). |
| Tracer | T2 | Label attached at a different position (vendor change). Vendor-reported Kd about 40 nM; not re-measured in our buffer. |

Assay buffer is 25 mM HEPES pH 7.5, 150 mM NaCl, 1 mM TCEP, plus detergent where noted.

## Protocol history

Full parameters for each run are in `data/assay_runs.csv`.

| Run | Campaign | Version | What changed |
|---|---|---|---|
| R1 | C1 | v1 | Original protocol: 20 nM protein (L1), 5 nM T1, no detergent, 2% DMSO, 30 min incubation, top concentration 50 µM |
| R2 | C2 | v2 | Added 0.01% Tween-20, DMSO down to 1%, incubation 60 min, new protein lot L2 |
| R3 | C3 | v3 | Tracer T2 at 5 nM, protein down to 10 nM (back to L1), incubation 120 min, top concentration 30 µM |

## Next batch: budget and options

- **FP plates.** Up to 4 plates of 384 wells, in any layout. The standard layout fits 16 compound curves plus controls and REF-1 per plate.
- **Reads.** Up to 3 reads per plate, at different times after compound addition.
- **SPR.** Up to 8 compounds. SPR returns Kd, kon, koff, and the Rmax ratio (observed maximum response divided by the theoretical maximum for 1:1 binding).
- **Compounds.** Only `in_stock` compounds in `data/compounds.csv` can be tested in this batch.
- **Make-on-demand order.** You may also place one order of up to 24 compounds for a later batch. Lead times and costs are in `data/compounds.csv`.
- **Adjustable assay conditions:**

| Setting | Options |
|---|---|
| Protein | Lot L1, 2–40 nM |
| Tracer | T1 or T2, 1–10 nM |
| Detergent | None, 0.01% Tween-20, or 0.01% Triton X-100 |
| DMSO | 0.5–2%, the same in every well |
| Read times | 15–240 min after compound addition |
| Dose series | Top concentration, dilution factor, number of points, replicates |

## Liquid handling

- Compounds are stored as 10 mM DMSO stocks; see `data/batches.csv`.
- Dose series are made by serial dilution in DMSO, then transferred acoustically (2.5 nL minimum droplet). DMSO is backfilled so every well has the same DMSO percentage.
- The highest concentration you can reach is the stock concentration times the DMSO fraction. For example, a 10 mM stock at 1% DMSO gives at most 100 µM.
- Transfers the dispenser detects as failed are logged in `data/transfer_log.csv`.

## How results come back

- **FP:** one row per well, in the same format as `data/fp_wells.csv`.
- **SPR:** in the same format as `data/spr_results.csv`.

## Proposal format

Any clear format works. The easiest for us to read is a CSV with these columns, plus a short note on assay conditions and read times:

`plate`, `row`, `compound_id`, `batch_id`, `top_um`, `dilution`, `n_points`, `replicates`
