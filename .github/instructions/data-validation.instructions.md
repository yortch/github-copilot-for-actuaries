---
description: "Use when writing or reviewing data validation, data quality checks, regulatory filings, NAIC filings, Schedule P, actuarial standard of practice, ASOP, audit, SOX compliance, model validation"
---
# Data Validation & Regulatory Guidelines

## Data Quality Rules
- Cumulative loss triangles must be monotonically non-decreasing across development periods
- Paid losses must not exceed incurred losses for any individual claim
- Premium must be positive and within reasonable bounds for the line of business
- Loss ratios above 200% or below 10% should be flagged for investigation
- All policy records must have a valid state, LOB, and accident year

## Regulatory Context (North America P&C)
- **NAIC Annual Statement**: Schedule P contains 10-year loss development triangles by LOB
- **State Rate Filings**: Must include experience summary, trend selections, and indicated rate change
- **Actuarial Standard of Practice (ASOP)**:
  - ASOP #23: Data Quality
  - ASOP #25: Credibility Procedures
  - ASOP #36: Statements of Actuarial Opinion on P&C Loss Reserves
  - ASOP #43: Property/Casualty Unpaid Claim Estimates

## Testing Standards
- Every actuarial calculation function should have unit tests
- Test edge cases: zero exposure, zero claims, single accident year
- Validate that factor lookups handle unknown values with defaults
- Premium calculations should enforce minimum and maximum bounds
- Triangle operations should handle missing values (NaN) gracefully

## Audit Trail
- All parameter selections (trend factors, LDFs, tail factors) should be documented
- Code should be version-controlled -- this replaces the "save a copy" Excel workflow
- Functions should be pure (same inputs = same outputs) for reproducibility
