# Architecture overview

Owner: platform maintainer. Purpose: explain runtime boundaries and trust flow.

```mermaid
flowchart TB
  subgraph Browser[Untrusted browser]
    UI[React / TanStack Start]
  end
  subgraph App[Application trust zone]
    API[FastAPI API]
    DOM[Domain + application]
    GRAPH[LangGraph]
    RAG[FAISS retrieval]
    WORKER[Celery worker]
  end
  subgraph Data[Local data zone]
    PG[(PostgreSQL)]
    REDIS[(Redis)]
  end
  IDP[Keycloak / external OIDC] -->|signed JWT| API
  UI -->|validated REST / WS| API
  API --> DOM
  DOM --> GRAPH --> RAG
  DOM --> PG
  API --> REDIS --> WORKER --> PG
```

```mermaid
sequenceDiagram
  actor A as Analyst
  actor R as Reviewer
  participant UI as Web
  participant API as API
  participant G as LangGraph
  participant DB as State/Audit
  A->>UI: Open exception
  UI->>API: POST workflow + idempotency key
  API->>G: Invoke typed state
  G->>G: Validate, reconcile, retrieve, propose
  G-->>API: Interrupt for review
  API->>DB: Record trace/audit
  R->>API: Approval + expected version
  API->>G: Resume decision
  G->>DB: Allowlisted demo mutation + audit
  API-->>UI: Final reviewed state
```

```mermaid
erDiagram
  TRADE ||--o{ TRADE_EVENT : has
  TRADE ||--o{ EXCEPTION : raises
  EXCEPTION ||--o{ WORKFLOW : investigated_by
  WORKFLOW ||--o{ APPROVAL : reviewed_by
  WORKFLOW ||--o{ AUDIT_EVENT : emits
  KNOWLEDGE_DOCUMENT ||--o{ KNOWLEDGE_CHUNK : split_into
  SOURCE ||--o{ PROVENANCE_RECORD : attests
  EVALUATION_RUN ||--o{ EVALUATION_RESULT : contains
  OUTBOX_EVENT }o--|| AUDIT_EVENT : publishes
```

Components point inward: frameworks/adapters → application ports → domain. The browser owns presentation only. Authorization, validation, calculations, workflow policy, and mutation stay server-side. Public content is untrusted data; it cannot issue instructions or authorize tools. Model output is structured advisory data and cannot bypass deterministic gates or approval.

Failure handling: invalid input is rejected; duplicate commands replay safely; version conflicts return conflict; missing/malicious evidence escalates; provider errors fall back to mock or escalation; outbox gaps defer; WebSocket clients use polling fallback; observability failure never changes domain results.
