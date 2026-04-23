from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from options_engine.domain.models import OptionContract, Position

OrderSide = Literal["buy", "sell"]
PositionAction = Literal["open", "close"]
ExecutionMode = Literal["cross", "mid"]


@dataclass(frozen=True)
class PaperOrder:
    order_id: str
    contract: OptionContract
    side: OrderSide
    quantity: int
    requested_price: float | None
    submitted_at: datetime
    execution_mode: ExecutionMode = "cross"
    note: str | None = None


@dataclass(frozen=True)
class PaperFill:
    fill_id: str
    order_id: str
    contract: OptionContract
    side: OrderSide
    quantity: int
    execution_price: float
    fees: float
    executed_at: datetime


@dataclass(frozen=True)
class JournalEntry:
    timestamp: datetime
    action: PositionAction
    contract_id: str
    side: OrderSide
    quantity: int
    execution_price: float
    fees: float
    note: str | None = None


@dataclass
class PaperLedger:
    positions: dict[str, Position] = field(default_factory=dict)
    journal: list[JournalEntry] = field(default_factory=list)
    realized_pnl: float = 0.0
    total_fees: float = 0.0

    def apply_fill(self, fill: PaperFill) -> None:
        existing = self.positions.get(fill.contract.contract_id)
        fill_side = "long" if fill.side == "buy" else "short"
        self.total_fees += fill.fees

        if existing is None:
            self.positions[fill.contract.contract_id] = Position(
                contract=fill.contract,
                side=fill_side,
                quantity=fill.quantity,
                average_open_price=fill.execution_price,
                opened_at=fill.executed_at,
            )
            self.journal.append(
                JournalEntry(
                    timestamp=fill.executed_at,
                    action="open",
                    contract_id=fill.contract.contract_id,
                    side=fill.side,
                    quantity=fill.quantity,
                    execution_price=fill.execution_price,
                    fees=fill.fees,
                )
            )
            return

        # minimal v1 behavior: matching opposite order closes fully or partially; same direction increases quantity.
        if existing.side == fill_side:
            total_qty = existing.quantity + fill.quantity
            avg_price = ((existing.average_open_price * existing.quantity) + (fill.execution_price * fill.quantity)) / total_qty
            self.positions[fill.contract.contract_id] = Position(
                contract=fill.contract,
                side=existing.side,
                quantity=total_qty,
                average_open_price=avg_price,
                opened_at=existing.opened_at,
                strategy_tag=existing.strategy_tag,
            )
            self.journal.append(
                JournalEntry(
                    timestamp=fill.executed_at,
                    action="open",
                    contract_id=fill.contract.contract_id,
                    side=fill.side,
                    quantity=fill.quantity,
                    execution_price=fill.execution_price,
                    fees=fill.fees,
                    note="added_to_existing_position",
                )
            )
            return

        closed_qty = min(existing.quantity, fill.quantity)
        sign = 1 if existing.side == "long" else -1
        gross_realized = (fill.execution_price - existing.average_open_price) * sign * closed_qty * fill.contract.multiplier
        self.realized_pnl += gross_realized - fill.fees

        remaining_qty = existing.quantity - fill.quantity
        self.journal.append(
            JournalEntry(
                timestamp=fill.executed_at,
                action="close",
                contract_id=fill.contract.contract_id,
                side=fill.side,
                quantity=fill.quantity,
                execution_price=fill.execution_price,
                fees=fill.fees,
                note=f"realized_pnl={gross_realized - fill.fees:.2f}",
            )
        )
        if remaining_qty > 0:
            self.positions[fill.contract.contract_id] = Position(
                contract=fill.contract,
                side=existing.side,
                quantity=remaining_qty,
                average_open_price=existing.average_open_price,
                opened_at=existing.opened_at,
                strategy_tag=existing.strategy_tag,
            )
        else:
            self.positions.pop(fill.contract.contract_id, None)
