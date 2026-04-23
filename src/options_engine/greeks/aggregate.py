from __future__ import annotations

from dataclasses import dataclass

from options_engine.domain.models import Position, QuoteSnapshot


@dataclass(frozen=True)
class PortfolioGreeks:
    delta: float = 0.0
    gamma: float = 0.0
    theta: float = 0.0
    vega: float = 0.0
    rho: float = 0.0


def aggregate_portfolio_greeks(positions: list[Position], quotes: dict[str, QuoteSnapshot]) -> PortfolioGreeks:
    totals = {"delta": 0.0, "gamma": 0.0, "theta": 0.0, "vega": 0.0, "rho": 0.0}

    for position in positions:
        quote = quotes[position.contract.contract_id]
        sign = 1.0 if position.side == "long" else -1.0
        scale = sign * position.quantity * position.contract.multiplier
        totals["delta"] += (quote.delta or 0.0) * scale
        totals["gamma"] += (quote.gamma or 0.0) * scale
        totals["theta"] += (quote.theta or 0.0) * scale
        totals["vega"] += (quote.vega or 0.0) * scale
        totals["rho"] += (quote.rho or 0.0) * scale

    return PortfolioGreeks(**totals)
