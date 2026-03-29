"""
DEMO 6 (Part 2): Unit Tests for Actuarial Calculations
========================================================
Copilot Features: Test generation, assert patterns, edge cases

PRESENTER NOTES:
- Ask Copilot Chat: "Generate unit tests for the premium calculator"
- Show how tests catch regressions when actuarial logic changes
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from demo5_vba_migration.premium_calc import (
    get_age_factor, get_state_factor, get_credit_factor,
    get_vehicle_age_factor, calculate_premium, BASE_RATE, MINIMUM_PREMIUM,
)


class TestDriverAgeFactor(unittest.TestCase):
    def test_young_driver_surcharge(self):
        self.assertEqual(get_age_factor(18), 2.1)

    def test_base_rate_age(self):
        self.assertEqual(get_age_factor(40), 1.0)

    def test_senior_surcharge(self):
        self.assertEqual(get_age_factor(70), 1.2)

    def test_preferred_age(self):
        self.assertEqual(get_age_factor(50), 0.95)


class TestStateFactor(unittest.TestCase):
    def test_high_cost_states(self):
        self.assertEqual(get_state_factor("FL"), 1.30)
        self.assertEqual(get_state_factor("NY"), 1.25)

    def test_case_insensitive(self):
        self.assertEqual(get_state_factor("fl"), 1.30)

    def test_unknown_state(self):
        self.assertEqual(get_state_factor("ZZ"), 1.0)


class TestPremiumCalculation(unittest.TestCase):
    def test_base_case(self):
        result = calculate_premium(driver_age=40, state="OH", credit_tier="Good", vehicle_age=7)
        expected = BASE_RATE * 1.0 * 0.95 * 1.0 * 1.0
        self.assertAlmostEqual(result["calculated_premium"], expected, places=2)

    def test_minimum_premium_enforced(self):
        result = calculate_premium(driver_age=50, state="OH", credit_tier="Excellent", vehicle_age=20)
        self.assertGreaterEqual(result["calculated_premium"], MINIMUM_PREMIUM)

    def test_high_risk_profile(self):
        result = calculate_premium(driver_age=19, state="FL", credit_tier="Poor", vehicle_age=1)
        self.assertGreater(result["calculated_premium"], 3000)

    def test_all_factors_returned(self):
        result = calculate_premium(driver_age=30, state="TX", credit_tier="Good", vehicle_age=5)
        expected_keys = {"age_factor", "state_factor", "credit_factor", "vehicle_factor", "calculated_premium"}
        self.assertEqual(set(result.keys()), expected_keys)


if __name__ == "__main__":
    print("DEMO 6 (Part 2): Unit Tests for Actuarial Calculations")
    print("=" * 60)
    unittest.main(verbosity=2)
