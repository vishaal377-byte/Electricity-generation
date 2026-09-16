"""
Unit tests for ElectricityDemandAgent.
"""

import unittest
from electricity_agent.agent import ElectricityDemandAgent
from electricity_agent.config import COUNTRY_GROUPS


class TestElectricityAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.agent = ElectricityDemandAgent()

    def test_calculate_country(self):
        res = self.agent.calculate_country("France")
        self.assertEqual(res["iso_code"], "FRA")
        self.assertGreater(res["predicted_demand_twh"], 100)
        self.assertGreater(res["per_capita_kwh"], 1000)

    def test_calculate_country_with_override(self):
        res_base = self.agent.calculate_country("India")
        # Double primary energy consumption
        base_energy = res_base["applied_factors"]["primary_energy_consumption"]
        res_shock = self.agent.calculate_country(
            "India",
            factors_override={"primary_energy_consumption": base_energy * 1.5}
        )
        self.assertGreater(res_shock["predicted_demand_twh"], res_base["predicted_demand_twh"])
        self.assertGreater(res_shock["delta_twh"], 0)

    def test_calculate_bunch_group(self):
        res = self.agent.calculate_bunch("G7")
        self.assertEqual(res["group_name"], "G7")
        self.assertEqual(res["country_count"], 7)
        self.assertGreater(res["total_electricity_needed_twh"], 5000)
        self.assertEqual(len(res["countries"]), 7)

    def test_calculate_bunch_custom_list(self):
        countries = ["Germany", "Brazil", "Japan"]
        res = self.agent.calculate_bunch(countries)
        self.assertEqual(res["country_count"], 3)
        self.assertGreater(res["total_electricity_needed_twh"], 1000)

    def test_simulate_scenario(self):
        res = self.agent.simulate_scenario(
            "BRICS",
            gdp_growth_pct=15.0,
            re_capacity_expansion_pct=30.0
        )
        self.assertEqual(res["group_name"], "BRICS")
        self.assertEqual(len(res["countries"]), 5)
        self.assertGreater(res["total_scenario_twh"], 0)

    def test_explain_factors(self):
        res = self.agent.explain_country_factors("Japan")
        self.assertEqual(res["country"], "Japan")
        self.assertIn("factor_sensitivities", res)
        self.assertIn("primary_energy_consumption", res["factor_sensitivities"])


if __name__ == "__main__":
    unittest.main()
