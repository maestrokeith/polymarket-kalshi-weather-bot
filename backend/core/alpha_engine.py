"""Pure, simulation-only expected-value and fractional-Kelly signal calculations.

This module does not connect to exchanges, sign requests, or place/cancel orders.
All probabilities must come from an independently validated model; a threshold
breach or one observation is not sufficient to set probability to 100%.
"""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass(frozen=True)
class SignalAnalysis:
    market_id: str
    option: str
    market_probability: float
    model_probability: float
    payout_per_dollar: float
    expected_value_per_dollar: float
    edge_probability_points: float
    full_kelly_fraction: float
    fractional_kelly_fraction: float
    stake_fraction: float
    stake_amount: float
    action: str
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


def _probability(name: str, value: float) -> float:
    if not isinstance(value, (int, float)) or not 0.0 <= float(value) <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return float(value)


def analyze_binary_contract(
    *,
    market_id: str,
    option: str,
    market_price: float,
    model_probability: float,
    bankroll: float,
    fractional_kelly: float = 0.25,
    max_stake_fraction: float = 0.10,
    estimated_cost_per_contract: float = 0.0,
    min_net_ev_per_dollar: float = 0.04,
    data_is_fresh: bool = True,
    model_is_calibrated: bool = False,
) -> SignalAnalysis:
    """Calculate a paper-only signal for a $1 binary contract.

    market_price is the executable-side price estimate (ask for a buy), not the
    midpoint. estimated_cost_per_contract includes expected fees and slippage
    in dollars per contract. No action is recommended if model calibration or
    data freshness is not affirmatively confirmed.
    """
    price = _probability("market_price", market_price)
    model_p = _probability("model_probability", model_probability)
    if price <= 0.0 or price >= 1.0:
        raise ValueError("market_price must be strictly between 0 and 1")
    if bankroll < 0:
        raise ValueError("bankroll cannot be negative")
    if not 0.0 <= fractional_kelly <= 0.5:
        raise ValueError("fractional_kelly must be between 0 and 0.5")
    if not 0.0 <= max_stake_fraction <= 0.15:
        raise ValueError("max_stake_fraction must be between 0 and 0.15")
    if estimated_cost_per_contract < 0:
        raise ValueError("estimated_cost_per_contract cannot be negative")
    if min_net_ev_per_dollar < 0:
        raise ValueError("min_net_ev_per_dollar cannot be negative")

    cost = float(estimated_cost_per_contract)
    effective_cost = price + cost
    payout = 1.0 / price
    # Net expected profit per contract; payout is $1 if correct and $0 otherwise.
    ev_per_contract = model_p - effective_cost
    ev_per_dollar = ev_per_contract / price
    edge_points = model_p - price

    # Kelly for a binary contract purchased at price: f* = (p - price)/(1-price).
    full_kelly = max(0.0, (model_p - effective_cost) / (1.0 - effective_cost)) if effective_cost < 1 else 0.0
    fractional = full_kelly * fractional_kelly
    capped_fraction = min(fractional, max_stake_fraction)

    reason = "Positive net EV, but model calibration and fresh data are required."
    action = "HOLD"
    if bankroll == 0:
        reason = "Bankroll is zero."
    elif not data_is_fresh:
        reason = "Market/model inputs are stale; no signal."
    elif not model_is_calibrated:
        reason = "Model calibration is not confirmed; no actionable signal."
    elif effective_cost >= 1:
        reason = "Price plus estimated costs is at least the $1 payout."
    elif ev_per_dollar < min_net_ev_per_dollar:
        reason = "Net expected value is below the configured threshold."
    elif capped_fraction <= 0:
        reason = "Kelly stake is zero."
    else:
        action = "PAPER BUY"
        reason = "Positive net EV after estimated costs; paper signal only."

    stake_fraction = capped_fraction if action == "PAPER BUY" else 0.0
    return SignalAnalysis(
        market_id=str(market_id),
        option=str(option).upper(),
        market_probability=price,
        model_probability=model_p,
        payout_per_dollar=payout,
        expected_value_per_dollar=ev_per_dollar,
        edge_probability_points=edge_points,
        full_kelly_fraction=full_kelly,
        fractional_kelly_fraction=fractional,
        stake_fraction=stake_fraction,
        stake_amount=bankroll * stake_fraction,
        action=action,
        reason=reason,
    )


def compare_cross_exchange_prices(
    *,
    price_a: float,
    price_b: float,
    contracts_confirmed_identical: bool,
    combined_cost_per_contract: float,
) -> dict:
    """Report a possible binary complete-set arbitrage, never execute it.

    For mutually exclusive YES/NO contracts, callers must supply the price of
    complementary sides whose settlement rules are confirmed identical. This
    function rejects unverified equivalence and accounts for supplied costs.
    """
    a = _probability("price_a", price_a)
    b = _probability("price_b", price_b)
    if a <= 0 or a >= 1 or b <= 0 or b >= 1:
        raise ValueError("Prices must be strictly between 0 and 1")
    if combined_cost_per_contract < 0:
        raise ValueError("combined_cost_per_contract cannot be negative")
    raw_cost = a + b
    net_cost = raw_cost + float(combined_cost_per_contract)
    eligible = bool(contracts_confirmed_identical and net_cost < 1.0)
    return {
        "price_a": a,
        "price_b": b,
        "gross_complete_set_cost": raw_cost,
        "combined_cost_per_contract": float(combined_cost_per_contract),
        "net_complete_set_cost": net_cost,
        "theoretical_net_edge_per_set": max(0.0, 1.0 - net_cost) if eligible else 0.0,
        "action": "PAPER ARBITRAGE CANDIDATE" if eligible else "NO ARBITRAGE",
        "reason": (
            "Candidate only; identical settlement rules, fillability, fees, limits, and transfer/settlement risks require manual verification."
            if eligible else
            "No eligible arbitrage: contract equivalence is unverified or net complete-set cost is at least $1."
        ),
    }
