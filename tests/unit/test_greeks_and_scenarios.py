from options_engine.greeks.aggregate import aggregate_portfolio_greeks
from options_engine.scenarios.spot_shock import run_spot_shock
from tests.fixtures.risk_reversal_portfolio import POSITIONS, QUOTES


def test_portfolio_greeks_aggregate_with_position_signs_and_multiplier():
    greeks = aggregate_portfolio_greeks(POSITIONS, QUOTES)
    expected_delta = (0.82 * 108 * 100) + ((-0.21) * -1 * 216 * 100)
    assert round(greeks.delta, 2) == round(expected_delta, 2)


def test_positive_spot_shock_changes_portfolio_values():
    base_mid = sum((((q.bid + q.ask) / 2) - p.average_open_price) * (1 if p.side == "long" else -1) * p.quantity * p.contract.multiplier for p, q in [(POSITIONS[0], QUOTES[POSITIONS[0].contract.contract_id]), (POSITIONS[1], QUOTES[POSITIONS[1].contract.contract_id])])
    shocked = run_spot_shock(POSITIONS, QUOTES, 0.10)
    assert shocked.total_unrealized_pnl_mid != round(base_mid, 2)
