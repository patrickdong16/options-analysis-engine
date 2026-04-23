# Domain Model Draft

## Core domain entities

### Underlying
Represents the stock or ETF under analysis.
Fields:
- symbol
- name
- currency
- exchange

### OptionContract
Represents a uniquely identifiable option contract.
Fields:
- contract_id
- underlying
- expiry
- strike
- right
- multiplier
- style
- currency
- provider_symbol

### QuoteSnapshot
Represents a point-in-time market snapshot.
Fields:
- instrument_id
- bid
- ask
- last
- mark
- iv
- greeks
- open_interest
- volume
- timestamp
- source

### Position
Represents current inventory in a contract.
Fields:
- contract_id
- side
- quantity
- average_open_price
- opened_at
- strategy_tag

### Portfolio
Represents grouped positions and account-level state.
Fields:
- portfolio_id
- positions
- cash_ledger
- realized_pnl
- unrealized_pnl
- aggregated_greeks

### Order
Represents a simulated instruction.
Fields:
- order_id
- contract_id
- side
- quantity
- order_type
- requested_price
- submitted_at
- status

### Fill
Represents a simulated or actual execution event.
Fields:
- fill_id
- order_id
- contract_id
- side
- quantity
- execution_price
- fees
- executed_at

## Invariants
- quantity must always be explicit and never inferred from text
- side conventions must be normalized consistently
- multiplier must always participate in notional/pnl calculations
- quote snapshots must preserve timestamp and source provenance
- a close-out calculation must always reveal whether it used bid/ask or mid

## Suggested first strategy tags
- risk_reversal
- straddle
- vertical_spread
- covered_call
- custom
