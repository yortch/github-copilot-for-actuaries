"""
Generate synthetic P&C insurance data for all actuarial demos.

Datasets created:
  - loss_triangle.csv     : Paid loss development triangle (Personal Auto)
  - policy_data.csv       : Policy-level exposure and premium data
  - claim_data.csv        : Individual claim-level records
  - cat_event_history.csv : Historical catastrophe event losses

All data is entirely synthetic — no real policyholder information is used.
"""

import os
import numpy as np
import pandas as pd

np.random.seed(42)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_loss_triangle():
    """
    Create a paid loss development triangle for Personal Auto Liability.
    Accident years 2015-2024, development lags 12-120 months.
    """
    accident_years = list(range(2015, 2025))
    dev_months = [12, 24, 36, 48, 60, 72, 84, 96, 108, 120]
    num_years = len(accident_years)

    # Cumulative development factors (typical auto liability pattern)
    cdf_pattern = [1.000, 1.450, 1.680, 1.800, 1.870, 1.910, 1.935, 1.950, 1.960, 1.965]

    # Base ultimate losses by accident year (with some trend)
    base_ultimate = 25_000_000
    trend = 1.04  # 4% annual loss trend
    ultimates = [base_ultimate * (trend ** i) for i in range(num_years)]

    # Build cumulative paid losses
    triangle = {}
    for i, ay in enumerate(accident_years):
        available_devs = num_years - i  # Fewer columns for more recent years
        row = {}
        for j in range(available_devs):
            dev = dev_months[j]
            # Paid at this dev = ultimate / CDF-to-ultimate at this dev * noise
            ratio = cdf_pattern[j] / cdf_pattern[-1]
            noise = np.random.normal(1.0, 0.03)
            row[dev] = round(ultimates[i] * ratio * noise)
        triangle[ay] = row

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(triangle, orient="index")
    df.index.name = "accident_year"
    df.columns = [f"dev_{m}" for m in dev_months[: df.shape[1]]]

    # Make it a proper triangle (NaN for future development)
    for i, ay in enumerate(accident_years):
        for j in range(num_years - i, len(dev_months)):
            col = f"dev_{dev_months[j]}"
            if col in df.columns:
                df.loc[ay, col] = np.nan

    df.to_csv(os.path.join(OUTPUT_DIR, "loss_triangle.csv"))
    print(f"  Created loss_triangle.csv ({len(accident_years)} accident years)")
    return df


def generate_policy_data():
    """
    Create policy-level data for Personal Auto and Homeowners.
    ~50,000 policies across 2015-2024.
    """
    n_policies = 50_000

    states = ["TX", "FL", "CA", "IL", "NY", "PA", "OH", "GA", "NC", "MI"]
    state_weights = [0.15, 0.14, 0.13, 0.10, 0.10, 0.08, 0.07, 0.07, 0.08, 0.08]

    lobs = ["Personal Auto", "Homeowners"]
    lob_weights = [0.60, 0.40]

    coverages_auto = ["Liability", "Collision", "Comprehensive"]
    coverages_home = ["Dwelling", "Personal Property", "Liability"]

    policies = {
        "policy_id": [f"POL-{i:06d}" for i in range(n_policies)],
        "policy_year": np.random.choice(range(2015, 2025), n_policies),
        "state": np.random.choice(states, n_policies, p=state_weights),
        "line_of_business": np.random.choice(lobs, n_policies, p=lob_weights),
        "driver_age": np.clip(np.random.normal(42, 15, n_policies).astype(int), 16, 85),
        "vehicle_age": np.clip(np.random.exponential(5, n_policies).astype(int), 0, 25),
        "credit_score_tier": np.random.choice(
            ["Excellent", "Good", "Fair", "Poor"], n_policies, p=[0.25, 0.35, 0.25, 0.15]
        ),
        "territory": np.random.choice([f"T{i:02d}" for i in range(1, 21)], n_policies),
        "earned_exposure": np.round(np.random.uniform(0.5, 1.0, n_policies), 2),
    }

    df = pd.DataFrame(policies)

    # Generate premiums based on risk characteristics
    base_premium = np.where(df["line_of_business"] == "Personal Auto", 800, 1200)
    age_factor = np.where(df["driver_age"] < 25, 1.6, np.where(df["driver_age"] > 65, 1.2, 1.0))
    state_factor = df["state"].map(
        {"FL": 1.3, "NY": 1.25, "CA": 1.2, "TX": 1.1, "MI": 1.15,
         "PA": 1.05, "IL": 1.05, "GA": 1.08, "NC": 1.0, "OH": 0.95}
    )
    credit_factor = df["credit_score_tier"].map(
        {"Excellent": 0.85, "Good": 1.0, "Fair": 1.15, "Poor": 1.4}
    )

    df["written_premium"] = np.round(
        base_premium * age_factor * state_factor * credit_factor * df["earned_exposure"]
        * np.random.normal(1.0, 0.05, n_policies),
        2,
    )
    df["written_premium"] = df["written_premium"].clip(lower=200)

    # Assign coverage
    df["coverage"] = df["line_of_business"].apply(
        lambda lob: np.random.choice(coverages_auto if lob == "Personal Auto" else coverages_home)
    )

    df.to_csv(os.path.join(OUTPUT_DIR, "policy_data.csv"), index=False)
    print(f"  Created policy_data.csv ({n_policies:,} policies)")
    return df


def generate_claim_data(policy_df):
    """
    Generate individual claim records linked to policies.
    Claim frequency ~ 8% for auto, 4% for homeowners.
    """
    claims = []
    claim_id = 0

    for _, policy in policy_df.iterrows():
        freq = 0.08 if policy["line_of_business"] == "Personal Auto" else 0.04
        n_claims = np.random.poisson(freq * policy["earned_exposure"])

        for _ in range(n_claims):
            claim_id += 1

            if policy["line_of_business"] == "Personal Auto":
                severity = np.random.lognormal(mean=8.5, sigma=1.2)
            else:
                severity = np.random.lognormal(mean=9.0, sigma=1.5)

            # Paid vs incurred (some claims still open)
            pct_paid = np.random.beta(5, 2)
            paid = round(severity * pct_paid, 2)
            incurred = round(severity, 2)

            claim_type = np.random.choice(
                ["Bodily Injury", "Property Damage", "Collision", "Comprehensive", "Other"],
                p=[0.25, 0.25, 0.20, 0.15, 0.15],
            ) if policy["line_of_business"] == "Personal Auto" else np.random.choice(
                ["Wind/Hail", "Water Damage", "Fire", "Theft", "Liability", "Other"],
                p=[0.30, 0.20, 0.10, 0.10, 0.15, 0.15],
            )

            status = "Closed" if pct_paid > 0.9 else "Open"

            claims.append({
                "claim_id": f"CLM-{claim_id:07d}",
                "policy_id": policy["policy_id"],
                "accident_year": policy["policy_year"],
                "state": policy["state"],
                "line_of_business": policy["line_of_business"],
                "claim_type": claim_type,
                "paid_loss": paid,
                "incurred_loss": incurred,
                "status": status,
                "report_lag_days": max(1, int(np.random.exponential(30))),
            })

    df = pd.DataFrame(claims)
    df.to_csv(os.path.join(OUTPUT_DIR, "claim_data.csv"), index=False)
    print(f"  Created claim_data.csv ({len(claims):,} claims)")
    return df


def generate_cat_events():
    """
    Generate historical catastrophe event data (hurricanes, severe storms, wildfires).
    Simulates 10 years of CAT activity across the book.
    """
    events = []
    event_id = 0

    cat_types = ["Hurricane", "Severe Storm", "Wildfire", "Winter Storm", "Tornado"]
    affected_states = {
        "Hurricane": ["FL", "TX", "NC", "GA"],
        "Severe Storm": ["TX", "IL", "OH", "PA", "GA"],
        "Wildfire": ["CA"],
        "Winter Storm": ["NY", "PA", "IL", "OH", "MI"],
        "Tornado": ["TX", "OH", "IL", "GA", "NC"],
    }

    for year in range(2015, 2025):
        n_events = np.random.poisson(4)  # ~4 CAT events per year
        for _ in range(n_events):
            event_id += 1
            cat_type = np.random.choice(cat_types, p=[0.20, 0.35, 0.10, 0.20, 0.15])
            states = affected_states[cat_type]
            primary_state = np.random.choice(states)

            # Loss severity depends on CAT type
            if cat_type == "Hurricane":
                gross_loss = np.random.lognormal(mean=17.5, sigma=1.5)
            elif cat_type == "Wildfire":
                gross_loss = np.random.lognormal(mean=16.5, sigma=1.5)
            else:
                gross_loss = np.random.lognormal(mean=15.5, sigma=1.2)

            events.append({
                "event_id": f"CAT-{event_id:04d}",
                "year": year,
                "cat_type": cat_type,
                "primary_state": primary_state,
                "gross_loss": round(gross_loss, 2),
                "claim_count": max(10, int(np.random.lognormal(4, 1))),
                "event_name": f"{year} {primary_state} {cat_type} #{event_id}",
            })

    df = pd.DataFrame(events)
    df.to_csv(os.path.join(OUTPUT_DIR, "cat_event_history.csv"), index=False)
    print(f"  Created cat_event_history.csv ({len(events)} events)")
    return df


if __name__ == "__main__":
    print("Generating synthetic P&C insurance data...")
    print()
    generate_loss_triangle()
    policy_df = generate_policy_data()
    generate_claim_data(policy_df)
    generate_cat_events()
    print()
    print("Done! All data files are in the data/ folder.")
