"""
DEMO 4: Catastrophe Loss Exceedance Curve
==========================================
Copilot Features: Monte Carlo simulation code, statistical distributions, visualization

PRESENTER NOTES:
- CAT modeling is critical for P&C insurers — especially in FL, TX, CA
- Show Copilot generating simulation loops and distribution fitting
- Ask Copilot Chat: "What's the difference between OEP and AEP?"
- Great demo for showing Copilot's understanding of risk metrics (VaR, TVaR)

INSURANCE CONTEXT:
- Insurers model catastrophe risk (hurricanes, earthquakes, wildfires) with simulation
- OEP = Occurrence Exceedance Probability (single largest event in a year)
- AEP = Aggregate Exceedance Probability (total of all events in a year)
- Key return periods: 1-in-100 (1%), 1-in-250 (0.4%) are used for capital and reinsurance
- Results feed into reinsurance purchasing, capital modeling, and rating agency analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


# =============================================================================
# Step 1: Load and analyze historical catastrophe event data
# =============================================================================


def load_cat_data():
    """Load historical CAT event data and summarize by type."""
    cat_df = pd.read_csv(os.path.join(DATA_DIR, "cat_event_history.csv"))

    print("Historical Catastrophe Events Summary")
    print("=" * 70)

    summary = (
        cat_df.groupby("cat_type")
        .agg(
            event_count=("event_id", "count"),
            avg_loss=("gross_loss", "mean"),
            max_loss=("gross_loss", "max"),
            total_claims=("claim_count", "sum"),
        )
        .sort_values("avg_loss", ascending=False)
    )

    print(summary.to_string(float_format=lambda x: f"${x:,.0f}" if x > 100 else f"{x:.0f}"))
    print(f"\nTotal events: {len(cat_df)}")
    print(f"Average events per year: {len(cat_df) / 10:.1f}")
    print()
    return cat_df


# =============================================================================
# Step 2: Fit frequency and severity distributions to historical data
# =============================================================================


def fit_cat_distributions(cat_df):
    """
    Fit statistical distributions to CAT event data:
    - Frequency: Poisson (events per year)
    - Severity: Lognormal (loss per event)
    """
    # Frequency: events per year
    events_per_year = cat_df.groupby("year").size()
    avg_freq = events_per_year.mean()
    print(f"CAT Frequency: Poisson(lambda={avg_freq:.2f})")

    # Severity: fit lognormal to gross losses
    losses = cat_df["gross_loss"].values
    log_losses = np.log(losses)
    mu = log_losses.mean()
    sigma = log_losses.std()
    print(f"CAT Severity: LogNormal(mu={mu:.2f}, sigma={sigma:.2f})")
    print(f"  Mean severity: ${np.exp(mu + sigma**2 / 2):,.0f}")
    print(f"  Median severity: ${np.exp(mu):,.0f}")
    print()

    return avg_freq, mu, sigma


# =============================================================================
# Step 3: Run Monte Carlo simulation for annual CAT losses
# =============================================================================


def simulate_cat_losses(avg_freq, mu, sigma, n_simulations=100_000):
    """
    Monte Carlo simulation of annual catastrophe losses.
    For each simulated year:
    1. Draw number of events from Poisson(avg_freq)
    2. For each event, draw a loss from LogNormal(mu, sigma)
    3. Record the maximum single event loss (for OEP) and total (for AEP)
    """
    rng = np.random.default_rng(seed=42)

    oep_losses = np.zeros(n_simulations)  # Max single event per year
    aep_losses = np.zeros(n_simulations)  # Aggregate losses per year

    for i in range(n_simulations):
        n_events = rng.poisson(avg_freq)

        if n_events > 0:
            event_losses = rng.lognormal(mu, sigma, n_events)
            oep_losses[i] = event_losses.max()
            aep_losses[i] = event_losses.sum()
        else:
            oep_losses[i] = 0
            aep_losses[i] = 0

    print(f"Simulation complete: {n_simulations:,} years simulated")
    print(f"  Years with 0 CAT events: {(aep_losses == 0).sum():,} ({(aep_losses == 0).mean():.1%})")
    print(f"  Average annual aggregate: ${aep_losses.mean():,.0f}")
    print(f"  Max single event (across all sims): ${oep_losses.max():,.0f}")
    print()

    return oep_losses, aep_losses


# =============================================================================
# Step 4: Build exceedance probability curves and calculate risk metrics
# =============================================================================


def build_ep_curves(oep_losses, aep_losses):
    """
    Build OEP and AEP exceedance probability curves.
    Calculate VaR and TVaR at key return periods.
    """
    return_periods = [10, 25, 50, 100, 250, 500]

    print("Exceedance Probability Analysis")
    print("=" * 80)
    print(f"{'Return Period':<15} {'Exceedance Prob':<18} {'OEP ($)':<20} {'AEP ($)':<20}")
    print("-" * 80)

    results = []
    for rp in return_periods:
        prob = 1 / rp
        percentile = 1 - prob

        oep_val = np.percentile(oep_losses, percentile * 100)
        aep_val = np.percentile(aep_losses, percentile * 100)

        # TVaR (Tail Value at Risk) = average of losses exceeding VaR
        oep_tvar = oep_losses[oep_losses >= oep_val].mean() if (oep_losses >= oep_val).any() else 0
        aep_tvar = aep_losses[aep_losses >= aep_val].mean() if (aep_losses >= aep_val).any() else 0

        print(f"1-in-{rp:<10} {prob:<18.2%} ${oep_val:<19,.0f} ${aep_val:<19,.0f}")

        results.append({
            "return_period": rp,
            "exceedance_prob": prob,
            "oep_var": oep_val,
            "aep_var": aep_val,
            "oep_tvar": oep_tvar,
            "aep_tvar": aep_tvar,
        })

    print()

    # Highlight key metrics used in reinsurance and capital
    print("Key Risk Metrics:")
    print(f"  1-in-100 OEP VaR:  ${results[3]['oep_var']:>15,.0f}")
    print(f"  1-in-100 OEP TVaR: ${results[3]['oep_tvar']:>15,.0f}")
    print(f"  1-in-250 AEP VaR:  ${results[4]['aep_var']:>15,.0f}")
    print(f"  1-in-250 AEP TVaR: ${results[4]['aep_tvar']:>15,.0f}")
    print()

    return pd.DataFrame(results)


# =============================================================================
# Step 5: Visualize exceedance probability curves
# =============================================================================


def plot_ep_curves(oep_losses, aep_losses, ep_table):
    """Plot OEP and AEP exceedance probability curves."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Sort losses for empirical EP curve
    sorted_oep = np.sort(oep_losses)[::-1]
    sorted_aep = np.sort(aep_losses)[::-1]
    n = len(sorted_oep)
    probs = np.arange(1, n + 1) / n

    # Left: OEP curve
    ax1 = axes[0]
    ax1.semilogy(sorted_oep[sorted_oep > 0], probs[: (sorted_oep > 0).sum()], color="#2196F3", linewidth=1.5)
    ax1.axhline(y=0.01, color="red", linestyle="--", alpha=0.7, label="1-in-100")
    ax1.axhline(y=0.004, color="darkred", linestyle="--", alpha=0.7, label="1-in-250")
    ax1.set_xlabel("Loss ($)")
    ax1.set_ylabel("Exceedance Probability")
    ax1.set_title("OEP Curve (Single Largest Event)")
    ax1.legend()
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x / 1e6:.0f}M"))
    ax1.grid(True, alpha=0.3)

    # Right: AEP curve
    ax2 = axes[1]
    ax2.semilogy(sorted_aep[sorted_aep > 0], probs[: (sorted_aep > 0).sum()], color="#FF9800", linewidth=1.5)
    ax2.axhline(y=0.01, color="red", linestyle="--", alpha=0.7, label="1-in-100")
    ax2.axhline(y=0.004, color="darkred", linestyle="--", alpha=0.7, label="1-in-250")
    ax2.set_xlabel("Loss ($)")
    ax2.set_ylabel("Exceedance Probability")
    ax2.set_title("AEP Curve (Annual Aggregate)")
    ax2.legend()
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x / 1e6:.0f}M"))
    ax2.grid(True, alpha=0.3)

    plt.suptitle("Catastrophe Loss Exceedance Probability Curves", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "ep_curves.png"), dpi=150)
    plt.show()
    print("Chart saved to demo4_cat_modeling/ep_curves.png")


# =============================================================================
# Run the full demo
# =============================================================================


if __name__ == "__main__":
    print("DEMO 4: Catastrophe Loss Exceedance Curve")
    print("=" * 80)
    print()

    # Step 1: Load historical data
    cat_df = load_cat_data()

    # Step 2: Fit distributions
    avg_freq, mu, sigma = fit_cat_distributions(cat_df)

    # Step 3: Monte Carlo simulation
    oep_losses, aep_losses = simulate_cat_losses(avg_freq, mu, sigma)

    # Step 4: EP curves and risk metrics
    ep_table = build_ep_curves(oep_losses, aep_losses)

    # Step 5: Visualize
    plot_ep_curves(oep_losses, aep_losses, ep_table)
