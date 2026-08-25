import { useQuery } from "@tanstack/react-query";
import { Link, createFileRoute } from "@tanstack/react-router";
import { AlertTriangle, ChevronRight, Filter, Search } from "lucide-react";
import { useState } from "react";
import { EmptyState, LoadingState } from "@/components/primitives/StateBlocks";
import { PageHeader } from "@/components/primitives/PageHeader";
import { Panel } from "@/components/primitives/Panel";
import { StatusBadge, type StatusBadgeProps } from "@/components/primitives/StatusBadge";
import { Input } from "@/components/ui/input";
import { useDemoRole } from "@/lib/demo-role";
import { getExceptions } from "@/lib/tradeops-api";

const title = "Exception Queue — TradeOps Copilot";
const description =
  "Filterable queue of deterministic synthetic fixed-income trade exceptions with reviewed workflow routing.";

export const Route = createFileRoute("/exceptions")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
    ],
  }),
  component: ExceptionsPage,
});

const severityTone: Record<string, NonNullable<StatusBadgeProps["tone"]>> = {
  critical: "severe",
  high: "severe",
  medium: "pending",
  low: "neutral",
};

function ExceptionsPage() {
  const { role } = useDemoRole();
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [severity, setSeverity] = useState("");
  const query = useQuery({
    queryKey: ["exceptions", role, status, severity, search],
    queryFn: () => getExceptions(role, { status, severity, search }),
  });

  return (
    <div className="mx-auto flex w-full max-w-[90rem] flex-col gap-5">
      <PageHeader
        title="Exception queue"
        summary="Review deterministic findings across all twelve required synthetic scenarios. Filters affect only the local demonstration dataset."
        meta={
          <div className="flex flex-wrap items-center gap-2">
            <StatusBadge tone="info">Synthetic records</StatusBadge>
            <StatusBadge tone="neutral">Role · {role}</StatusBadge>
          </div>
        }
      />

      <Panel
        title="Queue filters"
        description="Search synthetic trade IDs or exception categories."
        actions={
          <StatusBadge tone="neutral">
            {query.data ? `${query.data.total} results` : "Loading"}
          </StatusBadge>
        }
      >
        <div className="grid gap-3 md:grid-cols-[minmax(16rem,1fr)_12rem_12rem]">
          <label className="grid gap-1 text-xs font-medium text-foreground">
            <span className="flex items-center gap-1.5">
              <Search className="size-3.5" aria-hidden="true" /> Search
            </span>
            <Input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="TRD-DEMO-000001 or currency mismatch"
            />
          </label>
          <label className="grid gap-1 text-xs font-medium text-foreground">
            <span className="flex items-center gap-1.5">
              <Filter className="size-3.5" aria-hidden="true" /> Status
            </span>
            <select
              value={status}
              onChange={(event) => setStatus(event.target.value)}
              className="h-9 cursor-pointer rounded-md border border-input bg-background px-3 text-sm"
            >
              <option value="">All statuses</option>
              <option value="open">Open</option>
              <option value="escalated">Escalated</option>
              <option value="resolved">Resolved</option>
            </select>
          </label>
          <label className="grid gap-1 text-xs font-medium text-foreground">
            Severity
            <select
              value={severity}
              onChange={(event) => setSeverity(event.target.value)}
              className="h-9 cursor-pointer rounded-md border border-input bg-background px-3 text-sm"
            >
              <option value="">All severities</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </label>
        </div>
      </Panel>

      <Panel
        title="Active findings"
        description="Open a row to inspect evidence, proposal, workflow trace, and reviewer controls."
        flush
      >
        {query.isPending ? <LoadingState label="Loading synthetic exception queue" /> : null}
        {query.isError ? (
          <div role="alert" className="m-4 rounded-md border border-severe/30 bg-severe-subtle p-4">
            <div className="flex items-start gap-3">
              <AlertTriangle className="mt-0.5 size-4 text-severe" aria-hidden="true" />
              <div>
                <p className="text-sm font-semibold">Queue API unavailable</p>
                <p className="mt-1 text-xs text-muted-foreground">
                  Start the local API on port 8000, then retry. Deterministic fixtures remain safe
                  and unchanged.
                </p>
                <button
                  type="button"
                  onClick={() => query.refetch()}
                  className="mt-3 cursor-pointer text-xs font-semibold text-primary underline"
                >
                  Retry request
                </button>
              </div>
            </div>
          </div>
        ) : null}
        {query.data?.items.length === 0 ? (
          <EmptyState
            title="No exceptions match"
            description="Clear or broaden the filters to return to the synthetic queue."
          />
        ) : null}
        {query.data?.items.length ? (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[64rem] border-collapse text-left text-xs">
              <caption className="sr-only">Synthetic trade exception queue</caption>
              <thead>
                <tr className="border-b border-border bg-muted/45 text-2xs uppercase tracking-wide text-muted-foreground">
                  <th scope="col" className="px-4 py-2 font-medium">
                    Trade
                  </th>
                  <th scope="col" className="px-4 py-2 font-medium">
                    Exception
                  </th>
                  <th scope="col" className="px-4 py-2 font-medium">
                    Severity
                  </th>
                  <th scope="col" className="px-4 py-2 font-medium">
                    Status
                  </th>
                  <th scope="col" className="px-4 py-2 font-medium">
                    Route
                  </th>
                  <th scope="col" className="px-4 py-2 font-medium">
                    Version
                  </th>
                  <th scope="col" className="px-4 py-2 text-right font-medium">
                    Open
                  </th>
                </tr>
              </thead>
              <tbody>
                {query.data.items.map((item) => (
                  <tr
                    key={item.id}
                    className="border-b border-border transition-colors hover:bg-accent/60"
                  >
                    <th scope="row" className="num px-4 py-2.5 font-semibold">
                      {item.synthetic_trade_id}
                    </th>
                    <td className="px-4 py-2.5">
                      <p className="font-medium text-foreground">
                        {item.exception_type.replaceAll("_", " ")}
                      </p>
                      <p className="mt-0.5 max-w-xl truncate text-2xs text-muted-foreground">
                        {item.explanation}
                      </p>
                    </td>
                    <td className="px-4 py-2.5">
                      <StatusBadge tone={severityTone[item.severity] ?? "neutral"}>
                        {item.severity}
                      </StatusBadge>
                    </td>
                    <td className="px-4 py-2.5">
                      <StatusBadge tone={item.status === "escalated" ? "severe" : "pending"}>
                        {item.status}
                      </StatusBadge>
                    </td>
                    <td className="px-4 py-2.5 text-muted-foreground">
                      {item.review_route.replaceAll("_", " ")}
                    </td>
                    <td className="num px-4 py-2.5 text-muted-foreground">v{item.version}</td>
                    <td className="px-4 py-2.5 text-right">
                      <Link
                        to="/exceptions/$exceptionId"
                        params={{ exceptionId: item.id }}
                        aria-label={`Open ${item.synthetic_trade_id}`}
                        className="inline-flex size-10 cursor-pointer items-center justify-center rounded-md text-primary transition-colors hover:bg-accent"
                      >
                        <ChevronRight className="size-4" aria-hidden="true" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null}
      </Panel>
    </div>
  );
}
