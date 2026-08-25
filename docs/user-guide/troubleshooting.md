# Troubleshooting

Owner: support maintainer. Purpose: resolve common local-demo problems.

| Symptom             | Check                                 | Resolution                                                               |
| ------------------- | ------------------------------------- | ------------------------------------------------------------------------ |
| web/API unavailable | `docker compose ps`                   | run `docker compose up --build -d`; inspect service logs                 |
| API not ready       | `/api/v1/health/ready` and PostgreSQL | wait for health, inspect migration/database logs                         |
| 401/403             | environment and selected role         | use labelled local role; production requires valid OIDC token            |
| 409 conflict        | exception version                     | refresh and review current state; do not retry with a fabricated version |
| 429 rate limited    | request burst                         | wait and reduce frequency; the demo has a deliberately low bound         |
| workflow escalates  | evidence/citation panel               | add reviewed evidence in a future dataset version; never bypass the gate |
| no live update      | browser network/WebSocket             | use polling refresh; inspect `/api/v1/events`                            |
| state disappeared   | API restart                           | expected for web-facing demo mutations; rerun the deterministic journey  |
| port collision      | ports 3000/8000/8080/9090/3001        | stop the conflicting process or override reviewed port mappings          |

Sanitize tokens, environment values, and bodies before sharing logs.
