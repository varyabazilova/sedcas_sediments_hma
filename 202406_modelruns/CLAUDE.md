# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a scientific modeling codebase for glacier-fed catchment sediment transport and debris flow analysis. The repository contains the SedCas (Sediment Cascade) model, which simulates hydrological processes, sediment generation from landslides, and debris flow formation in mountain catchments.

## Core Model Architecture

### Main Model Components
- **`modules.py`**: Core hydrological and sediment transport functions including:
  - Degree-day snow/ice melt models
  - Evapotranspiration calculations (Penman-Monteith, Priestley-Taylor)
  - Multi-reservoir hydrological model
  - Landslide magnitude generation (power-law distributions)
  - Sediment cascade model (hillslope → channel → outlet)

- **`SedCas_glacier_sed.py`**: Main model class that orchestrates the workflow:
  - Loads climate (.met) and parameter (.par) files
  - Runs multi-HRU (Hydrologic Response Unit) hydrology
  - Handles glacier processes (melt only when snow-free)
  - Generates sediment input and runs sediment transport model
  - Outputs results to CSV files

- **`run.py`**: Simple execution script for the model

### Key Model Directories
- **`model_runs_notebooks2/`**: Current working model version
- **`processing_pipeline/`**: Jupyter notebooks for data analysis and visualization
- **`30years/`**: Model output organized by scenario (SL_daily, SL_once, TL)

## Running the Model

### Basic Model Execution
```python
# From model_runs_notebooks2/ directory
python run.py
```

### Required Input Files
- **Climate file**: `.met` format with columns D (date), Pr (precipitation), Ta (temperature), Rsw (solar radiation)
- **Parameter file**: `parameters.par` with model configuration

### Model Output
- **`Hydro.out`**: Hydrological components (discharge, ET, snow, storage)
- **`Sediment.out`**: Sediment transport results including debris flows

## Parameter Configuration

### Key Parameters in `parameters.par`
- **`qdf`**: Critical discharge threshold for debris flows (2.4 mm/h)
- **`smax`**: Maximum sediment concentration for debris flows (0.57)
- **`smax_nodf`**: Maximum concentration for bedload transport (0.4)
- **`minDF`**: Minimum debris flow volume (2000 m³)
- **`sediment_input`**: Fixed landslide volume input (m³)

### HRU Configuration
- **`n_HRU`**: Number of hydrologic response units
- **`HRUs`**: Unit types ['forest', 'bedrock', 'glacier']
- **`shares`**: Area fractions for each HRU
- **`Vwcaps`**: Water storage capacities
- **`ks`**: Residence time parameters

## Debris Flow Physics

### Debris Flow Triggering Conditions
1. Discharge must exceed critical threshold (`qdf`)
2. Sediment concentration > 40% (`smax_nodf`)
3. Event volume > minimum threshold (2000 m³)
4. No snow present
5. Consecutive events are automatically combined

### Transport Regimes
- **Sub-critical flow**: Exponential bedload transport relationship
- **Debris flows**: Linear transport above critical discharge
- **Supply vs transport limited**: Model accounts for channel sediment availability

## Data Analysis Workflow

### Processing Pipeline (numbered notebooks)
1. **TL processing**: Transport-limited sediment calculations
2. **Hydrology analysis**: Water balance components
3. **Volume calculations**: Debris flow frequency-magnitude
4. **Storage analysis**: Monthly sediment storage dynamics
5. **Bubble plots**: Multi-dimensional sediment transport analysis
6. **Visualization**: Combined plots and statistical analysis

### Output Data Structure
- **Location-based**: `langtang_*` and `mustang_*` prefixes
- **Scenario-based**: `landcover1-5` suffixes for different land cover scenarios
- **Threshold-based**: `20percent-60percent` for different sediment input levels
- **Temporal**: `daily` vs `once` sediment input frequencies

## Model Versions and Variants

### Current Active Directories
- **`model_runs_notebooks2/`**: Primary working version
- **`from_jacob_fixed_glacier_jan2025/`**: Latest glacier modeling fixes

### Sediment Input Modes
- **Fixed increase**: Linear sediment input over time
- **Once per year**: Single annual landslide event (day 1)
- **Stochastic**: Power-law distributed landslide magnitudes (currently disabled)

## Important Model Behavior Notes

- Glacier melting only occurs when snow depth = 0
- Hillslope storage currently bypassed (rhc = 0)
- All landslide material goes directly to channel storage
- Water balance verification included in model output
- Model supports multiple stochastic realizations (M parameter)