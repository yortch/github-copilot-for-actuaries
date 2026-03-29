"""
DEMO 5: VBA-to-Python Migration — Premium Rating Calculator
=============================================================
Copilot Features: Cross-language translation, /explain, refactoring

PRESENTER NOTES:
- Start by opening premium_calc.vba and asking Copilot Chat to explain it
- Then ask Copilot to "Convert this to Python"
- Compare the generated code with this "answer key"
- This is often the MOST impactful demo for insurance actuarial teams

INSURANCE CONTEXT:
- Many actuarial teams have legacy VBA macros embedded in Excel workbooks
- Migrating to Python makes the logic testable, auditable, and scalable
- The rating factors here are typical of a personal auto pricing model
"""

import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

BASE_RATE = 800.0
MINIMUM_PREMIUM = 300.0


def get_age_factor(driver_age: int) -> float:
    """Driver age rating factor — young and elderly drivers pay more."""
    if driver_age < 21:
        return 2.1
    elif driver_age <= 25:
        return 1.6
    elif driver_age <= 35:
        return 1.1
    elif driver_age <= 45:
        return 1.0
    elif driver_age <= 55:
        return 0.95
    elif driver_age <= 65:
        return 1.0
    else:
        return 1.2


def get_state_factor(state: str) -> float:
    """Territory/state rating factor."""
    state_factors = {
        "FL": 1.30, "NY": 1.25, "CA": 1.20, "MI": 1.15, "TX": 1.10,
        "GA": 1.08, "PA": 1.05, "IL": 1.05, "NC": 1.00, "OH": 0.95,
    }
    return state_factors.get(state.upper(), 1.0)


def get_credit_factor(credit_tier: str) -> float:
    """Insurance credit score tier factor."""
    credit_factors = {"EXCELLENT": 0.85, "GOOD": 1.00, "FAIR": 1.15, "POOR": 1.40}
    return credit_factors.get(credit_tier.upper(), 1.0)


def get_vehicle_age_factor(vehicle_age: int) -> float:
    """Vehicle age factor — newer vehicles cost more to insure."""
    if vehicle_age <= 2:
        return 1.15
    elif vehicle_age <= 5:
        return 1.05
    elif vehicle_age <= 10:
        return 1.00
    elif vehicle_age <= 15:
        return 0.90
    else:
        return 0.80


def calculate_premium(driver_age: int, state: str, credit_tier: str, vehicle_age: int) -> dict:
    """Calculate auto insurance premium for a single policy."""
    age_factor = get_age_factor(driver_age)
    state_factor = get_state_factor(state)
    credit_factor = get_credit_factor(credit_tier)
    vehicle_factor = get_vehicle_age_factor(vehicle_age)

    premium = BASE_RATE * age_factor * state_factor * credit_factor * vehicle_factor
    premium = max(premium, MINIMUM_PREMIUM)

    return {
        "age_factor": age_factor,
        "state_factor": state_factor,
        "credit_factor": credit_factor,
        "vehicle_factor": vehicle_factor,
        "calculated_premium": round(premium, 2),
    }


def calculate_premiums_batch(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate premiums for a DataFrame of policies (vectorized)."""
    df = df.copy()
    df["age_factor"] = df["driver_age"].apply(get_age_factor)
    df["state_factor"] = df["state"].apply(get_state_factor)
    df["credit_factor"] = df["credit_score_tier"].apply(get_credit_factor)
    df["vehicle_factor"] = df["vehicle_age"].apply(get_vehicle_age_factor)

    df["calculated_premium"] = (
        BASE_RATE * df["age_factor"] * df["state_factor"] * df["credit_factor"] * df["vehicle_factor"]
    ).round(2).clip(lower=MINIMUM_PREMIUM)

    return df


if __name__ == "__main__":
    print("DEMO 5: VBA-to-Python Migration — Premium Calculator")
    print("=" * 80)
    print()

    policies = pd.read_csv(os.path.join(DATA_DIR, "policy_data.csv"))
    auto_policies = policies[policies["line_of_business"] == "Personal Auto"].copy()

    print(f"Calculating premiums for {len(auto_policies):,} Personal Auto policies...")
    rated = calculate_premiums_batch(auto_policies)

    sample_cols = [
        "policy_id", "driver_age", "state", "credit_score_tier", "vehicle_age",
        "age_factor", "state_factor", "credit_factor", "vehicle_factor",
        "written_premium", "calculated_premium",
    ]
    print("\nSample Rated Policies (first 10):")
    print(rated[sample_cols].head(10).to_string(index=False))

    print(f"\nAverage premium: ${rated['calculated_premium'].mean():,.2f}")
    print(f"Total premium:   ${rated['calculated_premium'].sum():,.0f}")

    print("\nSingle Policy Example (19yo, FL, Poor credit, new car):")
    result = calculate_premium(driver_age=19, state="FL", credit_tier="Poor", vehicle_age=1)
    for key, value in result.items():
        print(f"  {key}: {value}")
