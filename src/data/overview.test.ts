import { describe, expect, it } from "vitest";
import {
  categoryBreakdown,
  dataAsOf,
  queueLanes,
  recentExceptions,
  summaryMetrics,
} from "./overview";

function metricValue(id: string) {
  const metric = summaryMetrics.find((item) => item.id === id);
  expect(metric, `Missing summary metric: ${id}`).toBeDefined();
  return Number(metric?.value);
}

describe("deterministic synthetic overview fixture", () => {
  it("uses an explicit fixed timestamp and synthetic instrument labels", () => {
    expect(dataAsOf).toContain("fixed fixture");
    expect(recentExceptions).not.toHaveLength(0);
    expect(recentExceptions.every((row) => row.instrument.startsWith("SYN "))).toBe(true);
  });

  it("keeps aggregate totals internally consistent", () => {
    const categoryTotal = categoryBreakdown.reduce((total, item) => total + item.count, 0);
    const shareTotal = categoryBreakdown.reduce((total, item) => total + item.share, 0);
    const queueOpen = queueLanes.reduce((total, lane) => total + lane.open, 0);
    const queuePending = queueLanes.reduce((total, lane) => total + lane.pending, 0);
    const queueVerified = queueLanes.reduce((total, lane) => total + lane.verified, 0);

    expect(categoryTotal).toBe(metricValue("open"));
    expect(queueOpen).toBe(metricValue("open"));
    expect(queuePending).toBe(metricValue("pending"));
    expect(queueVerified).toBe(metricValue("verified"));
    expect(shareTotal).toBe(100);
  });

  it("uses stable unique identifiers", () => {
    const exceptionIds = recentExceptions.map((row) => row.id);
    const laneIds = queueLanes.map((lane) => lane.id);

    expect(new Set(exceptionIds).size).toBe(exceptionIds.length);
    expect(new Set(laneIds).size).toBe(laneIds.length);
  });
});
