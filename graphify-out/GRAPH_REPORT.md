# Graph Report - tradeops-insight  (2026-08-24)

## Corpus Check
- 258 files · ~65,704 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1559 nodes · 2841 edges · 184 communities (85 shown, 99 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 181 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1c94de90`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- routeTree.gen.ts
- cn
- sidebar.tsx
- devDependencies
- compilerOptions
- index.tsx
- pagination.tsx
- utils.ts
- __root.tsx
- server.ts
- components.json
- scripts
- command.tsx
- menubar.tsx
- form.tsx
- config.py
- dependencies
- chart.tsx
- models.py
- Domain glossary
- Architecture Baseline
- Settlement-date mismatch runbook
- pipeline.py
- What You Must Do When Invoked
- Principal
- graphify reference: extra exports and benchmark
- validate_manifest
- carousel.tsx
- navigation-menu.tsx
- sonner.tsx
- table.tsx
- breadcrumb.tsx
- date-fns
- embla-carousel-react
- @hookform/resolvers
- input-otp
- @radix-ui/react-accordion
- @radix-ui/react-alert-dialog
- @radix-ui/react-aspect-ratio
- @radix-ui/react-avatar
- @radix-ui/react-collapsible
- @radix-ui/react-context-menu
- @radix-ui/react-dialog
- @radix-ui/react-hover-card
- @radix-ui/react-label
- @radix-ui/react-menubar
- @radix-ui/react-navigation-menu
- @radix-ui/react-popover
- @radix-ui/react-radio-group
- @radix-ui/react-scroll-area
- @radix-ui/react-select
- @radix-ui/react-separator
- @radix-ui/react-slider
- @radix-ui/react-slot
- @radix-ui/react-switch
- @radix-ui/react-tabs
- @radix-ui/react-toggle
- @radix-ui/react-toggle-group
- @radix-ui/react-tooltip
- react-day-picker
- react-dom
- react-hook-form
- react-resizable-panels
- recharts
- tailwind-merge
- tailwindcss
- @tailwindcss/vite
- @tanstack/react-query
- @tanstack/react-router
- @tanstack/react-start
- @tanstack/router-plugin
- tw-animate-css
- vaul
- vite-tsconfig-paths
- zod
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- docs/README.md
- ADR 0002: Python runtime and durable task queue boundary
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- Routes
- extraction-spec.md
- alert.tsx
- TradeOps backend foundation
- main
- adapters/__init__.py
- api/__init__.py
- routes/__init__.py
- application/__init__.py
- SettlementDatePolicy
- configure_observability
- build_workflow
- ports/__init__.py
- worker/__init__.py
- tradeops-copilot-backend
- TradeOps Copilot Product Brief
- Project state
- CONTRIBUTING.md
- ADR 0001: Modular Monolith with a Background Worker
- TradeOps Copilot
- README.md
- manifest.json
- @radix-ui/react-dropdown-menu
- clsx
- ADR 0003: Relational persistence and idempotency
- ADR 0004: Offline retrieval and explicit agent graph
- cmdk
- exception-triage.md
- tools.py
- exceptions_.$exceptionId.tsx
- ReconciliationPolicy
- Panel.tsx
- ReconciliationInput
- api/app.py
- Settings
- EventDeliveryTracker
- Design System Master File
- exceptions.tsx
- build_golden_dataset
- StatusBadge.tsx
- health.py
- SyntheticTrade
- session.py
- checkpoints.py
- test_api_security.py
- test_api_operations.py
- test_api_platform.py
- TokenDecoder
- CHANGELOG.md
- Documentation index
- pull_request_template.md
- Security Policy
- ROADMAP.md
- DATA_LICENSES.md
- 0005-oidc-provider-strategy.md
- 0006-transactional-outbox.md
- 0007-human-control-policy.md
- 0008-model-provider-abstraction.md
- 0009-observability-stack.md
- 0010-public-synthetic-data.md
- eslint
- eslint-config-prettier
- @eslint/js
- eslint-plugin-prettier
- eslint-plugin-react-hooks
- globals
- aws/README.md
- jest-axe
- @lovable.dev/vite-tanstack-config
- nitro
- @playwright/test
- prettier
- @testing-library/jest-dom
- @testing-library/react
- @testing-library/user-event
- @types/jest-axe
- @types/node
- @types/react
- @types/react-dom
- typescript
- typescript-eslint
- vite
- @vitejs/plugin-react
- vitest
- @vitest/coverage-v8
- k6-import.js
- k6-smoke.js
- k6-websocket.js
- check_docs.py

## God Nodes (most connected - your core abstractions)
1. `cn()` - 231 edges
2. `Settings` - 42 edges
3. `Principal` - 38 edges
4. `SettlementDatePolicy` - 38 edges
5. `DemoOperationsService` - 37 edges
6. `ReconciliationPolicy` - 29 edges
7. `Base` - 28 edges
8. `scripts` - 27 edges
9. `IdentityMixin` - 24 edges
10. `Role` - 23 edges

## Surprising Connections (you probably didn't know these)
- `SeedResult` --uses--> `ReconciliationPolicy`  [INFERRED]
  backend/src/tradeops/adapters/persistence/repository.py → backend/src/tradeops/domain/reconciliation.py
- `SeedResult` --uses--> `SyntheticDataset`  [INFERRED]
  backend/src/tradeops/adapters/persistence/repository.py → backend/src/tradeops/domain/synthetic.py
- `ExceptionSummary` --uses--> `ReconciliationPolicy`  [INFERRED]
  backend/src/tradeops/adapters/persistence/repository.py → backend/src/tradeops/domain/reconciliation.py
- `ExceptionSummary` --uses--> `SyntheticDataset`  [INFERRED]
  backend/src/tradeops/adapters/persistence/repository.py → backend/src/tradeops/domain/synthetic.py
- `TradeOpsRepository` --uses--> `ReconciliationPolicy`  [INFERRED]
  backend/src/tradeops/adapters/persistence/repository.py → backend/src/tradeops/domain/reconciliation.py

## Import Cycles
- None detected.

## Communities (184 total, 99 thin omitted)

### Community 0 - "routeTree.gen.ts"
Cohesion: 0.09
Nodes (28): getRouter(), Route, Route, Route, Route, Route, Route, Route (+20 more)

### Community 1 - "cn"
Cohesion: 0.06
Nodes (53): AccordionContent, AccordionItem, AccordionTrigger, Avatar, AvatarFallback, AvatarImage, Card, CardContent (+45 more)

### Community 2 - "sidebar.tsx"
Cohesion: 0.06
Nodes (40): Input, Separator, SheetContent, SheetContentProps, SheetDescription, SheetFooter(), SheetHeader(), SheetOverlay (+32 more)

### Community 3 - "devDependencies"
Cohesion: 0.29
Nodes (7): @axe-core/playwright, eslint-plugin-react-refresh, jsdom, devDependencies, @axe-core/playwright, eslint-plugin-react-refresh, jsdom

### Community 4 - "compilerOptions"
Cohesion: 0.06
Nodes (32): DOM, DOM.Iterable, ES2022, eslint.config.js, src/**/*.ts, src/**/*.tsx, vite/client, vite.config.ts (+24 more)

### Community 5 - "index.tsx"
Cohesion: 0.25
Nodes (12): CategoryBars(), ExceptionTable(), QueueLaneList(), CategoryBreakdown, dataAsOf, QueueLane, queueLanes, recentExceptions (+4 more)

### Community 6 - "pagination.tsx"
Cohesion: 0.12
Nodes (21): AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter(), AlertDialogHeader(), AlertDialogOverlay, AlertDialogTitle (+13 more)

### Community 7 - "utils.ts"
Cohesion: 0.08
Nodes (19): Badge(), BadgeProps, badgeVariants, Checkbox, HoverCardContent, InputOTP, InputOTPGroup, InputOTPSeparator (+11 more)

### Community 8 - "__root.tsx"
Cohesion: 0.12
Nodes (13): AppFooter(), AppShell(), SideNav(), SideNavProps, StatusBar(), DemoRoleProvider(), LovableErrorOptions, LovableEvents (+5 more)

### Community 9 - "server.ts"
Cohesion: 0.16
Nodes (13): consumeLastCapturedError(), describeError(), describeStatus(), originalConsoleError, safeStringify(), renderErrorPage(), fetch(), getServerEntry() (+5 more)

### Community 10 - "components.json"
Cohesion: 0.11
Nodes (18): aliases, components, hooks, lib, ui, utils, iconLibrary, registries (+10 more)

### Community 11 - "scripts"
Cohesion: 0.06
Nodes (33): name, overrides, rolldown, private, scripts, backend:format:check, backend:lint, backend:sync (+25 more)

### Community 12 - "command.tsx"
Cohesion: 0.12
Nodes (14): Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList, CommandSeparator, CommandShortcut() (+6 more)

### Community 13 - "menubar.tsx"
Cohesion: 0.12
Nodes (11): Menubar, MenubarCheckboxItem, MenubarContent, MenubarItem, MenubarLabel, MenubarRadioItem, MenubarSeparator, MenubarShortcut() (+3 more)

### Community 14 - "form.tsx"
Cohesion: 0.19
Nodes (12): FormControl, FormDescription, FormFieldContext, FormFieldContextValue, FormItem, FormItemContext, FormItemContextValue, FormLabel (+4 more)

### Community 15 - "config.py"
Cohesion: 0.20
Nodes (10): get_settings(), Validated process configuration with safe local defaults., Build and cache immutable process settings., create_worker(), Celery application factory with side-effect-free configuration., Configure a worker without connecting to its broker., main(), Start the explicitly configured worker. (+2 more)

### Community 16 - "dependencies"
Cohesion: 0.15
Nodes (13): class-variance-authority, lucide-react, dependencies, class-variance-authority, lucide-react, @radix-ui/react-checkbox, @radix-ui/react-progress, react (+5 more)

### Community 17 - "chart.tsx"
Cohesion: 0.25
Nodes (9): ChartConfig, ChartContainer, ChartContext, ChartContextProps, ChartLegendContent, ChartTooltipContent, getPayloadConfigFromPayload(), THEMES (+1 more)

### Community 18 - "models.py"
Cohesion: 0.09
Nodes (47): SQLAlchemy persistence adapter., ApprovalRecord, AuditEventRecord, Base, CounterpartyRecord, DataSourceSyncRunRecord, DocumentChunkRecord, DocumentRecord (+39 more)

### Community 19 - "Domain glossary"
Cohesion: 0.25
Nodes (7): Domain glossary, Escalation, Exception catalogue, Exception finding, Review correction, Settlement-date mismatch, Synthetic trade

### Community 20 - "Architecture Baseline"
Cohesion: 0.22
Nodes (8): Architecture Baseline, Dependency direction, Evolution criteria, Initial module boundaries, Investigation workflow, Ownership boundaries, System shape, Workflow safety model

### Community 21 - "Settlement-date mismatch runbook"
Cohesion: 0.29
Nodes (6): Current limitations, Detection, Escalation, Review correction, Settlement-date mismatch runbook, Severity and routing

### Community 22 - "pipeline.py"
Cohesion: 0.09
Nodes (27): Safe, offline-capable retrieval primitives., chunk_document(), Citation, FaissKnowledgeIndex, generate_synthetic_policy_documents(), HashEmbeddingProvider, KnowledgeChunk, KnowledgeDocument (+19 more)

### Community 23 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 24 - "Principal"
Cohesion: 0.06
Nodes (104): ANALYST, AUDITOR, ApprovalRequest, approve_workflow(), _audit(), audit_events(), AuditResponse, _exception() (+96 more)

### Community 25 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 26 - "validate_manifest"
Cohesion: 0.19
Nodes (15): _entry(), ProvenanceEntry, ProvenanceError, Path, ValueError, Offline provenance-manifest validation for committed public-data fixtures., Raised when a manifest is malformed or a fixture hash no longer matches., Validate required metadata, repository-contained paths, and SHA-256 hashes. (+7 more)

### Community 27 - "carousel.tsx"
Cohesion: 0.19
Nodes (13): Carousel, CarouselApi, CarouselContent, CarouselContext, CarouselContextProps, CarouselItem, CarouselNext, CarouselOptions (+5 more)

### Community 28 - "navigation-menu.tsx"
Cohesion: 0.29
Nodes (7): NavigationMenu, NavigationMenuContent, NavigationMenuIndicator, NavigationMenuList, NavigationMenuTrigger, navigationMenuTriggerStyle, NavigationMenuViewport

### Community 30 - "table.tsx"
Cohesion: 0.22
Nodes (8): Table, TableBody, TableCaption, TableCell, TableFooter, TableHead, TableHeader, TableRow

### Community 31 - "breadcrumb.tsx"
Cohesion: 0.25
Nodes (7): Breadcrumb, BreadcrumbEllipsis(), BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator()

### Community 80 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 81 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 82 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 83 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 84 - "docs/README.md"
Cohesion: 0.06
Nodes (17): Architecture decisions, API guide, RAG ingestion and retrieval design, Scaling and evolution, Data dictionary, Synthetic data methodology, Release process, Developer setup (+9 more)

### Community 85 - "ADR 0002: Python runtime and durable task queue boundary"
Cohesion: 0.40
Nodes (4): ADR 0002: Python runtime and durable task queue boundary, Consequences, Context, Decision

### Community 92 - "alert.tsx"
Cohesion: 0.50
Nodes (4): Alert, AlertDescription, AlertTitle, alertVariants

### Community 99 - "SettlementDatePolicy"
Cohesion: 0.21
Nodes (17): Independently testable deterministic rule families., evaluate_settlement_date(), Versioned convention supplied to the settlement-date rule., Return a typed mismatch finding, or ``None`` when the dates agree., SettlementDatePolicy, parametrize, test_explicit_holiday_is_not_a_business_day(), test_finding_id_is_deterministic_and_version_sensitive() (+9 more)

### Community 100 - "configure_observability"
Cohesion: 0.14
Nodes (11): Safe telemetry composition., ApiMetrics, Low-cardinality Prometheus metrics for one API process., Own an isolated registry so application factories remain test-safe., configure_observability(), FastAPI, Structured logging and OpenTelemetry setup without recording domain payloads., Instrument non-test API processes and export traces through the local collector. (+3 more)

### Community 101 - "build_workflow"
Cohesion: 0.07
Nodes (31): build_workflow(), CompiledStateGraph, Explicit typed LangGraph workflow with mandatory human review before mutation., Compile the reviewed thirteen-node graph with replayable defaults., _step(), Typed workflow and provider composition., Classification, MockModelProvider (+23 more)

### Community 106 - "TradeOps Copilot Product Brief"
Cohesion: 0.25
Nodes (7): Data policy, First release journey, Non-goals, Purpose, Release principle, TradeOps Copilot Product Brief, Users and outcomes

### Community 107 - "Project state"
Cohesion: 0.33
Nodes (5): Final actions, Project state, Release checkpoint, Safety boundaries and limitations, Verification evidence

### Community 108 - "CONTRIBUTING.md"
Cohesion: 0.20
Nodes (7): Coding rules, graphify, Ownership boundaries, Review requirements, TradeOps Copilot — agent guidelines, Code of Conduct, Contributing

### Community 109 - "ADR 0001: Modular Monolith with a Background Worker"
Cohesion: 0.33
Nodes (5): ADR 0001: Modular Monolith with a Background Worker, Consequences, Context, Decision, Revisit when

### Community 110 - "TradeOps Copilot"
Cohesion: 0.25
Nodes (8): Architecture, Primary journey, Providers and data, Quick start, Repository and limits, TradeOps Copilot, Verification, What it demonstrates

### Community 111 - "README.md"
Cohesion: 0.09
Nodes (11): Demonstration script, Architecture overview, Data source and provenance guide, Deployment guide, Testing strategy, Evaluation baseline, AI system card, Operations runbook (+3 more)

### Community 112 - "manifest.json"
Cohesion: 0.50
Nodes (3): manifest_version, notice, sources

### Community 116 - "ADR 0003: Relational persistence and idempotency"
Cohesion: 0.50
Nodes (3): ADR 0003: Relational persistence and idempotency, Consequences, Decision

### Community 120 - "tools.py"
Cohesion: 0.12
Nodes (25): ApplyResolutionInput, ApplyResolutionOutput, calculate_settlement_date(), compare_trade_versions(), CompareTradeVersionsInput, CompareTradeVersionsOutput, FieldDifference, BaseModel (+17 more)

### Community 121 - "exceptions_.$exceptionId.tsx"
Cohesion: 0.13
Nodes (23): StatusBarProps, DemoRoleContext, DemoRoleContextValue, ApiError, approveWorkflow(), AuditEvent, auditSchema, DemoRole (+15 more)

### Community 122 - "ReconciliationPolicy"
Cohesion: 0.16
Nodes (19): Dependency-free domain layer for deterministic facts and rules., evaluate_reconciliation(), Evaluate all twelve rule families without network or model calls., Versioned tolerances and freshness bounds for the catalogue., ReconciliationPolicy, _baseline(), generate_synthetic_dataset(), _inject() (+11 more)

### Community 123 - "Panel.tsx"
Cohesion: 0.13
Nodes (13): PlaceholderSectionProps, PageHeader(), PageHeaderProps, Panel(), PanelProps, Route, scopeExcluded, scopeIncluded (+5 more)

### Community 124 - "ReconciliationInput"
Cohesion: 0.20
Nodes (17): Return the immutable synthetic trade fixture., ExceptionFinding, ExceptionSeverity, ExceptionType, StrEnum, Structured outputs from deterministic exception rules., An explainable, deterministic rule finding; never an automatic state change., ReviewRoute (+9 more)

### Community 125 - "api/app.py"
Cohesion: 0.11
Nodes (13): _problem(), FastAPI, Request, FastAPI application factory and cross-cutting HTTP safety contracts., FixedWindowRateLimiter, Small-process rate limiter for the local demo and single-instance reference API., Bound requests per client over a rolling minute without external state., OidcTokenDecoder (+5 more)

### Community 126 - "Settings"
Cohesion: 0.15
Nodes (16): create_app(), Create an API process without opening external connections., Environment-backed settings shared by API and worker composition roots., Settings, test_health_contracts_are_deterministic(), test_production_disables_interactive_api_documentation(), HTTP envelope, request-size, and rate-limit safety tests., test_rate_limit_returns_retry_contract() (+8 more)

### Community 127 - "EventDeliveryTracker"
Cohesion: 0.16
Nodes (13): ApplicationEvent, DeliveryResult, EventDeliveryTracker, Idempotent, order-aware event delivery policy., Reject duplicates and defer gaps without losing the event., _event(), UUID, Duplicate, reordered, and missed event behavior. (+5 more)

### Community 128 - "Design System Master File"
Cohesion: 0.11
Nodes (17): Additional Forbidden Patterns, Anti-Patterns (Do NOT Use), Buttons, Cards, Color Palette, Component Specs, Design System Master File, Global Rules (+9 more)

### Community 129 - "exceptions.tsx"
Cohesion: 0.22
Nodes (13): EmptyState(), FrameProps, LoadingState(), PermissionDeniedState(), SkeletonRows(), StateFrame(), useDemoRole(), getExceptions() (+5 more)

### Community 130 - "build_golden_dataset"
Cohesion: 0.19
Nodes (12): BaselineResult, build_golden_dataset(), GoldenCase, Versioned, deterministic mock evaluation dataset., Return exactly 50 independently named synthetic evaluation cases., Evaluate the deterministic expected routing contract without a model key., run_mock_baseline(), Deterministic evaluation datasets and runners. (+4 more)

### Community 131 - "StatusBadge.tsx"
Cohesion: 0.19
Nodes (11): severityTone, stateTone, MetricTile(), MetricTileProps, badgeVariants, StatusBadge(), StatusBadgeProps, ExceptionRow (+3 more)

### Community 132 - "health.py"
Cohesion: 0.26
Nodes (11): HealthResponse, liveness(), BaseModel, get, Request, Process health contracts that do not probe unconfigured infrastructure., Confirm that the API process can serve requests., Confirm readiness for the currently dependency-free API. (+3 more)

### Community 133 - "SyntheticTrade"
Cohesion: 0.20
Nodes (9): ValueError, Immutable synthetic trade facts., Raised when a synthetic trade violates a domain invariant., A versioned synthetic trade snapshot used as input to deterministic rules., SyntheticTrade, TradeValidationError, parametrize, test_synthetic_trade_accepts_fixed_precision_and_utc_facts() (+1 more)

### Community 134 - "session.py"
Cohesion: 0.25
Nodes (9): create_engine(), create_session_factory(), Session, Explicit SQLAlchemy engine and session construction., Persistence infrastructure unit tests., test_create_engine_uses_configured_database_url(), test_session_factory_binds_engine_without_expiring_objects(), Engine (+1 more)

### Community 135 - "checkpoints.py"
Cohesion: 0.24
Nodes (9): checkpoint_connection_string(), postgres_workflow(), CompiledStateGraph, PostgreSQL checkpoint composition for normal local workflow execution., Translate the SQLAlchemy URL to the psycopg URL expected by LangGraph., Set up and yield a graph backed by durable PostgreSQL checkpoints., Durable-checkpoint configuration tests., test_checkpoint_url_rejects_non_postgresql_database() (+1 more)

### Community 136 - "test_api_security.py"
Cohesion: 0.27
Nodes (8): FakeDecoder, production_client(), TestClient, Authentication and authorization boundary tests., test_production_requires_bearer_token(), test_token_without_application_role_is_denied(), test_validated_claims_create_principal(), fixture

### Community 137 - "test_api_operations.py"
Cohesion: 0.36
Nodes (9): _client(), TestClient, Versioned API success, authorization, conflict, and idempotency tests., test_identity_not_found_validation_and_production_authentication(), test_negative_authorization_and_stale_version_conflict(), test_openapi_contains_versioned_operations_contracts(), test_queue_detail_filters_and_security_headers(), test_websocket_snapshot_and_polling_fallback() (+1 more)

### Community 138 - "test_api_platform.py"
Cohesion: 0.39
Nodes (7): _client(), TestClient, Platform API contract and privileged-operation tests., test_dashboard_trades_knowledge_and_evaluation_contracts(), test_import_is_admin_only_and_idempotent(), test_non_allowlisted_source_is_rejected(), test_source_sync_and_evaluation_runs_require_admin()

### Community 139 - "TokenDecoder"
Cohesion: 0.50
Nodes (3): Protocol, Boundary for signature-validating bearer token decoders., TokenDecoder

### Community 140 - "CHANGELOG.md"
Cohesion: 0.50
Nodes (3): [0.1.0] - 2026-08-24, Added, Changelog

### Community 141 - "Documentation index"
Cohesion: 0.50
Nodes (4): Architecture and AI, Documentation index, Product and domain, Security, development, and operations

### Community 142 - "pull_request_template.md"
Cohesion: 0.50
Nodes (3): Evidence and known limitations, Scope, Verification

### Community 143 - "Security Policy"
Cohesion: 0.50
Nodes (4): Boundaries, Report a vulnerability, Security Policy, Supported version

## Knowledge Gaps
- **394 isolated node(s):** `tradeops-copilot-backend`, `$schema`, `style`, `rsc`, `tsx` (+389 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **99 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `cn()` connect `cn` to `exceptions.tsx`, `sidebar.tsx`, `StatusBadge.tsx`, `pagination.tsx`, `utils.ts`, `__root.tsx`, `carousel.tsx`, `command.tsx`, `menubar.tsx`, `form.tsx`, `navigation-menu.tsx`, `chart.tsx`, `Panel.tsx`, `alert.tsx`, `table.tsx`, `breadcrumb.tsx`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `ReconciliationPolicy` connect `ReconciliationPolicy` to `Principal`, `models.py`, `SettlementDatePolicy`, `ReconciliationInput`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `Settings` connect `Settings` to `health.py`, `configure_observability`, `session.py`, `checkpoints.py`, `test_api_security.py`, `test_api_operations.py`, `test_api_platform.py`, `TokenDecoder`, `config.py`, `Principal`, `api/app.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `Settings` (e.g. with `HealthResponse` and `OidcTokenDecoder`) actually correct?**
  _`Settings` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Principal` (e.g. with `ApprovalRequest` and `AuditResponse`) actually correct?**
  _`Principal` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `SettlementDatePolicy` (e.g. with `ReconciliationFinding` and `ReconciliationInput`) actually correct?**
  _`SettlementDatePolicy` has 19 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tradeops-copilot-backend`, `$schema`, `style` to the rest of the system?**
  _394 weakly-connected nodes found - possible documentation gaps or missing edges._