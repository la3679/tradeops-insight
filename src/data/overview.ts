/**
 * Deterministic synthetic data for the Overview screen.
 * No live feed, no randomness, no real instruments or counterparties.
 */

export type Severity = "high" | "medium" | "low";
export type ReviewState = "verified" | "pending" | "escalated";

export type SummaryMetric = {
  readonly id: string;
  readonly label: string;
  readonly value: string;
  readonly unit?: string;
  readonly note: string;
};

export const summaryMetrics: readonly SummaryMetric[] = [
  {
    id: "open",
    label: "Open exceptions",
    value: "30",
    note: "Fast synthetic seed, deterministic findings",
  },
  {
    id: "pending",
    label: "Awaiting review",
    value: "12",
    note: "Items with an unconfirmed proposed resolution",
  },
  {
    id: "verified",
    label: "Reviewer-verified",
    value: "0",
    note: "Fresh seed; review actions begin at zero",
  },
  {
    id: "high",
    label: "High severity",
    value: "15",
    note: "Sample items tagged high severity in the fixture",
  },
] as const;

export type ExceptionRow = {
  readonly id: string;
  readonly instrument: string;
  readonly category: string;
  readonly severity: Severity;
  readonly state: ReviewState;
  readonly ageHours: number;
  readonly owner: string;
};

export const recentExceptions: readonly ExceptionRow[] = [
  {
    id: "EXC-DEMO-0001",
    instrument: "SYN Corporate Bond 0031",
    category: "Settlement date mismatch",
    severity: "high",
    state: "escalated",
    ageHours: 3,
    owner: "Desk Ops A",
  },
  {
    id: "EXC-DEMO-0002",
    instrument: "SYN Government Bond 0028",
    category: "Counterparty name mismatch",
    severity: "medium",
    state: "pending",
    ageHours: 7,
    owner: "Desk Ops A",
  },
  {
    id: "EXC-DEMO-0003",
    instrument: "SYN Corporate Bond 0034",
    category: "Missing confirmation",
    severity: "medium",
    state: "pending",
    ageHours: 12,
    owner: "Desk Ops B",
  },
  {
    id: "EXC-DEMO-0004",
    instrument: "SYN Government Bond 0027",
    category: "Price tolerance break",
    severity: "low",
    state: "pending",
    ageHours: 21,
    owner: "Desk Ops B",
  },
  {
    id: "EXC-DEMO-0005",
    instrument: "SYN Government Bond 0026",
    category: "Duplicate trade or event",
    severity: "low",
    state: "pending",
    ageHours: 30,
    owner: "Desk Ops C",
  },
] as const;

export type CategoryBreakdown = {
  readonly category: string;
  readonly count: number;
  readonly share: number;
};

export const categoryBreakdown: readonly CategoryBreakdown[] = [
  { category: "Settlement date mismatch", count: 8, share: 27 },
  { category: "Counterparty identity", count: 7, share: 23 },
  { category: "Missing or contradictory evidence", count: 6, share: 20 },
  { category: "Price or notional mismatch", count: 5, share: 17 },
  { category: "Duplicate or malformed payload", count: 4, share: 13 },
] as const;

export type QueueLane = {
  readonly id: string;
  readonly name: string;
  readonly open: number;
  readonly pending: number;
  readonly verified: number;
};

export const queueLanes: readonly QueueLane[] = [
  { id: "lane-a", name: "Identity review", open: 10, pending: 4, verified: 0 },
  { id: "lane-b", name: "Economic terms", open: 10, pending: 4, verified: 0 },
  { id: "lane-c", name: "Evidence and dates", open: 10, pending: 4, verified: 0 },
] as const;

export const dataAsOf = "2026-08-24 14:00 UTC (fixed fixture)";
