---
description: "Use when writing or reviewing pricing and ratemaking code: GLM, frequency-severity models, pure premium, relativities, rating factors, loss costs, rate indications, rate filings, experience rating, credibility"
---
# Ratemaking & Pricing Guidelines

## Core Concepts
- **Pure Premium** = Frequency x Severity (loss cost per exposure unit)
- **Indicated Rate** = Pure Premium / (1 - Expense Ratio - Profit Target)
- **Relativity**: Multiplicative factor for a rating variable relative to a base level (base = 1.000)
- **On-Level Premium**: Historical premium adjusted to the current rate level
- **Loss Trend**: Annual rate of increase in loss costs, applied to project historical losses forward

## GLM Modeling
- **Frequency**: Poisson distribution with log link, exposure as offset
- **Severity**: Gamma distribution with log link, conditional on a claim occurring
- Use Treatment (reference-level) coding for categorical rating variables
- The base level for each variable should be the largest or most representative class
- Relativities = exp(coefficient) for log-link models
- Always check model diagnostics: deviance residuals, dispersion, AIC/BIC

## Rate Indication Workflow
1. Compile earned premium and incurred losses by accident year
2. Apply **loss development** factors (from reserving analysis)
3. Apply **loss trend** to project to prospective period
4. Apply **on-level factors** to adjust premium to current rate level
5. Calculate **overall indicated rate change** = (actual LR / permissible LR) - 1

## Best Practices
- Use at least 5 years of experience (10 preferred) for credibility
- Weight experience years by earned premium
- Clearly state all selected assumptions: trend rate, expense ratio, profit target
- Compare modeled vs actual frequency and severity by rating variable
