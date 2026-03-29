---
name: rate-indication
description: "Perform an actuarial rate indication analysis. Use when asked to calculate indicated rate changes, compile experience data, apply loss development and trending, on-level premiums, or prepare rate filing exhibits. Trigger phrases: rate indication, indicated rate change, experience study, loss trend, on-level premium, rate filing, permissible loss ratio, expense ratio."
---
# Rate Indication Skill

## What This Skill Does
Guides Copilot through a full ratemaking workflow — from experience compilation to indicated rate change.

## Workflow

### Step 1: Compile Experience
- Aggregate earned premium and incurred losses by accident year
- Calculate reported loss ratios, claim frequency, and average severity
- Filter by line of business and state as needed

### Step 2: Apply Loss Development
- Use development factors from the reserving analysis (or the loss-triangle-analysis skill)
- Multiply reported incurred losses by the CDF to ultimate
- Result: **Developed Ultimate Losses** by accident year

### Step 3: Apply Loss Trend
- Select an annual loss trend rate (typically 2%–6% for P&C)
- Trend period = prospective midpoint − historical midpoint
- Trend factor = (1 + annual trend) ^ trend period
- Result: **Trended Ultimate Losses**

### Step 4: On-Level Premium
- Adjust historical premium to the current rate level
- On-level factor = Current Rate Level Index / Historical Rate Level Index
- Result: **On-Level Earned Premium**

### Step 5: Calculate Indicated Rate Change
```
Overall Trended Loss Ratio = Total Trended Ultimate / Total On-Level Premium
Permissible Loss Ratio = 1 - Expense Ratio - Profit Target  
Indicated Rate Change = (Trended LR / Permissible LR) - 1
```

### Step 6: Visualize
- Bar chart: On-level premium vs trended ultimate by accident year
- Line chart: Reported vs trended loss ratios over time
- Summary panel with the indicated rate change prominently displayed

## Key Assumptions to Document
- Annual loss trend rate and basis (frequency, severity, or combined)
- Expense ratio and profit/contingency target
- Credibility standard (if weighting multiple years)
- Any exclusions of accident years and justification

## Output Format
1. Experience summary table (premium, losses, loss ratios by AY)
2. Development, trend, and on-level factor table
3. Indicated rate change calculation
4. Visualization dashboard
