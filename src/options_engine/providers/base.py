from __future__ import annotations

from typing import Protocol, Sequence

from options_engine.domain.models import OptionContract, QuoteSnapshot


class OptionsDataProvider(Protocol):
    def get_option_quote(self, contract_id: str) -> QuoteSnapshot: ...

    def get_option_quotes(self, contract_ids: Sequence[str]) -> list[QuoteSnapshot]: ...

    def search_contract(
        self, underlying: str, expiry: str, strike: float, right: str
    ) -> OptionContract: ...
