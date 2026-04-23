# Provider Adapter Draft

## Goal
Support stable options market-data providers without leaking provider-specific payloads into the portfolio engine.

## Design principle
The engine core must depend on a small normalized interface. Provider adapters translate external API responses into internal domain objects.

## Required adapter methods
- `get_underlying_quote(symbol)`
- `get_expirations(symbol)`
- `get_option_chain(symbol, expiry)`
- `search_contract(underlying, expiry, strike, right)`
- `get_option_quote(contract_id)`
- `get_option_quotes(contract_ids)`

## Normalized outputs
### Underlying quote
- symbol
- bid
- ask
- last
- mark
- timestamp
- source

### Option contract
- contract_id
- underlying
- expiry
- strike
- right
- multiplier
- style
- currency
- source_symbol

### Option quote
- contract_id
- bid
- ask
- last
- mark
- iv
- delta
- gamma
- theta
- vega
- rho
- open_interest
- volume
- timestamp
- source

## Error handling requirements
- distinguish `not_found`, `stale_quote`, `rate_limit`, `provider_error`
- preserve source timestamps
- surface missing greeks explicitly instead of silently inventing them

## Future-proofing
Adapters should support:
- multiple providers
- primary + fallback mode
- recorded fixtures for test replay

## Initial recommendation
Start with one stable provider, but implement the interface as if a second provider will be added within the next month.
