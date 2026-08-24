import { createFileRoute } from "@tanstack/react-router";
import { CategoryBars } from "@/components/overview/CategoryBars";
import { ExceptionTable } from "@/components/overview/ExceptionTable";
import { QueueLaneList } from "@/components/overview/QueueLaneList";
import { MetricTile } from "@/components/primitives/MetricTile";
import { PageHeader } from "@/components/primitives/PageHeader";
import { Panel } from "@/components/primitives/Panel";
import { StatusBadge } from "@/components/primitives/StatusBadge";
import {
  categoryBreakdown,
  dataAsOf,
  queueLanes,
  recentExceptions,
  summaryMetrics,
} from "@/data/overview";

const title = "Overview — TradeOps Copilot";
const description =
  "Operations overview for synthetic fixed-income trade exceptions. An independent educational portfolio console using deterministic mock data only.";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
    ],
  }),
  component: OverviewPage,
});

const metricTone = {
  open: undefined,
  pending: "pending",
  verified: "verified",
  high: "severe",
} as const;

const metricBadge: Record<string, string | undefined> = {
  pending: "Pending",
  verified: "Verified",
  high: "High",
};

function OverviewPage() {
  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-6">
      <PageHeader
        title="Overview"
        summary="Snapshot of the synthetic exception fixture used to demonstrate the console layout. Nothing on this screen reflects real trading activity."
        meta={
          <div className="flex flex-wrap items-center gap-2">
            <StatusBadge tone="info">Deterministic mock data</StatusBadge>
            <span className="num text-2xs text-muted-foreground">
              Fixture as of {dataAsOf}
            </span>
          </div>
        }
      />

      <section aria-label="Fixture summary" className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {summaryMetrics.map((metric) => {
          const tone = metricTone[metric.id as keyof typeof metricTone];
          const badge = metricBadge[metric.id];
          return (
            <MetricTile
              key={metric.id}
              label={metric.label}
              value={metric.value}
              note={metric.note}
              {...(tone ? { tone } : {})}
              {...(badge ? { badge } : {})}
            />
          );
        })}
      </section>

      <Panel
        title="Recent exceptions"
        description="Five most recent items in the sample fixture. Row order is fixed."
        flush
        actions={<StatusBadge tone="neutral">Sample · 5 of 42</StatusBadge>}
      >
        <ExceptionTable rows={recentExceptions} />
      </Panel>

      <div className="grid gap-4 lg:grid-cols-2">
        <Panel
          title="Exception categories"
          description="Share of the 42-item sample by break category."
        >
          <CategoryBars items={categoryBreakdown} />
        </Panel>

        <Panel
          title="Queue lanes"
          description="Sample distribution across three notional desk lanes."
        >
          <QueueLaneList lanes={queueLanes} />
        </Panel>
      </div>

      <p className="text-2xs leading-relaxed text-muted-foreground">
        All values above come from a checked-in fixture and do not change over time. No
        performance, accuracy, or coverage claims are made.
      </p>
    </div>
  );
}
