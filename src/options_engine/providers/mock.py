from __future__ import annotations

from typing import Sequence

from options_engine.domain.models import OptionContract, QuoteSnapshot
from options_engine.providers.base import OptionsDataProvider


class MockOptionsDataProvider(OptionsDataProvider):
    def __init__(self, contracts: dict[str, OptionContract], quotes: dict[str, QuoteSnapshot]):
        self.contracts = contracts
        self.quotes = quotes

    def get_option_quote(self, contract_id: str) -> QuoteSnapshot:
        return self.quotes[contract_id]

    def get_option_quotes(self, contract_ids: Sequence[str]) -> list[QuoteSnapshot]:
        return [self.quotes[contract_id] for contract_id in contract_ids]

    def search_contract(self, underlying: str, expiry: str, strike: float, right: str) -> OptionContract:
        for contract in self.contracts.values():
            if (
                contract.underlying == underlying
                and contract.expiry.isoformat() == expiry
                and contract.strike == strike
                and contract.right == right
            ):
                return contract
        raise KeyError(f"No contract found for {underlying} {expiry} {strike} {right}")
