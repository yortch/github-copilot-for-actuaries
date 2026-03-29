---
description: "Use when writing or reviewing reserving code: loss triangles, chain ladder, Bornhuetter-Ferguson, IBNR, case reserves, bulk reserves, development factors, link ratios, tail factors, Schedule P"
---
# Reserving Guidelines

## Terminology
- **Loss Triangle**: Matrix of cumulative losses by accident year (rows) and development period (columns)
- **Link Ratio / Age-to-Age Factor**: Ratio of cumulative losses at dev period n+1 to dev period n
- **CDF (Cumulative Development Factor)**: Product of link ratios from a given maturity to ultimate
- **IBNR**: Incurred But Not Reported -- the difference between projected ultimate and current incurred
- **Tail Factor**: Development beyond the oldest observed maturity (typically selected as 1.00-1.05)

## Methods
- **Chain Ladder**: Ultimate = Latest Diagonal x CDF. Simple, data-driven, can be volatile for immature years.
- **Bornhuetter-Ferguson**: Ultimate = Paid + (Expected Ultimate x % Unreported). Blends chain ladder with a priori expectation. More stable for recent accident years.
- **Cape Cod**: Similar to BF but uses the triangle's own data to derive the expected loss ratio.

## Best Practices
- Always use **volume-weighted** (not simple average) link ratios as the default
- Exclude outlier years from factor selection when justified
- Apply a tail factor -- do not assume 1.000 without justification
- Present chain ladder and BF side-by-side for reserve committees
- Document all selections and exclusions

## Common Pitfalls
- Confusing incremental vs cumulative triangles
- Using arithmetic average link ratios (biases toward small years)
- Forgetting to handle the latest diagonal correctly when years have different maturities
- Negative IBNR is a red flag -- investigate before accepting
