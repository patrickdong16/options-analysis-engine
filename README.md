# Options Analysis Engine

Public project to build an API-backed options portfolio analysis and paper-trading engine for US equity options.

## Why
Most lightweight options tools stop at single-leg pricing or thin dashboards. This project is intended to support real multi-leg portfolio analysis with explicit close-out logic, portfolio Greeks, scenario analysis, and paper-trading workflows.

## What it should become
A durable engine that can:
- ingest stable options market data from a provider adapter
- normalize contract and quote data
- compute close-out and mid portfolio valuations
- aggregate Greeks across multi-leg portfolios
- run scenario analysis for spot, vol, and time shocks
- support simulated trading journals and roll workflows
- later expose these capabilities through Pepper/skill-style interfaces

## MVP focus
- manual portfolio input
- provider adapter abstraction
- close-out valuation (`long -> bid`, `short -> ask`)
- mark-to-mid valuation
- portfolio Greeks
- scenario engine
- paper-trading journal
- CLI-first interaction

## Core documents
- `REQUIREMENTS.md`
- `TDD.md`
- `TESTING.md`

## Status
Kickoff / architecture phase.
