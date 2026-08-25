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
    value: "42",
    note: "Synthetic queue snapshot, fixed sample set",
  },
  {
    id: "pending",
    label: "Awaiting review",
    value: "11",
    note: "Items with an unconfirmed proposed resolution",
  },
  {
    id: "verified",
    label: "Reviewer-verified",
    value: "27",
    note: "Closed after a human confirmed the sample outcome",
  },
  {
    id: "high",
    label: "High severity",
    value: "4",
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
    id: "EXC-10412",
    instrument: "SYN 4.25% 2031 Corp",
    category: "Settlement date mismatch",
    severity: "high",
    state: "escalated",
    ageHours: 3,
    owner: "Desk Ops A",
  },
  {
    id: "EXC-10408",
    instrument: "SYN 2.75% 2028 Govt",
    category: "Accrued interest variance",
    severity: "medium",
    state: "pending",
    ageHours: 7,
    owner: "Desk Ops A",
  },
  {
    id: "EXC-10399",
    instrument: "SYN 5.10% 2034 Corp",
    category: "Counterparty SSI missing",
    severity: "medium",
    state: "pending",
    ageHours: 12,
    owner: "Desk Ops B",
  },
  {
    id: "EXC-10387",
    instrument: "SYN 3.00% 2027 Muni",
    category: "Price tolerance break",
    severity: "low",
    state: "verified",
    ageHours: 21,
    owner: "Desk Ops B",
  },
  {
    id: "EXC-10376",
    instrument: "SYN 1.95% 2026 Govt",
    category: "Duplicate allocation",
    severity: "low",
    state: "verified",
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
  { category: "Settlement date mismatch", count: 14, share: 33 },
  { category: "Accrued interest variance", count: 11, share: 26 },
  { category: "Counterparty SSI missing", count: 8, share: 19 },
  { category: "Price tolerance break", count: 6, share: 14 },
  { category: "Duplicate allocation", count: 3, share: 8 },
] as const;

export type QueueLane = {
  readonly id: string;
  readonly name: string;
  readonly open: number;
  readonly pending: number;
  readonly verified: number;
};

export const queueLanes: readonly QueueLane[] = [
  { id: "lane-a", name: "Desk Ops A", open: 18, pending: 5, verified: 11 },
  { id: "lane-b", name: "Desk Ops B", open: 15, pending: 4, verified: 9 },
  { id: "lane-c", name: "Desk Ops C", open: 9, pending: 2, verified: 7 },
] as const;

export const dataAsOf = "2026-03-02 09:00 UTC (fixed fixture)";
