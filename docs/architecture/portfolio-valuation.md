# Portfolio Valuation Spec

## Objectives
Define trustworthy and explainable portfolio valuation outputs.

## Valuation modes
### 1. Close-out valuation
Purpose: estimate what the portfolio is worth if closed now.
Rules:
- long option closes at bid
- short option closes at ask
- fees may be included or excluded, but basis must be labeled

### 2. Mid valuation
Purpose: neutral mark for internal tracking/comparison.
Rules:
- option value = (bid + ask) / 2 when both exist
- if one side missing, mark output as approximated

## Required outputs
Per leg:
- contract identity
- side
- quantity
- multiplier
- entry price
- current close-out price
- current mid price
- unrealized pnl (close-out)
- unrealized pnl (mid)
- warning flags

Portfolio level:
- total close-out value
- total mid value
- total unrealized pnl (close-out)
- total unrealized pnl (mid)
- total greek exposures
- valuation timestamp
- quote freshness summary

## Warning conditions
- stale quote
- missing bid/ask
- approximated mark
- provider greeks missing
- contract not found

## Attribution requirements
The portfolio report must reveal:
- largest pnl contributor
- largest downside contributor under scenario
- positions with weakest quote quality

## Example rule
A 1x2 risk reversal must display each leg separately before showing the grouped strategy summary so that close-out logic remains auditable.
