from __future__ import annotations

from dataclasses import dataclass

from options_engine.domain.models import Position, QuoteSnapshot
from options_engine.valuation.closeout import value_portfolio


@dataclass(frozen=True)
class SpotShockResult:
    shock_pct: float
    total_unrealized_pnl_mid: float
    total_unrealized_pnl_close: float
    base_total_unrealized_pnl_mid: float
    base_total_unrealized_pnl_close: float
    delta_mid_pnl: float
    delta_close_pnl: float


# Placeholder rule for first skeleton:
# apply the same percentage move to bid/ask/last/mark for option quotes.
def run_spot_shock(
    positions: list[Position],
    quotes: dict[str, QuoteSnapshot],
    shock_pct: float,
) -> SpotShockResult:
    shocked_quotes: dict[str, QuoteSnapshot] = {}
    factor = 1.0 + shock_pct
    for contract_id, quote in quotes.items():
        shocked_quotes[contract_id] = QuoteSnapshot(
            instrument_id=quote.instrument_id,
            bid=quote.bid * factor if quote.bid is not None else None,
            ask=quote.ask * factor if quote.ask is not None else None,
            last=quote.last * factor if quote.last is not None else None,
            mark=quote.mark * factor if quote.mark is not None else None,
            iv=quote.iv,
            delta=quote.delta,
            gamma=quote.gamma,
            theta=quote.theta,
            vega=quote.vega,
            rho=quote.rho,
            open_interest=quote.open_interest,
            volume=quote.volume,
            timestamp=quote.timestamp,
            source=quote.source,
        )

    base_valuation = value_portfolio(positions, quotes)
    valuation = value_portfolio(positions, shocked_quotes)
    return SpotShockResult(
        shock_pct=shock_pct,
        total_unrealized_pnl_mid=valuation.total_unrealized_pnl_mid,
        total_unrealized_pnl_close=valuation.total_unrealized_pnl_close,
        base_total_unrealized_pnl_mid=base_valuation.total_unrealized_pnl_mid,
        base_total_unrealized_pnl_close=base_valuation.total_unrealized_pnl_close,
        delta_mid_pnl=valuation.total_unrealized_pnl_mid - base_valuation.total_unrealized_pnl_mid,
        delta_close_pnl=valuation.total_unrealized_pnl_close - base_valuation.total_unrealized_pnl_close,
    )
