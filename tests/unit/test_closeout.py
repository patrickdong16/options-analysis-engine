from options_engine.valuation.closeout import value_portfolio
from tests.fixtures.risk_reversal_portfolio import POSITIONS, QUOTES


def test_risk_reversal_closeout_uses_bid_for_long_and_ask_for_short():
    valuation = value_portfolio(POSITIONS, QUOTES)
    legs = {leg.contract_id: leg for leg in valuation.legs}

    long_leg = legs["NBIS-2027-03-19-100C"]
    short_leg = legs["NBIS-2027-03-19-77.0764P"]

    assert long_leg.close_price == 83.67
    assert short_leg.close_price == 11.45

    assert round(long_leg.unrealized_pnl_close, 2) == round((83.67 - 36.84) * 108 * 100, 2)
    assert round(short_leg.unrealized_pnl_close, 2) == round((11.45 - 18.92) * -1 * 216 * 100, 2)

    expected_total = long_leg.unrealized_pnl_close + short_leg.unrealized_pnl_close
    assert round(valuation.total_unrealized_pnl_close, 2) == round(expected_total, 2)
