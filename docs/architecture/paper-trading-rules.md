# Paper Trading Simplification Rules

## Goal
Create a first useful simulation layer without pretending to be a full exchange simulator.

## Supported v1 actions
- open position
- close position
- partial close
- roll position (modeled as close + open)

## Execution assumptions
### Default close/open rules
- buy executes at ask in `cross` mode
- sell executes at bid in `cross` mode
- `mid` mode allowed for sensitivity analysis, not default realism

### Fees
- fixed fee per contract supported from day one
- fee schedule must be configurable

### Assignment / exercise
- v1 handles expiry outcome only
- ITM options at expiry may be converted using a simplified exercise/assignment rule
- no early-assignment realism in v1

### Slippage
- v1 may apply configurable slippage basis points or absolute amount
- if slippage applied, it must appear in the journal

## Journal requirements
Each simulated trade event must record:
- timestamp
- action type
- contract
- side
- quantity
- assumed execution basis
- execution price
- fees
- notes

## Why this simplification is acceptable
The first objective is decision support for DQ, not exchange-grade microstructure simulation. We need honest assumptions, not fake realism.
