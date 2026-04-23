from __future__ import annotations

from options_engine.domain.models import PortfolioValuation
from options_engine.greeks.aggregate import PortfolioGreeks


def render_portfolio_summary(valuation: PortfolioValuation, greeks: PortfolioGreeks | None = None) -> str:
    lines: list[str] = []
    lines.append("Portfolio Summary")
    lines.append(f"Close-out P&L: {valuation.total_unrealized_pnl_close:,.2f}")
    lines.append(f"Mid P&L: {valuation.total_unrealized_pnl_mid:,.2f}")
    if valuation.valuation_timestamp is not None:
        lines.append(f"Valuation timestamp: {valuation.valuation_timestamp.isoformat()}")
    if greeks is not None:
        lines.append(
            "Greeks: "
            f"Δ={greeks.delta:,.2f} "
            f"Γ={greeks.gamma:,.2f} "
            f"Θ={greeks.theta:,.2f} "
            f"V={greeks.vega:,.2f} "
            f"R={greeks.rho:,.2f}"
        )
    if valuation.warnings:
        lines.append("Warnings: " + ", ".join(sorted(set(valuation.warnings))))
    return "\n".join(lines)
