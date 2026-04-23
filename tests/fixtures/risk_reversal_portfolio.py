from datetime import date, datetime

from options_engine.domain.models import OptionContract, Position, QuoteSnapshot


NBIS_CALL = OptionContract(
    contract_id="NBIS-2027-03-19-100C",
    underlying="NBIS",
    expiry=date(2027, 3, 19),
    strike=100.0,
    right="C",
)

NBIS_PUT = OptionContract(
    contract_id="NBIS-2027-03-19-77.0764P",
    underlying="NBIS",
    expiry=date(2027, 3, 19),
    strike=77.0764,
    right="P",
)

POSITIONS = [
    Position(contract=NBIS_CALL, side="long", quantity=108, average_open_price=36.84, strategy_tag="risk_reversal"),
    Position(contract=NBIS_PUT, side="short", quantity=216, average_open_price=18.92, strategy_tag="risk_reversal"),
]

QUOTES = {
    NBIS_CALL.contract_id: QuoteSnapshot(
        instrument_id=NBIS_CALL.contract_id,
        bid=83.67,
        ask=85.10,
        last=84.20,
        mark=84.385,
        iv=0.87,
        delta=0.82,
        gamma=0.01,
        theta=-0.04,
        vega=0.18,
        rho=0.05,
        timestamp=datetime(2026, 4, 23, 15, 25),
        source="fixture",
    ),
    NBIS_PUT.contract_id: QuoteSnapshot(
        instrument_id=NBIS_PUT.contract_id,
        bid=10.25,
        ask=11.45,
        last=10.80,
        mark=10.85,
        iv=0.89,
        delta=-0.21,
        gamma=0.008,
        theta=-0.02,
        vega=0.11,
        rho=-0.03,
        timestamp=datetime(2026, 4, 23, 15, 25),
        source="fixture",
    ),
}
