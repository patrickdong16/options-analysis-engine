# TESTING.md — Options Analysis Engine

## Testing philosophy
This project must earn trust before it earns features.
The first version should prove that valuation and scenario outputs are correct, explainable, and reproducible.

## Verification gates for documentation kickoff
Before calling the kickoff complete:
1. Repo exists locally
2. Repo exists publicly on GitHub
3. Core documents exist and are internally consistent:
   - REQUIREMENTS.md
   - TDD.md
   - TESTING.md
   - README.md
4. Project card exists and points to the repo
5. GitHub remote is configured
6. Initial commit is pushed

## Verification gates for MVP implementation
### 1. Domain model tests
- contract identity generation
- quantity/multiplier handling
- side/sign normalization
- quote timestamp/source preservation

### 2. Valuation tests
- long close uses bid
- short close uses ask
- mid valuation uses midpoint
- per-leg unrealized pnl correct
- multi-leg total equals leg sum
- different multipliers produce correct notional pnl

### 3. Scenario tests
- spot up/down shocks change outputs deterministically
- IV shocks alter valuation in expected direction for calls/puts where applicable
- time-forward shocks reduce long-option value under otherwise fixed assumptions
- scenario report preserves base snapshot provenance

### 4. Paper trading tests
- opening position creates fill + position inventory
- partial close adjusts remaining inventory correctly
- roll creates close/open entries correctly
- realized pnl journal updates correctly
- fee handling is reflected in pnl

### 5. Provider adapter tests
- provider response normalization
- missing-field handling
- stale quote rejection or surfacing
- source provenance recorded consistently

## Initial test strategy
### Unit tests first
Focus on:
- valuation math
n- scenario logic
- sign conventions
- ledger transitions

### Integration tests second
Use:
- mock provider
- recorded quote fixtures
- sample multi-leg portfolios (risk reversal, straddle, vertical, covered call)

### Regression fixtures to include early
- 1x2 risk reversal close-out example
- deep ITM call + short puts
- mixed-expiry portfolio
- zero-bid / wide-spread edge case
- stale quote edge case

## Minimum acceptance test set before v1 use
1. Input a multi-leg portfolio manually
2. Pull normalized quotes from provider/mock provider
3. Produce:
   - close-out value
   - mid value
   - per-leg pnl
   - portfolio greeks
   - scenario table
4. Run a simulated open then close
5. Confirm journal and pnl reconcile

## Manual QA checklist
- numbers are labeled by basis (`close-out` vs `mid`)
- leg counts and multipliers are displayed clearly
- outputs show timestamps/source
- warnings appear when quotes are stale, missing, or approximated
- scenario outputs are understandable by DQ without code inspection

## Done definition for kickoff phase
Kickoff phase is done only when:
- docs are written
- repo is public
- files are pushed
- project card is present
- DQ has a clean written architecture starting point for the build phase
