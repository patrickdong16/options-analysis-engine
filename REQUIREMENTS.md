# REQUIREMENTS.md — Options Analysis Engine

## Project identity
- Name: options-analysis-engine
- Goal: Build a public, API-backed options analysis engine for US equity options with a skill-friendly interface for real-time portfolio analysis and paper trading.
- Owner: DQ
- Initial mode: public GitHub repo + documentation-first kickoff

## Why this project exists
DQ wants a durable system rather than a one-off skill so he can:
- connect a stable options API
- inspect real-time or near-real-time multi-leg option portfolios
- compute close-out P&L correctly using bid/ask logic
- analyze portfolio Greeks and scenario risk
- support simulated trading and review workflows
- expose the capability through Pepper later as a natural-language skill/command layer

## Primary users
- DQ as primary portfolio analyst / decision-maker
- Pepper as system operator and analysis interface

## Scope for phase 1 (documentation + architecture)
This first phase must produce the initial project foundation only:
1. Public GitHub repository created
2. Core kickoff documents completed:
   - REQUIREMENTS.md
   - TDD.md
   - TESTING.md
3. Initial project card created
4. README with project thesis and MVP scope
5. GitHub sync complete

## MVP product requirements
The first buildable version must support:
1. Option portfolio input
   - define multi-leg positions manually
   - support underlying, expiry, strike, right, quantity, multiplier, side
2. Market data ingestion
   - provider adapter layer for stable options API
   - fetch underlying quote and option quotes/chains
   - normalize bid/ask/last/mark/iv/greeks where available
3. Portfolio valuation
   - close-out valuation using long->bid and short->ask
   - mark-to-mid valuation
   - realized/unrealized P&L tracking
   - per-leg and portfolio-level aggregation
4. Risk analysis
   - delta, gamma, theta, vega, rho at leg and portfolio level
   - close-out attribution by leg
5. Scenario analysis
   - spot shocks (+/-5%, +/-10%, +/-20%)
   - IV shocks (+/-5 pts, +/-10 pts)
   - time shocks (+1d, +7d)
6. Paper trading support
   - simulated open/close/roll actions
   - journal of positions, orders, fills, and cash/premium ledger
7. Interface
   - CLI first
   - skill/chat interface later

## Non-goals for early phases
- auto live trading
- high-frequency dashboarding
- sophisticated execution simulation
- broker account syncing in v1
- full early-assignment realism in v1
- advanced volatility surface research before basic portfolio engine is stable

## Success criteria
The project is successful when:
1. Repo exists publicly on GitHub
2. Core docs clearly define build contract
3. There is a stable architecture for:
   - provider adapters
   - contract/quote/position modeling
   - valuation
   - greeks
   - scenarios
   - paper trading
4. DQ can later hand Pepper a multi-leg options portfolio and get trustworthy close-out P&L and scenario analysis

## Product principles
- Correctness over cleverness
- Portfolio-first, not single-leg-first
- Bid/ask close-out logic must be explicit
- Provider abstraction from day one
- CLI/API/skill are interfaces; portfolio engine is the core
- Simulated trading should begin with simple, explicit assumptions before realism expansion
