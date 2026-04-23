# TDD.md — Options Analysis Engine

## Technical thesis
Build a modular options portfolio engine with a provider abstraction layer, a portfolio/risk core, and a paper-trading ledger. The first implementation should optimize for correctness, inspectability, and extension—not for speed or UI richness.

## Architecture overview

### 1. Provider adapter layer
Purpose: isolate external market-data/API dependencies.

Core interface ideas:
- `get_underlying_quote(symbol)`
- `get_option_quote(contract_id)`
- `get_option_chain(symbol, expiry=None)`
- `get_expirations(symbol)`
- `search_contract(underlying, expiry, strike, right)`

Normalization target:
- underlying quote
- option contract metadata
- option quote snapshot
- optional provider greeks
- timestamps and source provenance

### 2. Domain model layer
Core entities:
- `Underlying`
- `OptionContract`
- `QuoteSnapshot`
- `Position`
- `Portfolio`
- `Order`
- `Fill`
- `StrategyTag`
- `ScenarioResult`

Key invariants:
- quantity and multiplier must never be implicit
- `side` and sign conventions must be explicit
- contract identity must include underlying + expiry + strike + right + multiplier/style when needed
- quotes must carry source + timestamp

### 3. Valuation engine
Functions:
- close-out valuation
- mid valuation
- realized/unrealized pnl
- leg attribution
- portfolio aggregation

Rules:
- close long at bid
- close short at ask
- mid valuation distinct from close-out valuation
- preserve original fill/open prices for P&L
- expose both per-leg and total portfolio outputs

### 4. Risk/Greeks engine
Responsibilities:
- ingest provider greeks where trusted
- fall back to model-derived greeks if required
- aggregate delta/gamma/theta/vega/rho by leg, strategy, and portfolio

Phase guidance:
- accept provider greeks first if stable API supplies them
- design fallback model interface, but do not block v1 on custom greeks library sophistication

### 5. Scenario engine
Inputs:
- current portfolio snapshot
- spot shock grid
- vol shock grid
- time-forward shock grid

Outputs:
- shocked close-out value
- shocked mid value
- greek changes
- biggest loss contributor by leg

### 6. Paper trading ledger
Responsibilities:
- record simulated orders
- transform orders into fills under explicit assumptions
- maintain position inventory
- support open, close, partial close, roll
- maintain journal for cash/premium realization

v1 simplifying assumptions:
- execution mode configurable: `cross` or `mid`
- roll = close old legs + open new legs
- assignment/exercise modeled simply at expiry only
- fixed fee model supported

### 7. Interfaces
Planned order:
1. Python package core
2. CLI commands
3. local API if useful
4. Pepper/skill integration
5. optional dashboard later

## Suggested repository layout
```text
options-analysis-engine/
  README.md
  REQUIREMENTS.md
  TDD.md
  TESTING.md
  src/options_engine/
    providers/
    domain/
    valuation/
    greeks/
    scenarios/
    paper/
    cli/
  tests/
    unit/
    integration/
    fixtures/
  docs/
    architecture/
    decisions/
```

## Recommended implementation order
### Phase 0 — kickoff/docs
- create repo
- write README + three core docs
- define project card

### Phase 1 — domain and provider abstraction
- contract and quote schemas
- provider adapter interface
- mock provider for deterministic tests

### Phase 2 — portfolio valuation
- close-out and mid valuation
- leg and total pnl
- support multi-leg strategies

### Phase 3 — scenario engine
- spot / vol / time shock grid

### Phase 4 — paper trading ledger
- orders/fills/journal/roll

### Phase 5 — Pepper interface
- command/skill wrapper for natural-language usage

## Design decisions to preserve
- provider-specific fields should not leak into the core engine
- scenario calculations should be deterministic and reproducible
- every valuation output should reveal the pricing basis used (`bid/ask`, `mid`, provider greeks, modeled greeks)
- the system should support both manual portfolio entry and later automated ingestion
