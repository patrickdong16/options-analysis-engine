from __future__ import annotations

from datetime import datetime

from options_engine.domain.models import LegValuation, PortfolioValuation, Position, QuoteSnapshot


def _mid_price(quote: QuoteSnapshot) -> tuple[float | None, list[str]]:
    warnings: list[str] = []
    if quote.bid is not None and quote.ask is not None:
        return (quote.bid + quote.ask) / 2.0, warnings
    if quote.mark is not None:
        warnings.append("mid_approximated_from_mark")
        return quote.mark, warnings
    warnings.append("missing_mid_price")
    return None, warnings


def _close_price(position: Position, quote: QuoteSnapshot) -> tuple[float | None, list[str]]:
    warnings: list[str] = []
    if position.side == "long":
        if quote.bid is not None:
            return quote.bid, warnings
        warnings.append("missing_bid_for_long_close")
        return None, warnings
    if quote.ask is not None:
        return quote.ask, warnings
    warnings.append("missing_ask_for_short_close")
    return None, warnings


def value_position(position: Position, quote: QuoteSnapshot) -> LegValuation:
    close_price, close_warnings = _close_price(position, quote)
    mid_price, mid_warnings = _mid_price(quote)
    warnings = [*close_warnings, *mid_warnings]
    signed = 1 if position.side == "long" else -1
    multiplier = position.contract.multiplier
    quantity = position.quantity

    pnl_close = None
    if close_price is not None:
        pnl_close = (close_price - position.average_open_price) * signed * quantity * multiplier

    pnl_mid = None
    if mid_price is not None:
        pnl_mid = (mid_price - position.average_open_price) * signed * quantity * multiplier

    return LegValuation(
        contract_id=position.contract.contract_id,
        side=position.side,
        quantity=quantity,
        multiplier=multiplier,
        entry_price=position.average_open_price,
        close_price=close_price,
        mid_price=mid_price,
        unrealized_pnl_close=pnl_close,
        unrealized_pnl_mid=pnl_mid,
        warnings=warnings,
    )


def value_portfolio(positions: list[Position], quotes: dict[str, QuoteSnapshot]) -> PortfolioValuation:
    legs: list[LegValuation] = []
    warnings: list[str] = []
    timestamps: list[datetime] = []

    for position in positions:
        quote = quotes[position.contract.contract_id]
        if quote.timestamp is not None:
            timestamps.append(quote.timestamp)
        leg = value_position(position, quote)
        legs.append(leg)
        warnings.extend(leg.warnings)

    total_close = sum(leg.unrealized_pnl_close or 0.0 for leg in legs)
    total_mid = sum(leg.unrealized_pnl_mid or 0.0 for leg in legs)
    valuation_timestamp = max(timestamps) if timestamps else None

    return PortfolioValuation(
        legs=legs,
        total_unrealized_pnl_close=total_close,
        total_unrealized_pnl_mid=total_mid,
        valuation_timestamp=valuation_timestamp,
        warnings=warnings,
    )
