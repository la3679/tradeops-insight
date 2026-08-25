# Security policy

## Supported versions

Until the first tagged release, only the current default branch is supported. After release, the latest minor release line will receive security fixes unless release notes state otherwise.

## Reporting a vulnerability

Do not open a public issue for suspected vulnerabilities, exposed credentials, private data, or exploitable agent behavior. Use GitHub's private vulnerability-reporting feature when it is enabled. If it is unavailable, use the private contact method on the maintainer's connected GitHub profile and include only the minimum information necessary to coordinate securely.

A useful report includes affected version/commit, prerequisites, reproducible steps, impact, and a safe proof of concept. Do not access data that is not yours, persist beyond what is necessary to demonstrate impact, degrade service, or test against third-party systems without authorization.

## Response targets

These are project-maintenance targets, not service-level guarantees:

- Acknowledge a complete report within five business days.
- Triage severity and coordinate next steps within ten business days.
- Publish remediation and credit with the reporter's consent after a fix is available.

## Security boundary

TradeOps Copilot processes synthetic demo state only. Nevertheless, reports involving authentication, authorization, prompt injection, unsafe tool invocation, SSRF, secret exposure, dependency compromise, audit integrity, approval bypass, or cross-role data leakage are considered security relevant.
