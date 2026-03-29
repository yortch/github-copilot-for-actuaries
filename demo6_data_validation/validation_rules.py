"""
DEMO 6: Data Validation Rules for Actuarial Data
==================================================
Copilot Features: Data quality checks, regulatory validation logic

PRESENTER NOTES:
- Show Copilot generating validation rules from comments
- Ask Copilot Chat: "What data quality checks should I run on a loss triangle?"
- Pair with test_actuarial_calcs.py for the testing demo

INSURANCE CONTEXT:
- Data quality is critical for regulatory filings (NAIC, state DOI)
- Common checks: triangle balance, premium/loss reconciliation, outlier detection
"""

import pandas as pd
import numpy as np
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def validate_triangle_monotonicity(triangle_df):
    """Cumulative paid losses must be non-decreasing across development periods."""
    issues = []
    for ay in triangle_df.index:
        row = triangle_df.loc[ay].dropna()
        for i in range(len(row) - 1):
            if row.iloc[i + 1] < row.iloc[i]:
                issues.append({
                    "rule": "Triangle Monotonicity", "accident_year": ay,
                    "detail": f"{row.index[i]}={row.iloc[i]:,.0f} > {row.index[i+1]}={row.iloc[i+1]:,.0f}",
                    "severity": "ERROR",
                })
    return issues


def validate_paid_vs_incurred(claims_df):
    """Paid losses should not exceed incurred losses for any claim."""
    issues = []
    for _, claim in claims_df[claims_df["paid_loss"] > claims_df["incurred_loss"]].iterrows():
        issues.append({
            "rule": "Paid > Incurred", "accident_year": claim["accident_year"],
            "detail": f"Claim {claim['claim_id']}: Paid=${claim['paid_loss']:,.0f} > Incurred=${claim['incurred_loss']:,.0f}",
            "severity": "ERROR",
        })
    return issues


def validate_large_loss_outliers(claims_df, threshold_multiplier=10):
    """Flag claims exceeding N times the median for their LOB."""
    issues = []
    for lob in claims_df["line_of_business"].unique():
        lob_claims = claims_df[claims_df["line_of_business"] == lob]
        threshold = lob_claims["incurred_loss"].median() * threshold_multiplier
        for _, claim in lob_claims[lob_claims["incurred_loss"] > threshold].iterrows():
            issues.append({
                "rule": "Large Loss Outlier", "accident_year": claim["accident_year"],
                "detail": f"Claim {claim['claim_id']} ({lob}): ${claim['incurred_loss']:,.0f} > {threshold_multiplier}x median",
                "severity": "WARNING",
            })
    return issues


def validate_premium_reasonableness(policy_df, min_premium=100, max_premium=20_000):
    """Flag policies with premium outside reasonable bounds."""
    issues = []
    for _, pol in policy_df[policy_df["written_premium"] < min_premium].iterrows():
        issues.append({
            "rule": "Premium Too Low", "accident_year": pol["policy_year"],
            "detail": f"Policy {pol['policy_id']}: ${pol['written_premium']:,.2f}", "severity": "WARNING",
        })
    for _, pol in policy_df[policy_df["written_premium"] > max_premium].iterrows():
        issues.append({
            "rule": "Premium Too High", "accident_year": pol["policy_year"],
            "detail": f"Policy {pol['policy_id']}: ${pol['written_premium']:,.2f}", "severity": "WARNING",
        })
    return issues


def validate_loss_ratios(policy_df, claims_df, max_loss_ratio=2.0):
    """Loss ratio > 200% by accident year should be investigated."""
    issues = []
    premium_by_ay = policy_df.groupby("policy_year")["written_premium"].sum()
    losses_by_ay = claims_df.groupby("accident_year")["incurred_loss"].sum()
    for ay in premium_by_ay.index:
        if ay in losses_by_ay.index:
            lr = losses_by_ay[ay] / premium_by_ay[ay]
            if lr > max_loss_ratio:
                issues.append({
                    "rule": "High Loss Ratio", "accident_year": ay,
                    "detail": f"Loss ratio = {lr:.1%}", "severity": "WARNING",
                })
    return issues


def run_all_validations():
    """Execute all validation rules and produce a summary report."""
    print("DEMO 6: Data Validation Rules")
    print("=" * 80)

    triangle = pd.read_csv(os.path.join(DATA_DIR, "loss_triangle.csv"), index_col="accident_year")
    claims = pd.read_csv(os.path.join(DATA_DIR, "claim_data.csv"))
    policies = pd.read_csv(os.path.join(DATA_DIR, "policy_data.csv"))

    all_issues = []
    for name, fn, args in [
        ("Triangle monotonicity", validate_triangle_monotonicity, (triangle,)),
        ("Paid vs incurred", validate_paid_vs_incurred, (claims,)),
        ("Large loss outliers", validate_large_loss_outliers, (claims,)),
        ("Premium reasonableness", validate_premium_reasonableness, (policies,)),
        ("Loss ratio check", validate_loss_ratios, (policies, claims)),
    ]:
        result = fn(*args)
        all_issues.extend(result)
        print(f"  [DONE] {name}: {len(result)} issues")

    print(f"\nTotal issues found: {len(all_issues)}")
    if all_issues:
        df = pd.DataFrame(all_issues)
        print(df.groupby(["severity", "rule"]).size().reset_index(name="count").to_string(index=False))
    return all_issues


if __name__ == "__main__":
    run_all_validations()
