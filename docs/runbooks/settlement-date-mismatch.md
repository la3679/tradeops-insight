# Settlement-date mismatch runbook

This runbook applies only to deterministic synthetic TradeOps Copilot records.

## Detection

Rule `settlement-date-v1` calculates the expected date from the trade date and configured business-day lag. Saturdays, Sundays, and explicitly supplied holiday dates are skipped. Matching dates produce no finding.

## Severity and routing

- A mismatch at or below the configured calendar-day threshold is medium severity and routes to reviewed correction.
- A date before the trade date or beyond the threshold is high severity and routes to escalation.

## Review correction

1. Confirm that the displayed rule version and calendar inputs match the synthetic case.
2. Compare the original date and calculated date with the synthetic evidence.
3. Approve or reject a correction only through a future reviewed workflow. This rule never changes the trade.

## Escalation

1. Do not alter the synthetic trade.
2. Record why the date is anomalous and request additional synthetic evidence.
3. Escalate to the designated demo supervisor workflow when it exists.

## Current limitations

No external holiday calendar, currency convention, product convention, database, or workflow integration exists in this slice. Policies must be supplied explicitly and are deterministic offline.
