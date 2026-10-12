import unittest

from backend.core.alpha_engine import analyze_binary_contract, compare_cross_exchange_prices


class AlphaEngineTests(unittest.TestCase):
    def test_uncalibrated_model_never_actionable(self):
        result = analyze_binary_contract(
            market_id="demo", option="YES", market_price=0.20,
            model_probability=0.70, bankroll=1000,
            data_is_fresh=True, model_is_calibrated=False,
        )
        self.assertEqual(result.action, "HOLD")
        self.assertEqual(result.stake_amount, 0)

    def test_paper_buy_uses_fractional_kelly_and_cap(self):
        result = analyze_binary_contract(
            market_id="demo", option="YES", market_price=0.20,
            model_probability=0.70, bankroll=1000,
            fractional_kelly=0.5, max_stake_fraction=0.10,
            data_is_fresh=True, model_is_calibrated=True,
            min_net_ev_per_dollar=0.04,
        )
        self.assertEqual(result.action, "PAPER BUY")
        self.assertLessEqual(result.stake_fraction, 0.10)
        self.assertLessEqual(result.stake_amount, 100)
        self.assertGreater(result.expected_value_per_dollar, 0)

    def test_costs_can_remove_edge(self):
        result = analyze_binary_contract(
            market_id="demo", option="NO", market_price=0.50,
            model_probability=0.55, bankroll=1000,
            estimated_cost_per_contract=0.06,
            data_is_fresh=True, model_is_calibrated=True,
        )
        self.assertEqual(result.action, "HOLD")

    def test_stale_data_blocks_signal(self):
        result = analyze_binary_contract(
            market_id="demo", option="YES", market_price=0.20,
            model_probability=0.70, bankroll=1000,
            data_is_fresh=False, model_is_calibrated=True,
        )
        self.assertEqual(result.action, "HOLD")

    def test_arbitrage_requires_identical_contracts(self):
        result = compare_cross_exchange_prices(
            price_a=0.42, price_b=0.50,
            contracts_confirmed_identical=False,
            combined_cost_per_contract=0.01,
        )
        self.assertEqual(result["action"], "NO ARBITRAGE")

    def test_complete_set_candidate_includes_costs(self):
        result = compare_cross_exchange_prices(
            price_a=0.42, price_b=0.50,
            contracts_confirmed_identical=True,
            combined_cost_per_contract=0.02,
        )
        self.assertEqual(result["action"], "PAPER ARBITRAGE CANDIDATE")
        self.assertAlmostEqual(result["theoretical_net_edge_per_set"], 0.06)


if __name__ == "__main__":
    unittest.main()
