# Privacy and logging policy

Owner: security/operations maintainer. Purpose: define collection and redaction.

The repository intentionally contains no customer, employee, client, account, order, or personal trading data. Runtime fixtures and identities are synthetic; public fixture fields are minimized and attributed. Do not import real data into this demo.

Logs may contain timestamp, severity, service, route template, status, duration, request/correlation ID, synthetic subject ID, workflow ID, and bounded error code. They must not contain bearer tokens, passwords, API keys, full prompts/documents, raw request bodies, or unnecessary user attributes. Metrics use bounded labels; traces use the same redaction. Local telemetry has no promised retention. A deployment owner must define retention, access, deletion, and incident obligations before non-demo use.
