"""
DEMO 3: Frequency-Severity GLM Pricing Model
=============================================
Copilot Features: Statistical code generation, inline suggestions, data wrangling

PRESENTER NOTES:
- This is a core ratemaking workflow — many actuaries do this in SAS or Excel today
- Show Copilot generating statsmodels GLM code from comments
- Great for "ask Copilot Chat: what distribution should I use for claim frequency?"
- Show inline suggestions as you type model formulas

INSURANCE CONTEXT:
- P&C actuaries build GLMs to determine base rates and rating factor relativities
- Frequency model (Poisson): How often do claims occur per exposure?
- Severity model (Gamma): Given a claim, how large is it?
- Pure Premium = Frequency × Severity — this drives the filed rate
- Relativities by rating variable determine surcharges/discounts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


# =============================================================================
# Step 1: Load and prepare policy/claim data for modeling
# =============================================================================


def prepare_modeling_data():
    """
    Merge policy and claim data to create a modeling dataset.
    Aggregate to one row per policy with claim count and average severity.
    """
    policies = pd.read_csv(os.path.join(DATA_DIR, "policy_data.csv"))
    claims = pd.read_csv(os.path.join(DATA_DIR, "claim_data.csv"))

    # Filter to Personal Auto only (for this demo)
    policies = policies[policies["line_of_business"] == "Personal Auto"].copy()

    # Aggregate claims to policy level
    claim_summary = (
        claims.groupby("policy_id")
        .agg(claim_count=("claim_id", "count"), total_incurred=("incurred_loss", "sum"))
        .reset_index()
    )

    # Merge — policies with no claims get 0
    model_df = policies.merge(claim_summary, on="policy_id", how="left")
    model_df["claim_count"] = model_df["claim_count"].fillna(0).astype(int)
    model_df["total_incurred"] = model_df["total_incurred"].fillna(0)

    # Calculate average severity for policies with claims
    model_df["avg_severity"] = np.where(
        model_df["claim_count"] > 0,
        model_df["total_incurred"] / model_df["claim_count"],
        0,
    )

    # Create age bands for modeling
    model_df["driver_age_band"] = pd.cut(
        model_df["driver_age"],
        bins=[0, 25, 35, 45, 55, 65, 100],
        labels=["16-25", "26-35", "36-45", "46-55", "56-65", "65+"],
    )

    model_df["vehicle_age_band"] = pd.cut(
        model_df["vehicle_age"],
        bins=[-1, 2, 5, 10, 15, 100],
        labels=["0-2", "3-5", "6-10", "11-15", "16+"],
    )

    print(f"Modeling dataset: {len(model_df):,} Personal Auto policies")
    print(f"  Claims: {model_df['claim_count'].sum():,}")
    print(f"  Claim frequency: {model_df['claim_count'].sum() / model_df['earned_exposure'].sum():.4f}")
    print(f"  Average severity: ${model_df.loc[model_df['claim_count'] > 0, 'avg_severity'].mean():,.0f}")
    print()
    return model_df


# =============================================================================
# Step 2: Fit a Poisson GLM for claim frequency
# =============================================================================


def fit_frequency_model(model_df):
    """
    Fit a Poisson GLM for claim frequency.
    Response: claim_count
    Exposure: earned_exposure (as offset)
    Predictors: driver_age_band, vehicle_age_band, credit_score_tier, state
    """
    # Prepare the formula with categorical variables
    model_df = model_df.copy()
    model_df["log_exposure"] = np.log(model_df["earned_exposure"])

    formula = (
        "claim_count ~ C(driver_age_band, Treatment('36-45')) "
        "+ C(vehicle_age_band, Treatment('3-5')) "
        "+ C(credit_score_tier, Treatment('Good')) "
        "+ C(state, Treatment('OH'))"
    )

    freq_model = smf.glm(
        formula=formula,
        data=model_df,
        family=sm.families.Poisson(),
        offset=model_df["log_exposure"],
    ).fit()

    print("Frequency Model (Poisson GLM)")
    print("=" * 80)
    print(freq_model.summary())
    print()
    return freq_model


# =============================================================================
# Step 3: Fit a Gamma GLM for claim severity
# =============================================================================


def fit_severity_model(model_df):
    """
    Fit a Gamma GLM for average claim severity.
    Only use records with at least one claim (severity is conditional on a claim occurring).
    """
    claims_only = model_df[model_df["claim_count"] > 0].copy()

    formula = (
        "avg_severity ~ C(driver_age_band, Treatment('36-45')) "
        "+ C(vehicle_age_band, Treatment('3-5')) "
        "+ C(credit_score_tier, Treatment('Good')) "
        "+ C(state, Treatment('OH'))"
    )

    sev_model = smf.glm(
        formula=formula,
        data=claims_only,
        family=sm.families.Gamma(link=sm.families.links.Log()),
    ).fit()

    print("Severity Model (Gamma GLM with Log Link)")
    print("=" * 80)
    print(sev_model.summary())
    print()
    return sev_model


# =============================================================================
# Step 4: Calculate rating relativities from model coefficients
# =============================================================================


def extract_relativities(freq_model, sev_model):
    """
    Convert GLM coefficients to multiplicative relativities.
    Relativity = exp(coefficient) for log-link models.
    """
    print("Rating Relativities (Base = 1.000)")
    print("=" * 80)

    for name, model in [("Frequency", freq_model), ("Severity", sev_model)]:
        print(f"\n{name} Relativities:")
        print("-" * 50)

        params = model.params
        for param_name, coef in params.items():
            if param_name == "Intercept":
                print(f"  Base Rate (Intercept): {np.exp(coef):.4f}")
            else:
                relativity = np.exp(coef)
                # Clean up the parameter name
                clean_name = param_name.replace("C(", "").replace(")", "").replace("Treatment", "Base")
                print(f"  {clean_name}: {relativity:.4f}")

    print()


# =============================================================================
# Step 5: Calculate pure premiums by driver age band
# =============================================================================


def calculate_pure_premiums(model_df, freq_model, sev_model):
    """
    Calculate predicted pure premiums (frequency x severity) by rating segment.
    """
    model_df = model_df.copy()
    model_df["log_exposure"] = np.log(model_df["earned_exposure"])

    # Predict frequency and severity
    model_df["pred_frequency"] = freq_model.predict(model_df)
    model_df["pred_freq_per_exposure"] = model_df["pred_frequency"] / model_df["earned_exposure"]

    # For severity, predict on all rows (using model coefficients)
    model_df["pred_severity"] = sev_model.predict(model_df)

    # Pure premium = frequency × severity
    model_df["pred_pure_premium"] = model_df["pred_freq_per_exposure"] * model_df["pred_severity"]

    # Summarize by driver age band
    summary = (
        model_df.groupby("driver_age_band", observed=True)
        .agg(
            policies=("policy_id", "count"),
            avg_pred_frequency=("pred_freq_per_exposure", "mean"),
            avg_pred_severity=("pred_severity", "mean"),
            avg_pure_premium=("pred_pure_premium", "mean"),
            actual_frequency=(
                "claim_count",
                lambda x: x.sum() / model_df.loc[x.index, "earned_exposure"].sum(),
            ),
        )
        .round(2)
    )

    print("Pure Premium Summary by Driver Age Band")
    print("=" * 80)
    print(summary.to_string())
    print()
    return model_df, summary


# =============================================================================
# Step 6: Visualize relativities
# =============================================================================


def plot_relativities(summary_df):
    """Plot predicted vs actual frequency by driver age band."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    age_bands = summary_df.index.astype(str)
    x = np.arange(len(age_bands))

    # Frequency
    axes[0].bar(x, summary_df["avg_pred_frequency"], color="#2196F3", alpha=0.8, label="Predicted")
    axes[0].bar(x, summary_df["actual_frequency"], color="#FF9800", alpha=0.5, label="Actual")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(age_bands, rotation=45)
    axes[0].set_title("Claim Frequency by Driver Age")
    axes[0].set_ylabel("Frequency")
    axes[0].legend()

    # Severity
    axes[1].bar(x, summary_df["avg_pred_severity"], color="#4CAF50")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(age_bands, rotation=45)
    axes[1].set_title("Predicted Severity by Driver Age")
    axes[1].set_ylabel("Average Severity ($)")
    axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

    # Pure Premium
    axes[2].bar(x, summary_df["avg_pure_premium"], color="#9C27B0")
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(age_bands, rotation=45)
    axes[2].set_title("Pure Premium by Driver Age")
    axes[2].set_ylabel("Pure Premium ($)")
    axes[2].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

    plt.suptitle("Personal Auto GLM Rating Analysis", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "glm_relativities.png"), dpi=150)
    plt.show()
    print("Chart saved to demo3_glm_pricing/glm_relativities.png")


# =============================================================================
# Run the full demo
# =============================================================================


if __name__ == "__main__":
    print("DEMO 3: Frequency-Severity GLM Pricing Model")
    print("=" * 80)
    print()

    # Step 1: Prepare data
    model_df = prepare_modeling_data()

    # Step 2: Frequency model
    freq_model = fit_frequency_model(model_df)

    # Step 3: Severity model
    sev_model = fit_severity_model(model_df)

    # Step 4: Rating relativities
    extract_relativities(freq_model, sev_model)

    # Step 5: Pure premiums
    model_df, summary = calculate_pure_premiums(model_df, freq_model, sev_model)

    # Step 6: Visualize
    plot_relativities(summary)
