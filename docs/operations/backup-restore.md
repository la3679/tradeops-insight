# Backup and restore guide

Owner: data/platform maintainer. Purpose: define recoverability for a future durable deployment.

Authoritative backup scope is PostgreSQL, migration/version metadata, provenance manifests, and versioned retrieval artifacts. Redis, caches, and the current in-memory demo state are not authoritative. Encrypt backups, restrict restore roles, record checksums, and test point-in-time recovery on an isolated environment.

Local exercise: stop mutation traffic, run `pg_dump` from the PostgreSQL container to an explicitly chosen protected path, record image/schema revision and SHA-256, restore into a new empty database, apply migrations, run repository/evaluation checks, and reconcile outbox sequences before reopening. The project does not ship or retain user backups.
