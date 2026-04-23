from options_engine.greeks.aggregate import aggregate_portfolio_greeks
from options_engine.scenarios.spot_shock import run_spot_shock
from tests.fixtures.risk_reversal_portfolio import POSITIONS, QUOTES


def test_portfolio_greeks_aggregate_with_position_signs_and_multiplier():
    greeks = aggregate_portfolio_greeks(POSITIONS, QUOTES)
    expected_delta = (0.82 * 108 * 100) + ((-0.21) * -1 * 216 * 100)
    assert round(greeks.delta, 2) == round(expected_delta, 2)


def test_positive_spot_shock_changes_portfolio_values():
    shocked = run_spot_shock(POSITIONS, QUOTES, 0.10)
    assert shocked.total_unrealized_pnl_mid != shocked.base_total_unrealized_pnl_mid
    assert round(shocked.delta_mid_pnl, 2) == round(shocked.total_unrealized_pnl_mid - shocked.base_total_unrealized_pnl_mid, 2)
    assert round(shocked.delta_close_pnl, 2) == round(shocked.total_unrealized_pnl_close - shocked.base_total_unrealized_pnl_close, 2)
