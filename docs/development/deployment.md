# Deployment guide

Owner: platform maintainer. Purpose: distinguish verified local deployment from cloud reference.

Docker Compose is the verified deployment: validate with `docker compose config --quiet`, start with `docker compose up --build -d`, run migrations from the API image, and verify API/web/Keycloak/Prometheus/Grafana health. Pin release image digests in a controlled registry for a real environment.

Before any non-local deployment: set `TRADEOPS_ENVIRONMENT=production`; provide managed PostgreSQL/Redis; configure an HTTPS OIDC issuer/audience and redirect URIs; use workload identity/secret storage; restrict ingress/egress; encrypt storage/backups; externalize demo mutation state; configure telemetry retention; test restore/failover; set budgets and provider timeouts; and complete privacy/security review. `infra/terraform/aws` describes a possible AWS topology but is not applied by this project.
