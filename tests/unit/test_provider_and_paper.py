from datetime import datetime

from options_engine.providers.mock import MockOptionsDataProvider
from options_engine.paper.ledger import PaperFill, PaperLedger
from tests.fixtures.risk_reversal_portfolio import NBIS_CALL, QUOTES


def test_mock_provider_returns_contract_and_quote():
    provider = MockOptionsDataProvider(
        contracts={NBIS_CALL.contract_id: NBIS_CALL},
        quotes={NBIS_CALL.contract_id: QUOTES[NBIS_CALL.contract_id]},
    )
    contract = provider.search_contract("NBIS", "2027-03-19", 100.0, "C")
    quote = provider.get_option_quote(NBIS_CALL.contract_id)

    assert contract.contract_id == NBIS_CALL.contract_id
    assert quote.bid == 83.67


def test_paper_ledger_open_and_close_flow():
    ledger = PaperLedger()
    open_fill = PaperFill(
        fill_id="f1",
        order_id="o1",
        contract=NBIS_CALL,
        side="buy",
        quantity=2,
        execution_price=40.0,
        fees=1.0,
        executed_at=datetime(2026, 4, 24, 6, 0),
    )
    ledger.apply_fill(open_fill)
    assert ledger.positions[NBIS_CALL.contract_id].quantity == 2

    close_fill = PaperFill(
        fill_id="f2",
        order_id="o2",
        contract=NBIS_CALL,
        side="sell",
        quantity=1,
        execution_price=45.0,
        fees=1.0,
        executed_at=datetime(2026, 4, 24, 6, 5),
    )
    ledger.apply_fill(close_fill)

    assert ledger.positions[NBIS_CALL.contract_id].quantity == 1
    assert len(ledger.journal) == 2
    assert ledger.journal[0].action == "open"
    assert ledger.journal[1].action == "close"
    assert round(ledger.realized_pnl, 2) == round(((45.0 - 40.0) * 1 * 1 * 100) - 1.0, 2)
    assert round(ledger.total_fees, 2) == 2.0
