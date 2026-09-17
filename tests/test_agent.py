"""
Unit tests for ElectricityDemandAgent.
Verifies future year forecasting and trajectory projections.
"""

import unittest
from electricity_agent.agent import ElectricityDemandAgent


class TestElectricityAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.agent = ElectricityDemandAgent()

    def test_calculate_country(self):
        res = self.agent.calculate_country("France", target_year=2024)
        self.assertEqual(res["iso_code"], "FRA")
        self.assertGreater(res["predicted_demand_twh"], 100)
        self.assertGreater(res["per_capita_kwh"], 1000)

    def test_calculate_future_year(self):
        # Forecast India in 2030 and 2035
        res_2024 = self.agent.calculate_country("India", target_year=2024)
        res_2030 = self.agent.calculate_country("India", target_year=2030)
        self.assertEqual(res_2030["target_year"], 2030)
        self.assertGreater(res_2030["predicted_demand_twh"], 1000)
        self.assertGreater(res_2030["projected_factors"]["population"], res_2024["projected_factors"]["population"])

    def test_calculate_bunch_group_future(self):
        res = self.agent.calculate_bunch("G7", target_year=2030)
        self.assertEqual(res["group_name"], "G7")
        self.assertEqual(res["country_count"], 7)
        self.assertEqual(res["target_year"], 2030)
        self.assertGreater(res["total_electricity_needed_twh"], 4000)

    def test_forecast_trajectory(self):
        res = self.agent.forecast_trajectory("BRICS", start_year=2024, end_year=2030, step=2)
        self.assertEqual(len(res["trajectory"]), 4)  # 2024, 2026, 2028, 2030
        self.assertEqual(res["trajectory"][0]["year"], 2024)
        self.assertEqual(res["trajectory"][-1]["year"], 2030)

    def test_simulate_scenario(self):
        res = self.agent.simulate_scenario(
            "BRICS",
            target_year=2030,
            gdp_growth_pct=15.0,
            re_capacity_expansion_pct=30.0,
        )
        self.assertEqual(res["group_name"], "BRICS")
        self.assertEqual(res["target_year"], 2030)
        self.assertGreater(res["total_scenario_twh"], 0)

    def test_explain_factors(self):
        res = self.agent.explain_country_factors("Japan", target_year=2030)
        self.assertEqual(res["country"], "Japan")
        self.assertEqual(res["target_year"], 2030)
        self.assertIn("factor_sensitivities", res)
        self.assertIn("primary_energy_consumption", res["factor_sensitivities"])

    def test_answer_prompt(self):
        prompt = "What will electricity consumption be for India and Germany in 2035 with 10% GDP growth?"
        res = self.agent.answer_prompt(prompt)
        self.assertEqual(res["target_year"], 2035)
        self.assertIn("India", res["countries"])
        self.assertIn("Germany", res["countries"])
        self.assertGreater(res["total_demand_twh"], 1000)
        self.assertIn("In **2035**", res["answer"])


if __name__ == "__main__":
    unittest.main()
