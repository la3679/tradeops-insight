# ADR 0006: Transactional outbox and delivery

Status: accepted. Persist domain state and an outbox record in one transaction, then deliver asynchronously with stable event IDs and aggregate sequences. Consumers reject duplicates/stale events and defer gaps. At-least-once transport is safer and more demonstrable than pretending distributed exactly-once delivery.
