# Graph Report - tradeops-insight  (2026-08-24)

## Corpus Check
- 167 files · ~42,752 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1115 nodes · 1865 edges · 120 communities (57 shown, 63 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 74 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `678c24d8`
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
- Settings
- dependencies
- chart.tsx
- models.py
- Domain glossary
- Architecture Baseline
- Settlement-date mismatch runbook
- pipeline.py
- What You Must Do When Invoked
- toggle-group.tsx
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
- input-otp.tsx
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
- observability/__init__.py
- build_workflow
- ports/__init__.py
- worker/__init__.py
- tradeops-copilot-backend
- TradeOps Copilot Product Brief
- Project State
- TradeOps Copilot — agent guidelines
- ADR 0001: Modular Monolith with a Background Worker
- TradeOps Copilot
- manifest.json
- @radix-ui/react-dropdown-menu
- clsx
- ADR 0003: Relational persistence and idempotency
- ADR 0004: Offline retrieval and explicit agent graph
- cmdk
- exception-triage.md

## God Nodes (most connected - your core abstractions)
1. `cn()` - 231 edges
2. `Base` - 27 edges
3. `SettlementDatePolicy` - 26 edges
4. `scripts` - 25 edges
5. `IdentityMixin` - 23 edges
6. `compilerOptions` - 22 edges
7. `ReconciliationPolicy` - 20 edges
8. `Settings` - 19 edges
9. `TimestampMixin` - 17 edges
10. `TradeOpsRepository` - 17 edges

## Surprising Connections (you probably didn't know these)
- `test_seed_is_idempotent_and_queue_evidence_is_detached()` --calls--> `create_engine()`  [INFERRED]
  backend/tests/adapters/persistence/test_repository.py → backend/src/tradeops/adapters/persistence/session.py
- `ReconciliationPolicy` --uses--> `ExceptionType`  [INFERRED]
  backend/src/tradeops/domain/reconciliation.py → backend/src/tradeops/domain/exceptions.py
- `SyntheticDataset` --uses--> `ExceptionType`  [INFERRED]
  backend/src/tradeops/domain/synthetic.py → backend/src/tradeops/domain/exceptions.py
- `ReconciliationPolicy` --uses--> `ExceptionSeverity`  [INFERRED]
  backend/src/tradeops/domain/reconciliation.py → backend/src/tradeops/domain/exceptions.py
- `ReconciliationPolicy` --uses--> `ReviewRoute`  [INFERRED]
  backend/src/tradeops/domain/reconciliation.py → backend/src/tradeops/domain/exceptions.py

## Import Cycles
- None detected.

## Communities (120 total, 63 thin omitted)

### Community 0 - "routeTree.gen.ts"
Cohesion: 0.06
Nodes (41): PlaceholderSection(), PlaceholderSectionProps, PageHeader(), PageHeaderProps, EmptyState(), FrameProps, LoadingState(), PermissionDeniedState() (+33 more)

### Community 1 - "cn"
Cohesion: 0.07
Nodes (47): AccordionContent, AccordionItem, AccordionTrigger, Avatar, AvatarFallback, AvatarImage, Card, CardContent (+39 more)

### Community 2 - "sidebar.tsx"
Cohesion: 0.06
Nodes (40): Input, Separator, SheetContent, SheetContentProps, SheetDescription, SheetFooter(), SheetHeader(), SheetOverlay (+32 more)

### Community 3 - "devDependencies"
Cohesion: 0.04
Nodes (49): eslint, eslint-config-prettier, @eslint/js, eslint-plugin-prettier, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jest-axe (+41 more)

### Community 4 - "compilerOptions"
Cohesion: 0.06
Nodes (32): DOM, DOM.Iterable, ES2022, eslint.config.js, src/**/*.ts, src/**/*.tsx, vite/client, vite.config.ts (+24 more)

### Community 5 - "index.tsx"
Cohesion: 0.12
Nodes (26): CategoryBars(), ExceptionTable(), severityTone, stateTone, QueueLaneList(), MetricTile(), MetricTileProps, Panel() (+18 more)

### Community 6 - "pagination.tsx"
Cohesion: 0.12
Nodes (21): AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter(), AlertDialogHeader(), AlertDialogOverlay, AlertDialogTitle (+13 more)

### Community 7 - "utils.ts"
Cohesion: 0.07
Nodes (16): Badge(), BadgeProps, badgeVariants, Checkbox, HoverCardContent, PopoverContent, Progress, RadioGroup (+8 more)

### Community 8 - "__root.tsx"
Cohesion: 0.13
Nodes (11): AppFooter(), AppShell(), SideNav(), SideNavProps, LovableErrorOptions, LovableEvents, reportLovableError(), Window (+3 more)

### Community 9 - "server.ts"
Cohesion: 0.16
Nodes (13): consumeLastCapturedError(), describeError(), describeStatus(), originalConsoleError, safeStringify(), renderErrorPage(), fetch(), getServerEntry() (+5 more)

### Community 10 - "components.json"
Cohesion: 0.11
Nodes (18): aliases, components, hooks, lib, ui, utils, iconLibrary, registries (+10 more)

### Community 11 - "scripts"
Cohesion: 0.06
Nodes (31): name, overrides, rolldown, private, scripts, backend:format:check, backend:lint, backend:sync (+23 more)

### Community 12 - "command.tsx"
Cohesion: 0.12
Nodes (14): Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList, CommandSeparator, CommandShortcut() (+6 more)

### Community 13 - "menubar.tsx"
Cohesion: 0.12
Nodes (11): Menubar, MenubarCheckboxItem, MenubarContent, MenubarItem, MenubarLabel, MenubarRadioItem, MenubarSeparator, MenubarShortcut() (+3 more)

### Community 14 - "form.tsx"
Cohesion: 0.19
Nodes (12): FormControl, FormDescription, FormFieldContext, FormFieldContextValue, FormItem, FormItemContext, FormItemContextValue, FormLabel (+4 more)

### Community 15 - "Settings"
Cohesion: 0.06
Nodes (42): create_engine(), create_session_factory(), Session, Explicit SQLAlchemy engine and session construction., create_app(), FastAPI application factory., Create an API process without opening external connections., HealthResponse (+34 more)

### Community 16 - "dependencies"
Cohesion: 0.15
Nodes (13): class-variance-authority, lucide-react, dependencies, class-variance-authority, lucide-react, @radix-ui/react-checkbox, @radix-ui/react-progress, react (+5 more)

### Community 17 - "chart.tsx"
Cohesion: 0.25
Nodes (9): ChartConfig, ChartContainer, ChartContext, ChartContextProps, ChartLegendContent, ChartTooltipContent, getPayloadConfigFromPayload(), THEMES (+1 more)

### Community 18 - "models.py"
Cohesion: 0.08
Nodes (61): SQLAlchemy persistence adapter., ApprovalRecord, AuditEventRecord, Base, CounterpartyRecord, DataSourceSyncRunRecord, DocumentChunkRecord, DocumentRecord (+53 more)

### Community 19 - "Domain glossary"
Cohesion: 0.29
Nodes (7): Domain glossary, Escalation, Exception catalogue, Exception finding, Review correction, Settlement-date mismatch, Synthetic trade

### Community 20 - "Architecture Baseline"
Cohesion: 0.25
Nodes (8): Architecture Baseline, Dependency direction, Evolution criteria, Initial module boundaries, Investigation workflow, Ownership boundaries, System shape, Workflow safety model

### Community 21 - "Settlement-date mismatch runbook"
Cohesion: 0.29
Nodes (6): Current limitations, Detection, Escalation, Review correction, Settlement-date mismatch runbook, Severity and routing

### Community 22 - "pipeline.py"
Cohesion: 0.10
Nodes (26): Safe, offline-capable retrieval primitives., chunk_document(), Citation, FaissKnowledgeIndex, generate_synthetic_policy_documents(), HashEmbeddingProvider, KnowledgeChunk, KnowledgeDocument (+18 more)

### Community 23 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 24 - "toggle-group.tsx"
Cohesion: 0.43
Nodes (5): ToggleGroup, ToggleGroupContext, ToggleGroupItem, Toggle, toggleVariants

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

### Community 84 - "input-otp.tsx"
Cohesion: 0.40
Nodes (4): InputOTP, InputOTPGroup, InputOTPSeparator, InputOTPSlot

### Community 85 - "ADR 0002: Python runtime and durable task queue boundary"
Cohesion: 0.40
Nodes (4): ADR 0002: Python runtime and durable task queue boundary, Consequences, Context, Decision

### Community 92 - "alert.tsx"
Cohesion: 0.50
Nodes (4): Alert, AlertDescription, AlertTitle, alertVariants

### Community 99 - "SettlementDatePolicy"
Cohesion: 0.09
Nodes (45): Return detached evidence payloads for a single finding., ExceptionFinding, ExceptionSeverity, ExceptionType, Structured outputs from deterministic exception rules., An explainable, deterministic rule finding; never an automatic state change., ReviewRoute, Dependency-free domain layer for deterministic facts and rules. (+37 more)

### Community 101 - "build_workflow"
Cohesion: 0.07
Nodes (34): build_workflow(), Explicit typed LangGraph workflow with mandatory human review before mutation., Versioned workflow state; steps use an append reducer across checkpoints., Compile the reviewed thirteen-node graph with replayable defaults., _step(), WorkflowState, Typed workflow and provider composition., Classification (+26 more)

### Community 106 - "TradeOps Copilot Product Brief"
Cohesion: 0.29
Nodes (7): Data policy, First release journey, Non-goals, Purpose, Release principle, TradeOps Copilot Product Brief, Users and outcomes

### Community 107 - "Project State"
Cohesion: 0.25
Nodes (7): Environment notes, Known limitations, Next three actions, Project State, Resume checkpoint, Safety boundaries, Verification status

### Community 108 - "TradeOps Copilot — agent guidelines"
Cohesion: 0.33
Nodes (5): Coding rules, graphify, Ownership boundaries, Review requirements, TradeOps Copilot — agent guidelines

### Community 109 - "ADR 0001: Modular Monolith with a Background Worker"
Cohesion: 0.33
Nodes (5): ADR 0001: Modular Monolith with a Background Worker, Consequences, Context, Decision, Revisit when

### Community 110 - "TradeOps Copilot"
Cohesion: 0.33
Nodes (6): Architecture and safety, Current scope, Local development, Lovable, TradeOps Copilot, Verification

### Community 112 - "manifest.json"
Cohesion: 0.50
Nodes (3): manifest_version, notice, sources

### Community 116 - "ADR 0003: Relational persistence and idempotency"
Cohesion: 0.50
Nodes (3): ADR 0003: Relational persistence and idempotency, Consequences, Decision

## Knowledge Gaps
- **307 isolated node(s):** `tradeops-copilot-backend`, `$schema`, `style`, `rsc`, `tsx` (+302 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **63 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `cn()` connect `cn` to `routeTree.gen.ts`, `sidebar.tsx`, `index.tsx`, `pagination.tsx`, `utils.ts`, `__root.tsx`, `command.tsx`, `menubar.tsx`, `form.tsx`, `navigation-menu.tsx`, `chart.tsx`, `input-otp.tsx`, `toggle-group.tsx`, `carousel.tsx`, `alert.tsx`, `table.tsx`, `breadcrumb.tsx`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Why does `dependencies` connect `dependencies` to `scripts`, `date-fns`, `embla-carousel-react`, `@hookform/resolvers`, `input-otp`, `@radix-ui/react-accordion`, `@radix-ui/react-alert-dialog`, `@radix-ui/react-aspect-ratio`, `@radix-ui/react-avatar`, `@radix-ui/react-collapsible`, `@radix-ui/react-context-menu`, `@radix-ui/react-dialog`, `@radix-ui/react-hover-card`, `@radix-ui/react-label`, `@radix-ui/react-menubar`, `@radix-ui/react-navigation-menu`, `@radix-ui/react-popover`, `@radix-ui/react-radio-group`, `@radix-ui/react-scroll-area`, `@radix-ui/react-select`, `@radix-ui/react-separator`, `@radix-ui/react-slider`, `@radix-ui/react-slot`, `@radix-ui/react-switch`, `@radix-ui/react-tabs`, `@radix-ui/react-toggle`, `@radix-ui/react-toggle-group`, `@radix-ui/react-tooltip`, `react-day-picker`, `react-dom`, `react-hook-form`, `react-resizable-panels`, `recharts`, `tailwind-merge`, `tailwindcss`, `@tailwindcss/vite`, `@tanstack/react-query`, `@tanstack/react-router`, `@tanstack/react-start`, `@tanstack/router-plugin`, `tw-animate-css`, `vaul`, `vite-tsconfig-paths`, `zod`, `@radix-ui/react-dropdown-menu`, `clsx`, `cmdk`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `devDependencies` connect `devDependencies` to `scripts`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `SettlementDatePolicy` (e.g. with `ReconciliationFinding` and `ReconciliationInput`) actually correct?**
  _`SettlementDatePolicy` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tradeops-copilot-backend`, `$schema`, `style` to the rest of the system?**
  _307 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `routeTree.gen.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.05573770491803279 - nodes in this community are weakly interconnected._
- **Should `cn` be split into smaller, more focused modules?**
  _Cohesion score 0.06558441558441558 - nodes in this community are weakly interconnected._