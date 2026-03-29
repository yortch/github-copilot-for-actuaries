# Copilot Workspace Instructions -- P&C Actuarial

## Project Context
This is a Property & Casualty insurance actuarial workspace. All code relates to reserving, ratemaking, catastrophe modeling, and regulatory analysis for a North American insurer.

## Domain Conventions
- Use standard actuarial terminology: "accident year" (not "loss year"), "earned premium" (not "revenue"), "IBNR" (not "unreported claims")
- Loss triangles are cumulative by default unless stated otherwise
- Development factors are age-to-age link ratios; CDFs are cumulative products
- Pure premium = frequency x severity
- Loss ratio = incurred losses / earned premium
- Always distinguish between paid, incurred, and ultimate loss bases

## Code Standards
- Python is the primary language (migrating from Excel/VBA/SAS)
- Use pandas for tabular data, numpy for numerical operations
- Use statsmodels for GLMs, scipy for distributions
- Format dollar amounts with commas and 2 decimals: `f""`
- Format percentages with 1 decimal: `f"{value:.1%}"`
- Use descriptive variable names that match actuarial concepts (e.g., `earned_premium`, `loss_development_factor`, `claim_frequency`)

## Data
- Sample data is in the `data/` folder (synthetic, no real PII)
- Lines of business: Personal Auto, Homeowners
- Policy years: 2015-2024
- States: TX, FL, CA, IL, NY, PA, OH, GA, NC, MI
