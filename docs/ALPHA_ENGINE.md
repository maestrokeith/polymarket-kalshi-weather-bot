# Simulation-only Alpha Engine

The pure calculations in `backend/core/alpha_engine.py` implement an auditable decision record for a binary contract. This is a calculator, not an exchange connector or executor.

## Signal output fields

Each `SignalAnalysis` contains:
- Market ID and YES/NO option
- Market price and model probability
- Payout per dollar at the quoted contract price
- Expected value per dollar after caller-supplied estimated costs
- Probability-point edge
- Full Kelly, fractional Kelly, capped stake fraction and stake amount
- Action and reason

The EV calculation is `(model_probability - market_price - estimated_cost_per_contract) / market_price`. The gross payout for a $1 contract purchased at price `p` is `1/p`; costs must be estimated realistically, including fees, spread and slippage.

## Mandatory guardrails

- The function returns `PAPER BUY` only if data freshness and model calibration are explicitly affirmed.
- Default fractional Kelly is 0.25x. The allowed range is 0–0.5x.
- Default per-trade stake cap is 10% of bankroll; hard maximum parameter is 15%.
- A market threshold observation does not imply a 100% outcome probability. Settlement rules, station, time window, forecast uncertainty and observation quality matter.
- Cross-exchange candidates require caller confirmation that contracts have identical settlement terms. Costs must include both legs' fees/slippage. A displayed price discrepancy is not guaranteed arbitrage until both legs are fillable.
- No order signing, placement, cancellation, wallet connection, or account access is implemented here.
- Do not wire this module to live execution while `SIMULATION_MODE=true` and the server-side live gate is false.

## Run tests

From the repository root:

```bash
python -m unittest tests.test_alpha_engine -v
```

These tests use only the Python standard library plus the project source.
