"""
DEMO 1: Loss Development Triangle & Chain Ladder Method
========================================================
Copilot Features: Code generation from comments, autocomplete, pandas patterns

PRESENTER NOTES:
- Open this file with all code below the imports deleted
- Type or uncomment each "# Step N" comment one at a time
- Let Copilot generate the code after each comment
- Use Copilot Chat to ask: "Explain what a chain ladder method is"

INSURANCE CONTEXT:
- The chain ladder is the most common reserving technique in P&C insurance
- Actuaries use loss triangles to project ultimate losses from partial data
- IBNR (Incurred But Not Reported) reserves are a key balance sheet item
- This mirrors work done for Schedule P filings and quarterly reserve reviews
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# =============================================================================
# Step 1: Load the loss triangle from CSV and display it
# =============================================================================


def load_loss_triangle():
    """Load the paid loss development triangle from CSV."""
    df = pd.read_csv(os.path.join(DATA_DIR, "loss_triangle.csv"), index_col="accident_year")
    print("Paid Loss Development Triangle (Cumulative)")
    print("=" * 80)
    print(df.to_string())
    print()
    return df


# =============================================================================
# Step 2: Calculate age-to-age (link ratio) development factors
# =============================================================================


def calculate_age_to_age_factors(triangle):
    """
    Calculate age-to-age development factors from a cumulative loss triangle.
    Link ratio = cumulative losses at dev period n+1 / cumulative losses at dev period n
    """
    columns = triangle.columns.tolist()
    factors = {}

    for i in range(len(columns) - 1):
        current_col = columns[i]
        next_col = columns[i + 1]

        # Only use rows where both columns have values
        mask = triangle[current_col].notna() & triangle[next_col].notna()
        current_values = triangle.loc[mask, current_col]
        next_values = triangle.loc[mask, next_col]

        # Weighted average link ratio (volume-weighted)
        weighted_factor = next_values.sum() / current_values.sum()
        factors[f"{current_col} -> {next_col}"] = round(weighted_factor, 4)

    factors_df = pd.Series(factors, name="Link Ratio")
    print("Age-to-Age Development Factors (Volume-Weighted)")
    print("=" * 60)
    print(factors_df.to_string())
    print()
    return factors_df


# =============================================================================
# Step 3: Calculate cumulative development factors (CDF) to ultimate
# =============================================================================


def calculate_cdfs_to_ultimate(age_to_age_factors):
    """
    Calculate cumulative development factors to ultimate.
    CDF at each age = product of all remaining age-to-age factors.
    Assumes a 1.000 tail factor (no development beyond the oldest maturity).
    """
    factors = age_to_age_factors.values
    n = len(factors)

    cdfs = []
    for i in range(n):
        cdf = np.prod(factors[i:])
        cdfs.append(round(cdf, 4))

    # Add a tail factor of 1.000 for the last development period
    cdfs.append(1.0000)

    cdf_labels = [f"dev_{12 * (i + 1)}" for i in range(len(cdfs))]
    cdf_series = pd.Series(cdfs, index=cdf_labels, name="CDF to Ultimate")

    print("Cumulative Development Factors to Ultimate")
    print("=" * 50)
    print(cdf_series.to_string())
    print()
    return cdf_series


# =============================================================================
# Step 4: Project ultimate losses for each accident year
# =============================================================================


def project_ultimate_losses(triangle, cdfs):
    """
    Multiply the latest diagonal value by the corresponding CDF to get ultimate losses.
    """
    results = []
    columns = triangle.columns.tolist()

    for ay in triangle.index:
        # Find the latest non-null development period for this accident year
        row = triangle.loc[ay].dropna()
        latest_dev = row.index[-1]
        latest_paid = row.iloc[-1]

        # Get the CDF for the latest development period
        dev_index = columns.index(latest_dev)
        cdf = cdfs.iloc[dev_index]

        # Ultimate = latest paid * CDF
        ultimate = round(latest_paid * cdf)
        ibnr = round(ultimate - latest_paid)

        results.append({
            "accident_year": ay,
            "latest_paid": latest_paid,
            "latest_dev_period": latest_dev,
            "cdf_to_ultimate": cdf,
            "projected_ultimate": ultimate,
            "ibnr_reserve": ibnr,
        })

    results_df = pd.DataFrame(results).set_index("accident_year")
    print("Ultimate Loss Projections & IBNR Reserves")
    print("=" * 80)
    print(results_df.to_string(float_format=lambda x: f"{x:,.0f}" if x > 100 else f"{x:.4f}"))
    print()
    print(f"Total IBNR Reserve: ${results_df['ibnr_reserve'].sum():,.0f}")
    print(f"Total Projected Ultimate: ${results_df['projected_ultimate'].sum():,.0f}")
    print()
    return results_df


# =============================================================================
# Step 5: Visualize the results — plot projected ultimates vs paid-to-date
# =============================================================================


def plot_reserve_summary(results_df):
    """Create a stacked bar chart showing paid losses and IBNR by accident year."""
    fig, ax = plt.subplots(figsize=(12, 6))

    accident_years = results_df.index.astype(str)
    paid = results_df["latest_paid"]
    ibnr = results_df["ibnr_reserve"]

    ax.bar(accident_years, paid, label="Paid to Date", color="#2196F3")
    ax.bar(accident_years, ibnr, bottom=paid, label="IBNR Reserve", color="#FF9800")

    ax.set_xlabel("Accident Year")
    ax.set_ylabel("Losses ($)")
    ax.set_title("Chain Ladder Reserve Analysis — Personal Auto Liability")
    ax.legend()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "reserve_summary.png"), dpi=150)
    plt.show()
    print("Chart saved to demo1_loss_triangle/reserve_summary.png")


# =============================================================================
# Run the full demo
# =============================================================================


if __name__ == "__main__":
    print("DEMO 1: Loss Development Triangle & Chain Ladder")
    print("=" * 80)
    print()

    # Step 1: Load the triangle
    triangle = load_loss_triangle()

    # Step 2: Calculate link ratios
    ata_factors = calculate_age_to_age_factors(triangle)

    # Step 3: Calculate CDFs to ultimate
    cdfs = calculate_cdfs_to_ultimate(ata_factors)

    # Step 4: Project ultimate losses and IBNR
    results = project_ultimate_losses(triangle, cdfs)

    # Step 5: Visualize
    plot_reserve_summary(results)
