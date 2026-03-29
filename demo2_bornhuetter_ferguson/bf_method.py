"""
DEMO 2: Bornhuetter-Ferguson (BF) Reserving Method
====================================================
Copilot Features: Chat /explain, refactoring, comparing methods

PRESENTER NOTES:
- This demo builds on Demo 1 (chain ladder) to show a more sophisticated approach
- The BF method blends the chain ladder with an a priori expected loss ratio
- Great opportunity to show Copilot Chat: "What's the difference between chain ladder and BF?"
- Show Copilot refactoring: "Convert this to use the Cape Cod method instead"

INSURANCE CONTEXT:
- BF is preferred when the chain ladder is unreliable for immature accident years
- Commonly used alongside chain ladder as a "reasonableness check"
- The a priori loss ratio comes from pricing, industry benchmarks, or management selection
- Actuaries present multiple methods side-by-side in reserve committee meetings
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Add parent directory to path so we can import demo1
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from demo1_loss_triangle.chain_ladder import (
    load_loss_triangle,
    calculate_age_to_age_factors,
    calculate_cdfs_to_ultimate,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


# =============================================================================
# Step 1: Define expected (a priori) loss ratios and earned premium by AY
# =============================================================================


def get_expected_losses():
    """
    Define a priori expected ultimate losses by accident year.
    In practice, these come from pricing indications, industry data, or management judgment.
    We use earned premium * expected loss ratio.
    """
    # Simulated earned premium by accident year (growing book of business)
    earned_premium = {
        2015: 38_000_000,
        2016: 40_500_000,
        2017: 42_000_000,
        2018: 44_500_000,
        2019: 46_000_000,
        2020: 43_000_000,  # COVID dip
        2021: 48_000_000,
        2022: 52_000_000,
        2023: 55_000_000,
        2024: 58_000_000,
    }

    # A priori expected loss ratio (selected by the actuary)
    expected_loss_ratio = 0.65  # 65% loss ratio

    expected_losses = {ay: round(prem * expected_loss_ratio) for ay, prem in earned_premium.items()}

    expected_df = pd.DataFrame({
        "earned_premium": earned_premium,
        "expected_loss_ratio": expected_loss_ratio,
        "expected_ultimate": expected_losses,
    })
    expected_df.index.name = "accident_year"

    print("A Priori Expected Losses")
    print("=" * 60)
    print(expected_df.to_string(float_format=lambda x: f"{x:,.0f}" if x > 1 else f"{x:.2%}"))
    print()
    return expected_df


# =============================================================================
# Step 2: Implement the Bornhuetter-Ferguson method
# =============================================================================


def bornhuetter_ferguson(triangle, cdfs, expected_df):
    """
    Calculate BF ultimate losses.

    BF Ultimate = Paid-to-Date + Expected_Ultimate * (1 - 1/CDF)

    Where:
    - Paid-to-Date is the latest diagonal from the triangle
    - Expected_Ultimate is the a priori expected loss (from pricing/ELR)
    - CDF is the cumulative development factor to ultimate
    - (1 - 1/CDF) is the "percent unreported"
    """
    results = []
    columns = triangle.columns.tolist()

    for ay in triangle.index:
        row = triangle.loc[ay].dropna()
        latest_dev = row.index[-1]
        latest_paid = row.iloc[-1]

        dev_index = columns.index(latest_dev)
        cdf = cdfs.iloc[dev_index]

        expected_ultimate = expected_df.loc[ay, "expected_ultimate"]

        # BF Formula: ultimate = paid + expected_ult * (1 - 1/CDF)
        pct_unreported = 1 - (1 / cdf)
        bf_ibnr = round(expected_ultimate * pct_unreported)
        bf_ultimate = round(latest_paid + bf_ibnr)

        # Also compute chain ladder for comparison
        cl_ultimate = round(latest_paid * cdf)
        cl_ibnr = round(cl_ultimate - latest_paid)

        results.append({
            "accident_year": ay,
            "latest_paid": latest_paid,
            "cdf": cdf,
            "pct_unreported": round(pct_unreported, 4),
            "expected_ultimate_apriori": expected_ultimate,
            "bf_ibnr": bf_ibnr,
            "bf_ultimate": bf_ultimate,
            "cl_ibnr": cl_ibnr,
            "cl_ultimate": cl_ultimate,
            "bf_vs_cl_diff": bf_ultimate - cl_ultimate,
        })

    df = pd.DataFrame(results).set_index("accident_year")

    print("Bornhuetter-Ferguson vs Chain Ladder Comparison")
    print("=" * 100)
    print(df.to_string(float_format=lambda x: f"{x:,.0f}" if abs(x) > 1 else f"{x:.4f}"))
    print()
    print(f"Total BF IBNR:  ${df['bf_ibnr'].sum():>14,.0f}")
    print(f"Total CL IBNR:  ${df['cl_ibnr'].sum():>14,.0f}")
    print(f"Difference:     ${df['bf_vs_cl_diff'].sum():>14,.0f}")
    print()
    return df


# =============================================================================
# Step 3: Visualize BF vs Chain Ladder comparison
# =============================================================================


def plot_bf_vs_cl(results_df):
    """Create a comparison chart of BF vs Chain Ladder ultimate estimates."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    ay = results_df.index.astype(str)

    # Left panel: Ultimate losses comparison
    ax1 = axes[0]
    ax1.plot(ay, results_df["bf_ultimate"], "o-", label="BF Ultimate", color="#2196F3", linewidth=2)
    ax1.plot(ay, results_df["cl_ultimate"], "s--", label="CL Ultimate", color="#FF9800", linewidth=2)
    ax1.plot(
        ay,
        results_df["expected_ultimate_apriori"],
        "^:",
        label="A Priori Expected",
        color="#4CAF50",
        linewidth=2,
    )
    ax1.set_xlabel("Accident Year")
    ax1.set_ylabel("Ultimate Losses ($)")
    ax1.set_title("BF vs Chain Ladder — Ultimate Loss Estimates")
    ax1.legend()
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    ax1.tick_params(axis="x", rotation=45)

    # Right panel: IBNR comparison
    ax2 = axes[1]
    width = 0.35
    x = np.arange(len(ay))
    ax2.bar(x - width / 2, results_df["bf_ibnr"], width, label="BF IBNR", color="#2196F3")
    ax2.bar(x + width / 2, results_df["cl_ibnr"], width, label="CL IBNR", color="#FF9800")
    ax2.set_xticks(x)
    ax2.set_xticklabels(ay, rotation=45)
    ax2.set_xlabel("Accident Year")
    ax2.set_ylabel("IBNR Reserve ($)")
    ax2.set_title("IBNR Reserves — BF vs Chain Ladder")
    ax2.legend()
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "bf_vs_cl_comparison.png"), dpi=150)
    plt.show()
    print("Chart saved to demo2_bornhuetter_ferguson/bf_vs_cl_comparison.png")


# =============================================================================
# Run the full demo
# =============================================================================


if __name__ == "__main__":
    print("DEMO 2: Bornhuetter-Ferguson Reserving Method")
    print("=" * 80)
    print()

    # Reuse chain ladder components from Demo 1
    triangle = load_loss_triangle()
    ata_factors = calculate_age_to_age_factors(triangle)
    cdfs = calculate_cdfs_to_ultimate(ata_factors)

    # BF-specific steps
    expected_df = get_expected_losses()
    results = bornhuetter_ferguson(triangle, cdfs, expected_df)
    plot_bf_vs_cl(results)
