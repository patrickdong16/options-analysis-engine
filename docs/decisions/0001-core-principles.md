# ADR 0001 — Core Principles

## Status
Accepted

## Decision
The project will use a system-kernel-first approach:
- portfolio engine first
- skill/chat interface later
- provider abstraction from day one
- close-out logic explicit and auditable
- paper trading simplified before realism expansion

## Rationale
DQ's real need is durable options analysis capability, not a one-off script or a thin skill wrapper.

## Consequences
- extra upfront design discipline
- easier provider replacement later
- cleaner path to chat, CLI, and dashboard interfaces
