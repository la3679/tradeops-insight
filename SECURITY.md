# Security Policy

## Supported version

Security fixes target the latest tagged release and `main`.

## Report a vulnerability

Do not open a public issue with exploit details, credentials, or personal data. Use GitHub's private vulnerability reporting for this repository. If unavailable, contact the maintainer through the non-private channel listed on the connected [GitHub profile](https://github.com/la3679) and ask for a private reporting path.

Include the affected revision, impact, reproduction, and suggested mitigation. Do not test against systems or data outside this repository's local synthetic environment.

## Boundaries

This demo cannot execute trades. Local credentials are intentionally labelled and must never be reused. Production mode requires OIDC validation and reviewed secret management. See [docs/security/architecture.md](docs/security/architecture.md).
