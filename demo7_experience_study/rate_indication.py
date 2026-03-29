"""
DEMO 7: Experience Study & Rate Indication
============================================
Copilot Features: Multi-step chained calculations, reusable utility functions

PRESENTER NOTES:
- This is the "putting it all together" demo — a full ratemaking workflow
- Ask Copilot Chat: "What adjustments are needed to trend historical losses?"

INSURANCE CONTEXT:
- Ratemaking = determining the rate needed to cover future losses + expenses
- Steps: development -> trend -> on-level -> ultimate loss ratio -> indicated rate change
- Output is the "indicated rate change" that goes into the rate filing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def compile_experience(policies_path, claims_path, line_of_business="Personal Auto"):
    """Aggregate earned premium and incurred losses by accident year."""
    policies = pd.read_csv(policies_path)
    claims = pd.read_csv(claims_path)

    policies = policies[policies["line_of_business"] == line_of_business]
    claims = claims[claims["line_of_business"] == line_of_business]

    premium_by_ay = (
        policies.groupby("policy_year")
        .agg(earned_premium=("written_premium", "sum"), earned_exposure=("earned_exposure", "sum"),
             policy_count=("policy_id", "count"))
        .rename_axis("accident_year")
    )
    losses_by_ay = (
        claims.groupby("accident_year")
        .agg(reported_incurred=("incurred_loss", "sum"), paid_losses=("paid_loss", "sum"),
             claim_count=("claim_id", "count"))
    )
    experience = premium_by_ay.join(losses_by_ay, how="left").fillna(0)
    experience["reported_loss_ratio"] = experience["reported_incurred"] / experience["earned_premium"]
    experience["frequency"] = experience["claim_count"] / experience["earned_exposure"]

    print(f"Experience Summary — {line_of_business}")
    print("=" * 90)
    print(experience.to_string(float_format=lambda x: f"{x:,.2f}" if x > 1 else f"{x:.4f}"))
    print()
    return experience


def apply_loss_development(experience):
    """Apply loss development factors to reported incurred losses."""
    current_year = experience.index.max()
    selected_ldfs = [1.000, 1.005, 1.015, 1.030, 1.060, 1.100, 1.160, 1.250, 1.380, 1.550]
    cdfs = {ay: selected_ldfs[min(current_year - ay, len(selected_ldfs) - 1)] for ay in experience.index}

    experience = experience.copy()
    experience["ldf_to_ultimate"] = experience.index.map(cdfs)
    experience["developed_ultimate"] = experience["reported_incurred"] * experience["ldf_to_ultimate"]
    return experience


def apply_loss_trend(experience, annual_trend=0.04, prospective_year=2026):
    """Trend historical losses to the prospective rating period."""
    experience = experience.copy()
    experience["trend_period"] = prospective_year - experience.index - 0.5
    experience["trend_factor"] = (1 + annual_trend) ** experience["trend_period"]
    experience["trended_ultimate"] = experience["developed_ultimate"] * experience["trend_factor"]
    return experience


def apply_on_level_factors(experience):
    """Adjust historical premiums to the current rate level."""
    rate_level_index = {
        2015: 0.82, 2016: 0.85, 2017: 0.88, 2018: 0.91, 2019: 0.93,
        2020: 0.95, 2021: 0.97, 2022: 0.99, 2023: 1.00, 2024: 1.00,
    }
    experience = experience.copy()
    experience["rate_level_index"] = experience.index.map(rate_level_index)
    experience["on_level_factor"] = 1.00 / experience["rate_level_index"]
    experience["on_level_premium"] = experience["earned_premium"] * experience["on_level_factor"]
    return experience


def calculate_rate_indication(experience, expense_ratio=0.30, profit_target=0.05):
    """Calculate the indicated rate change."""
    experience = experience.copy()
    experience["trended_loss_ratio"] = experience["trended_ultimate"] / experience["on_level_premium"]

    total_trended_ult = experience["trended_ultimate"].sum()
    total_on_level_prem = experience["on_level_premium"].sum()
    overall_loss_ratio = total_trended_ult / total_on_level_prem
    permissible_loss_ratio = 1 - expense_ratio - profit_target
    indicated_change = (overall_loss_ratio / permissible_loss_ratio) - 1

    print("=" * 80)
    print("RATE INDICATION SUMMARY")
    print("=" * 80)
    print(f"Overall Trended Loss Ratio:  {overall_loss_ratio:.1%}")
    print(f"Permissible Loss Ratio:      {permissible_loss_ratio:.1%}")
    print(f"INDICATED RATE CHANGE:       {indicated_change:+.1%}")
    print("=" * 80)
    return experience, indicated_change


def plot_rate_indication(experience, indicated_change):
    """Plot the experience study summary."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    ay = experience.index.astype(str)
    x = np.arange(len(ay))

    ax = axes[0, 0]
    ax.bar(x - 0.2, experience["on_level_premium"], 0.4, label="On-Level Premium", color="#2196F3")
    ax.bar(x + 0.2, experience["trended_ultimate"], 0.4, label="Trended Ultimate", color="#FF9800")
    ax.set_xticks(x); ax.set_xticklabels(ay, rotation=45)
    ax.set_title("On-Level Premium vs Trended Ultimate Losses"); ax.legend()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x / 1e6:.1f}M"))

    ax = axes[0, 1]
    ax.plot(ay, experience["reported_loss_ratio"], "o--", label="Reported", color="#9E9E9E")
    ax.plot(ay, experience["trended_loss_ratio"], "s-", label="Trended", color="#F44336", linewidth=2)
    ax.axhline(y=0.65, color="green", linestyle=":", label="Permissible (65%)")
    ax.set_title("Loss Ratio by Accident Year"); ax.legend()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:.0%}"))
    ax.tick_params(axis="x", rotation=45)

    ax = axes[1, 0]
    ax.plot(ay, experience["frequency"], "o-", color="#4CAF50", linewidth=2)
    ax.set_title("Claim Frequency Trend"); ax.set_ylabel("Claims per Earned Exposure")
    ax.tick_params(axis="x", rotation=45)

    ax = axes[1, 1]
    ax.axis("off")
    color = "#F44336" if indicated_change > 0 else "#4CAF50"
    ax.text(0.5, 0.6, "Indicated Rate Change", ha="center", va="center", fontsize=18,
            fontweight="bold", transform=ax.transAxes)
    ax.text(0.5, 0.35, f"{indicated_change:+.1%}", ha="center", va="center", fontsize=48,
            fontweight="bold", color=color, transform=ax.transAxes)

    plt.suptitle("Experience Study & Rate Indication — Personal Auto", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "rate_indication.png"), dpi=150)
    plt.show()


if __name__ == "__main__":
    print("DEMO 7: Experience Study & Rate Indication")
    print("=" * 80)
    print()

    experience = compile_experience(
        os.path.join(DATA_DIR, "policy_data.csv"),
        os.path.join(DATA_DIR, "claim_data.csv"),
    )
    experience = apply_loss_development(experience)
    experience = apply_loss_trend(experience)
    experience = apply_on_level_factors(experience)
    experience, indicated_change = calculate_rate_indication(experience)
    plot_rate_indication(experience, indicated_change)
