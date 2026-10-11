import json
from types import SimpleNamespace

from backend.core.settlement import calculate_pnl, _parse_market_resolution


def trade(direction: str, price: float = 0.40, size: float = 10.0):
    return SimpleNamespace(direction=direction, entry_price=price, size=size)


def test_yes_win_pnl():
    assert calculate_pnl(trade("yes"), 1.0) == 6.0


def test_yes_loss_pnl():
    assert calculate_pnl(trade("yes"), 0.0) == -4.0


def test_no_win_pnl():
    assert calculate_pnl(trade("no"), 0.0) == 6.0


def test_btc_up_down_aliases():
    assert calculate_pnl(trade("up"), 1.0) == 6.0
    assert calculate_pnl(trade("down"), 0.0) == 6.0


def test_unclosed_market_is_not_settled():
    assert _parse_market_resolution({"closed": False, "outcomePrices": "[1,0]"}) == (False, None)


def test_closed_market_first_outcome_win():
    assert _parse_market_resolution({"id": "fixture", "closed": True, "outcomePrices": json.dumps(["1", "0"])}) == (True, 1.0)


def test_closed_market_second_outcome_win():
    assert _parse_market_resolution({"id": "fixture", "closed": True, "outcomePrices": ["0", "1"]}) == (True, 0.0)


def test_ambiguous_resolution_is_not_settled():
    assert _parse_market_resolution({"closed": True, "outcomePrices": ["0.5", "0.5"]}) == (False, None)
