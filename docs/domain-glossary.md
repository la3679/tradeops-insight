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
All trade, event, instrument, counterparty, and document records described here are synthetic unless a field is explicitly marked as public reference metadata.

## Exception catalogue

| Type                           | Deterministic trigger                           | Review posture                                             |
| ------------------------------ | ----------------------------------------------- | ---------------------------------------------------------- |
| Invalid counterparty LEI       | Missing or not `LEI-DEMO-000000`                | Correct a malformed value; escalate a missing identity     |
| Counterparty name mismatch     | Normalized trade and reference names differ     | Review a typo; escalate a blank legal name                 |
| Unknown or inactive entity     | LEI absent from the snapshot or inactive        | Review inactive reference state; escalate unknown identity |
| Instrument ID mismatch         | Trade and reference synthetic IDs differ        | Review a known-format mismatch; escalate unknown format    |
| Notional mismatch              | Fixed-precision delta exceeds tolerance         | Escalate material deltas                                   |
| Price outside tolerance        | Absolute price delta exceeds policy             | Escalate values over five times tolerance                  |
| Currency mismatch              | Trade and instrument currencies differ          | Escalate unsupported currencies                            |
| Settlement-date mismatch       | Date differs from versioned business-day policy | Escalate pre-trade or material date deltas                 |
| Duplicate trade/event          | Duplicate trade or event key observed           | Escalate when both collide                                 |
| Missing/contradictory document | Confirmation absent or memo contradicts fields  | Escalate missing required evidence                         |
| Stale reference data           | Snapshot exceeds freshness bound                | Escalate at more than three times the bound                |
| Unsupported/malformed trade    | Unsupported product or malformed payload        | Escalate malformed payloads                                |

Every finding is explainable, stable across replay, non-mutating, and routes to human review before any synthetic demo-state correction.
