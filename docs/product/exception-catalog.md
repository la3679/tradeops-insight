# Exception catalog

- **Owner:** Product and domain maintainers
- **Purpose:** Define the stable queue categories, deterministic evidence, and initial review posture.

| Family                           | Primary deterministic signal                                                           | Default review posture  |
| -------------------------------- | -------------------------------------------------------------------------------------- | ----------------------- |
| Missing or invalid LEI           | absent value, invalid shape, or failed check digits                                    | High risk; review       |
| Legal-name mismatch              | normalized input matches neither legal name nor approved alias                         | Medium risk; review     |
| Unknown or inactive entity       | valid LEI absent from snapshot, or entity status inactive                              | High/critical; escalate |
| Instrument mismatch              | instrument absent or product conflicts with reference                                  | High; review            |
| Quantity or notional mismatch    | structured values differ from the comparison version beyond exact configured precision | High; review            |
| Price-tolerance breach           | absolute price variance exceeds versioned tolerance                                    | Medium/high; review     |
| Currency mismatch                | malformed currency or value differs from instrument/reference version                  | High; review            |
| Settlement-date mismatch         | supplied date differs from deterministic business-day calculation                      | Medium/high; review     |
| Duplicate trade or event         | event ID repeated or canonical trade fingerprint duplicated                            | Medium/high; review     |
| Document or memo issue           | required confirmation missing or extracted memo facts contradict the trade             | Medium/high; review     |
| Stale reference data             | required reference timestamp exceeds policy age                                        | Medium; refresh/review  |
| Unsupported or malformed payload | product outside allowlist or required business field unusable                          | High; reject/escalate   |

## Common rule contract

Every detector is side-effect free and returns a typed exception with severity, risk, human-readable explanation, suggested actions, bounded evidence facts, and a deterministic review requirement. A detector never applies a correction. Resolution policy and authorization are separate stages.

## Scenario standard

Each family receives at least one resolvable fixture and one escalation fixture. A resolvable fixture has adequate versioned evidence for a proposed synthetic correction; an escalation fixture is unsupported, inactive, contradictory, stale beyond recovery, or otherwise lacks sufficient evidence. Both remain synthetic.
