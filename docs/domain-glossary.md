# Domain glossary

## Synthetic trade

An immutable, versioned snapshot of invented trade facts. Trade identifiers use the `TRD-DEMO-000000` format and instrument identifiers use `INST-DEMO-000000`; neither represents a real security or transaction. Notional values use decimal arithmetic and observation timestamps are UTC.

## Exception finding

The structured output of a deterministic rule. A finding records the trade, rule version, severity, review route, explanation, and suggested actions. It is evidence for a workflow, not permission to mutate synthetic state.

## Settlement-date mismatch

A finding produced when the observed settlement date differs from the date calculated by an explicit settlement policy. Version 1 uses a configurable business-day lag, skips weekends, and skips only holidays supplied to the policy. It does not imply a universal market convention.

## Review correction

A route for a nearby mismatch where a reviewer can compare the proposed date with synthetic evidence. The rule does not apply the correction.

## Escalation

A route for a settlement date before the trade date or a mismatch beyond the configured calendar-day threshold. Escalation explicitly prohibits automatic correction.
