---
name: loss-triangle-analysis
description: "Build or analyze loss development triangles. Use when asked to create a loss triangle, calculate link ratios, compute CDFs, project ultimates, estimate IBNR, or produce chain ladder or Bornhuetter-Ferguson analyses. Trigger phrases: loss triangle, chain ladder, IBNR, development factors, link ratios, CDF, BF method, reserve analysis."
---
# Loss Triangle Analysis Skill

## What This Skill Does
Guides Copilot through the standard actuarial workflow for loss triangle analysis — from raw data to IBNR estimates.

## Workflow

### Step 1: Build the Triangle
- Pivot claim or loss data into a matrix: rows = accident year, columns = development period
- Ensure values are **cumulative** (not incremental) unless otherwise specified
- Handle partial years and varying maturities

### Step 2: Calculate Age-to-Age (Link) Ratios
- For each development period transition, compute: `LR(n) = Cumulative[n+1] / Cumulative[n]`
- Use **volume-weighted** average as the default selection
- Also compute simple average and medial (excluding highest/lowest) for comparison
- Display a factor selection table showing all methods

### Step 3: Select Factors and Compute CDFs
- Select link ratios for each transition (volume-weighted unless overridden)
- Apply a **tail factor** (do not assume 1.000 without justification)
- CDF to ultimate = product of selected link ratios from each maturity to ultimate

### Step 4: Project Ultimates and IBNR
- Ultimate = Latest Diagonal Value × CDF to Ultimate
- IBNR = Ultimate − Latest Incurred (or Latest Paid)
- Present results in a summary table by accident year

### Step 5: Visualize
- Stacked bar chart: Paid/Incurred (known) + IBNR (projected)
- Line chart: CDFs by maturity
- Optional: Actual vs Expected analysis

## Output Format
Always produce:
1. The development triangle (formatted table)
2. Link ratio selection table with multiple averaging methods
3. CDF to ultimate table
4. Ultimate and IBNR summary by accident year
5. At least one visualization

## Example Prompt Patterns
- "Build a chain ladder analysis from this triangle data"
- "Calculate IBNR reserves for personal auto"
- "Compare BF and chain ladder results"
