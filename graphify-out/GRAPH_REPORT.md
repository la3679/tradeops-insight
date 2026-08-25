# Graph Report - tradeops-insight  (2026-08-24)

## Corpus Check
- 131 files · ~32,898 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 835 nodes · 1258 edges · 106 communities (43 shown, 63 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `93a8d459`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- routeTree.gen.ts
- cn
- sidebar.tsx
- devDependencies
- compilerOptions
- index.tsx
- carousel.tsx
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
- sheet.tsx
- table.tsx
- Architecture Baseline
- drawer.tsx
- select.tsx
- What You Must Do When Invoked
- toggle-group.tsx
- graphify reference: extra exports and benchmark
- input-otp.tsx
- badge.tsx
- navigation-menu.tsx
- sonner.tsx
- class-variance-authority
- clsx
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
- @radix-ui/react-dropdown-menu
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
- dropdown-menu.tsx
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
- domain/__init__.py
- observability/__init__.py
- orchestration/__init__.py
- ports/__init__.py
- worker/__init__.py
- tradeops-copilot-backend

## God Nodes (most connected - your core abstractions)
1. `cn()` - 231 edges
2. `compilerOptions` - 22 edges
3. `scripts` - 20 edges
4. `Settings` - 15 edges
5. `What You Must Do When Invoked` - 12 edges
6. `FileRoutesByPath` - 10 edges
7. `/graphify` - 10 edges
8. `StatusBadge()` - 9 edges
9. `buttonVariants` - 9 edges
10. `graphify reference: extra exports and benchmark` - 8 edges

## Surprising Connections (you probably didn't know these)
- `StateFrame()` --calls--> `cn()`  [EXTRACTED]
  src/components/primitives/StateBlocks.tsx → src/lib/utils.ts
- `AlertDialogOverlay` --calls--> `cn()`  [EXTRACTED]
  src/components/ui/alert-dialog.tsx → src/lib/utils.ts
- `AlertDialogContent` --calls--> `cn()`  [EXTRACTED]
  src/components/ui/alert-dialog.tsx → src/lib/utils.ts
- `AlertDialogHeader()` --calls--> `cn()`  [EXTRACTED]
  src/components/ui/alert-dialog.tsx → src/lib/utils.ts
- `AlertDialogFooter()` --calls--> `cn()`  [EXTRACTED]
  src/components/ui/alert-dialog.tsx → src/lib/utils.ts

## Import Cycles
- None detected.

## Communities (106 total, 63 thin omitted)

### Community 0 - "routeTree.gen.ts"
Cohesion: 0.06
Nodes (41): PlaceholderSection(), PlaceholderSectionProps, PageHeader(), PageHeaderProps, EmptyState(), FrameProps, LoadingState(), PermissionDeniedState() (+33 more)

### Community 1 - "cn"
Cohesion: 0.09
Nodes (34): AccordionContent, AccordionItem, AccordionTrigger, Avatar, AvatarFallback, AvatarImage, Breadcrumb, BreadcrumbEllipsis() (+26 more)

### Community 2 - "sidebar.tsx"
Cohesion: 0.07
Nodes (33): Button, Input, Separator, Sidebar, SidebarContent, SidebarContext, SidebarContextProps, SidebarFooter (+25 more)

### Community 3 - "devDependencies"
Cohesion: 0.04
Nodes (49): eslint, eslint-config-prettier, @eslint/js, eslint-plugin-prettier, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jest-axe (+41 more)

### Community 4 - "compilerOptions"
Cohesion: 0.06
Nodes (32): DOM, DOM.Iterable, ES2022, eslint.config.js, src/**/*.ts, src/**/*.tsx, vite/client, vite.config.ts (+24 more)

### Community 5 - "index.tsx"
Cohesion: 0.12
Nodes (26): CategoryBars(), ExceptionTable(), severityTone, stateTone, QueueLaneList(), MetricTile(), MetricTileProps, Panel() (+18 more)

### Community 6 - "carousel.tsx"
Cohesion: 0.07
Nodes (33): AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter(), AlertDialogHeader(), AlertDialogOverlay, AlertDialogTitle (+25 more)

### Community 7 - "utils.ts"
Cohesion: 0.10
Nodes (11): Checkbox, HoverCardContent, PopoverContent, Progress, RadioGroup, RadioGroupItem, ResizableHandle(), ResizablePanelGroup() (+3 more)

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
Cohesion: 0.07
Nodes (26): name, overrides, rolldown, private, scripts, backend:format:check, backend:lint, backend:sync (+18 more)

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
Cohesion: 0.09
Nodes (33): create_app(), FastAPI application factory., Create an API process without opening external connections., HealthResponse, liveness(), Process health contracts that do not probe unconfigured infrastructure., Confirm that the API process can serve requests., Confirm readiness for the currently dependency-free API. (+25 more)

### Community 16 - "dependencies"
Cohesion: 0.15
Nodes (13): cmdk, lucide-react, dependencies, cmdk, lucide-react, @radix-ui/react-checkbox, @radix-ui/react-progress, react (+5 more)

### Community 17 - "chart.tsx"
Cohesion: 0.25
Nodes (9): ChartConfig, ChartContainer, ChartContext, ChartContextProps, ChartLegendContent, ChartTooltipContent, getPayloadConfigFromPayload(), THEMES (+1 more)

### Community 18 - "sheet.tsx"
Cohesion: 0.25
Nodes (8): SheetContent, SheetContentProps, SheetDescription, SheetFooter(), SheetHeader(), SheetOverlay, SheetTitle, sheetVariants

### Community 19 - "table.tsx"
Cohesion: 0.22
Nodes (8): Table, TableBody, TableCaption, TableCell, TableFooter, TableHead, TableHeader, TableRow

### Community 20 - "Architecture Baseline"
Cohesion: 0.05
Nodes (37): Coding rules, graphify, Ownership boundaries, Review requirements, TradeOps Copilot — agent guidelines, ADR 0001: Modular Monolith with a Background Worker, Consequences, Context (+29 more)

### Community 21 - "drawer.tsx"
Cohesion: 0.25
Nodes (6): DrawerContent, DrawerDescription, DrawerFooter(), DrawerHeader(), DrawerOverlay, DrawerTitle

### Community 22 - "select.tsx"
Cohesion: 0.25
Nodes (7): SelectContent, SelectItem, SelectLabel, SelectScrollDownButton, SelectScrollUpButton, SelectSeparator, SelectTrigger

### Community 23 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 24 - "toggle-group.tsx"
Cohesion: 0.43
Nodes (5): ToggleGroup, ToggleGroupContext, ToggleGroupItem, Toggle, toggleVariants

### Community 25 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 26 - "input-otp.tsx"
Cohesion: 0.40
Nodes (4): InputOTP, InputOTPGroup, InputOTPSeparator, InputOTPSlot

### Community 27 - "badge.tsx"
Cohesion: 0.67
Nodes (3): Badge(), BadgeProps, badgeVariants

### Community 28 - "navigation-menu.tsx"
Cohesion: 0.29
Nodes (7): NavigationMenu, NavigationMenuContent, NavigationMenuIndicator, NavigationMenuList, NavigationMenuTrigger, navigationMenuTriggerStyle, NavigationMenuViewport

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

### Community 84 - "dropdown-menu.tsx"
Cohesion: 0.20
Nodes (9): DropdownMenuCheckboxItem, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuRadioItem, DropdownMenuSeparator, DropdownMenuShortcut(), DropdownMenuSubContent (+1 more)

### Community 85 - "ADR 0002: Python runtime and durable task queue boundary"
Cohesion: 0.40
Nodes (4): ADR 0002: Python runtime and durable task queue boundary, Consequences, Context, Decision

### Community 92 - "alert.tsx"
Cohesion: 0.50
Nodes (4): Alert, AlertDescription, AlertTitle, alertVariants

## Knowledge Gaps
- **283 isolated node(s):** `tradeops-copilot-backend`, `$schema`, `style`, `rsc`, `tsx` (+278 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **63 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `cn()` connect `cn` to `routeTree.gen.ts`, `sidebar.tsx`, `index.tsx`, `carousel.tsx`, `utils.ts`, `__root.tsx`, `command.tsx`, `menubar.tsx`, `form.tsx`, `chart.tsx`, `sheet.tsx`, `table.tsx`, `drawer.tsx`, `select.tsx`, `toggle-group.tsx`, `input-otp.tsx`, `badge.tsx`, `navigation-menu.tsx`, `dropdown-menu.tsx`, `alert.tsx`?**
  _High betweenness centrality (0.194) - this node is a cross-community bridge._
- **Why does `dependencies` connect `dependencies` to `scripts`, `class-variance-authority`, `clsx`, `date-fns`, `embla-carousel-react`, `@hookform/resolvers`, `input-otp`, `@radix-ui/react-accordion`, `@radix-ui/react-alert-dialog`, `@radix-ui/react-aspect-ratio`, `@radix-ui/react-avatar`, `@radix-ui/react-collapsible`, `@radix-ui/react-context-menu`, `@radix-ui/react-dialog`, `@radix-ui/react-dropdown-menu`, `@radix-ui/react-hover-card`, `@radix-ui/react-label`, `@radix-ui/react-menubar`, `@radix-ui/react-navigation-menu`, `@radix-ui/react-popover`, `@radix-ui/react-radio-group`, `@radix-ui/react-scroll-area`, `@radix-ui/react-select`, `@radix-ui/react-separator`, `@radix-ui/react-slider`, `@radix-ui/react-slot`, `@radix-ui/react-switch`, `@radix-ui/react-tabs`, `@radix-ui/react-toggle`, `@radix-ui/react-toggle-group`, `@radix-ui/react-tooltip`, `react-day-picker`, `react-dom`, `react-hook-form`, `react-resizable-panels`, `recharts`, `tailwind-merge`, `tailwindcss`, `@tailwindcss/vite`, `@tanstack/react-query`, `@tanstack/react-router`, `@tanstack/react-start`, `@tanstack/router-plugin`, `tw-animate-css`, `vaul`, `vite-tsconfig-paths`, `zod`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `devDependencies` connect `devDependencies` to `scripts`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **What connects `tradeops-copilot-backend`, `$schema`, `style` to the rest of the system?**
  _283 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `routeTree.gen.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.05573770491803279 - nodes in this community are weakly interconnected._
- **Should `cn` be split into smaller, more focused modules?**
  _Cohesion score 0.08780487804878048 - nodes in this community are weakly interconnected._
- **Should `sidebar.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.06612685560053981 - nodes in this community are weakly interconnected._