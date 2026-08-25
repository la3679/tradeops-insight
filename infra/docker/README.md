# Local infrastructure

- **Owner:** Platform maintainers
- **Purpose:** Run rebuildable local PostgreSQL and Redis dependencies without any paid service.

## Start and initialize

```bash
make infra-up
make migrate
```

PostgreSQL is authoritative. Redis is limited to delivery, locks, fan-out, rate controls, and caches. Both ports bind to loopback only. The committed credentials are conspicuously local demo values and must be replaced in any shared environment.

## Stop

```bash
make infra-down
```

This preserves named volumes. To remove volumes, use an explicit reviewed Docker Compose command; the Make target does not destroy data.

## Image choices

- PostgreSQL `18.6-alpine3.24` is the current supported stable release selected from the official image tags. PostgreSQL 18 uses `/var/lib/postgresql` as its volume target.
- Redis `8.8.2-alpine3.23` is pinned to an official image tag. Append-only persistence supports local recovery, but Redis remains non-authoritative.

Images will be reviewed by Dependabot/CI and upgraded through normal commits. Production designs pin verified digests in addition to versions.

## Current verification status

The Compose document is schema-parsed in this workspace and services have health checks, resource-bounded Redis configuration, loopback ports, named volumes, graceful shutdown, and `no-new-privileges`. Docker is not installed in the current work runtime, so container startup is explicitly not yet verified here; CI will run the migration against PostgreSQL.
