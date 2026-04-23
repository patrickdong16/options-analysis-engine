from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Literal, Optional

Right = Literal["C", "P"]
Side = Literal["long", "short"]
Style = Literal["american", "european"]


@dataclass(frozen=True)
class OptionContract:
    contract_id: str
    underlying: str
    expiry: date
    strike: float
    right: Right
    multiplier: int = 100
    style: Style = "american"
    currency: str = "USD"
    provider_symbol: Optional[str] = None


@dataclass(frozen=True)
class QuoteSnapshot:
    instrument_id: str
    bid: Optional[float]
    ask: Optional[float]
    last: Optional[float]
    mark: Optional[float]
    iv: Optional[float]
    delta: Optional[float] = None
    gamma: Optional[float] = None
    theta: Optional[float] = None
    vega: Optional[float] = None
    rho: Optional[float] = None
    open_interest: Optional[int] = None
    volume: Optional[int] = None
    timestamp: Optional[datetime] = None
    source: Optional[str] = None


@dataclass(frozen=True)
class Position:
    contract: OptionContract
    side: Side
    quantity: int
    average_open_price: float
    opened_at: Optional[datetime] = None
    strategy_tag: str = "custom"

    @property
    def signed_quantity(self) -> int:
        return self.quantity if self.side == "long" else -self.quantity


@dataclass(frozen=True)
class LegValuation:
    contract_id: str
    side: Side
    quantity: int
    multiplier: int
    entry_price: float
    close_price: Optional[float]
    mid_price: Optional[float]
    unrealized_pnl_close: Optional[float]
    unrealized_pnl_mid: Optional[float]
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class PortfolioValuation:
    legs: list[LegValuation]
    total_unrealized_pnl_close: float
    total_unrealized_pnl_mid: float
    valuation_timestamp: Optional[datetime]
    warnings: list[str] = field(default_factory=list)
