# Data files

All files are in `data/`. Concentrations are in µM unless a column name says otherwise.

## compounds.csv

The full library: tested compounds plus purchasable or synthesizable analogs.

| Column | Meaning |
|---|---|
| `compound_id` | Registry ID |
| `smiles` | Structure as registered |
| `availability` | `in_stock` or `make_on_demand` |
| `lead_time_days` | Days until a make-on-demand compound arrives (0 if in stock) |
| `cost_usd` | Synthesis cost for make-on-demand compounds (0 if in stock) |

## batches.csv

Physical batches of in-stock compounds.

| Column | Meaning |
|---|---|
| `batch_id` | Batch ID; a compound can have more than one batch |
| `compound_id` | Registry ID |
| `purity_pct` | LC-MS purity at registration |
| `registered_date` | Date the batch was registered |
| `stock_conc_mm` | Nominal DMSO stock concentration (mM) |

## assay_runs.csv

One row per FP run, with all protocol parameters: `run_id`, `campaign`, `assay_version`, `start_date`, `protein_lot`, `protein_nm_nominal`, `tracer_lot`, `tracer_nm`, `detergent`, `dmso_pct`, `incubation_min`, `top_conc_um`, `dilution`, `n_points`, `replicates`, and `notes`.

## plates.csv

`plate_id`, `run_id`, and `read_datetime` for each FP plate.

## fp_wells.csv

Raw FP data, one row per well.

| Column | Meaning |
|---|---|
| `plate_id`, `well`, `row`, `col` | Plate and position (rows A–P, columns 1–24) |
| `well_type` | `sample`, `reference` (REF-1), `high_control`, or `low_control` |
| `compound_id`, `batch_id` | Empty for controls |
| `replicate` | 1 or 2 for curves; 0 for controls |
| `conc_um` | Nominal compound concentration |
| `mp` | Fluorescence polarization (mP) |
| `total_intensity` | Total fluorescence intensity (parallel + 2 × perpendicular), in arbitrary units |

## fp_results_reported.csv

The team's reported results: one four-parameter logistic fit per compound per plate, made with `twin/fitting.py`. Percent inhibition is normalized to the median high and low controls of that plate.

| Column | Meaning |
|---|---|
| `plate_id`, `run_id`, `compound_id`, `batch_id` | Identifiers |
| `ic50_um`, `qualifier` | `=` for a fitted IC50; `>` means the IC50 was above the top concentration or the fit failed, and `ic50_um` is then the top concentration |
| `pic50` | −log10(IC50 in M) |
| `hill`, `top`, `bottom` | Fitted 4PL parameters (fit bounds: Hill 0.3–5, top 20–150, bottom −50–60) |
| `r2` | Fit R² |

## transfer_log.csv

Acoustic transfers the dispenser flagged as failed: `plate_id`, `well`, `status`, and `detail`.

## spr_results.csv

SPR measurements from June 2026: `compound_id`, `batch_id`, `run_date`, `kd_nm`, `kon_per_m_s`, `koff_per_s`, `rmax_ratio` (observed maximum response divided by the theoretical 1:1 maximum), and `chi2_rel` (fit residual relative to Rmax).

## tracer_saturation.csv

Protein titrations into a fixed tracer concentration, used to determine tracer Kd: `experiment_id`, `tracer_lot`, `protein_lot`, `tracer_nm`, `protein_nm_nominal`, `replicate`, `mp`, and `total_intensity`. Buffer contains 0.01% Tween-20 and 1% DMSO, read at 60 min.

## model_predictions.csv

The modeling team's predictions for every library compound (see [TWIN.md](TWIN.md)): `compound_id`, `pred_pki`, `pred_sd`, and `docking_score_kcal` (more negative means a better docking score).
