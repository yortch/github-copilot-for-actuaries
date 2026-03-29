---
description: "Use when writing or reviewing catastrophe modeling code: CAT models, Monte Carlo simulation, exceedance probability, OEP, AEP, return period, VaR, TVaR, reinsurance, probable maximum loss, PML"
---
# Catastrophe Modeling Guidelines

## Key Concepts
- **OEP (Occurrence Exceedance Probability)**: Probability that the single largest event in a year exceeds a given loss level
- **AEP (Aggregate Exceedance Probability)**: Probability that the total of all events in a year exceeds a given loss level
- **Return Period**: Inverse of exceedance probability (e.g., 1-in-100 = 1% annual probability)
- **VaR (Value at Risk)**: Loss at a given percentile (e.g., 99th percentile = 1-in-100 VaR)
- **TVaR (Tail Value at Risk)**: Average of all losses exceeding VaR -- captures tail severity

## Simulation Approach
- Use Monte Carlo with at least 100,000 simulated years for stable tail estimates
- Frequency: Poisson or Negative Binomial for event count per year
- Severity: Lognormal, Pareto, or vendor-specific distributions for event loss
- Always set a seed for reproducibility: 

## Reinsurance Context
- Key return periods for decision-making: 1-in-100, 1-in-250, 1-in-500
- OEP drives per-occurrence excess-of-loss (XOL) reinsurance pricing
- AEP drives aggregate stop-loss reinsurance pricing
- Rating agencies (AM Best, S&P) focus on 1-in-100 and 1-in-250 OEP/AEP

## Best Practices
- Validate simulation against historical experience as a reasonableness check
- Report both VaR and TVaR -- VaR alone misses tail concentration
- Clearly document distributional assumptions and parameter sources
- Use log-scale for exceedance probability plots
