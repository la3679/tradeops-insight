import { useQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";
import { ScrollText } from "lucide-react";
import {
  EmptyState,
  LoadingState,
  PermissionDeniedState,
} from "@/components/primitives/StateBlocks";
import { PageHeader } from "@/components/primitives/PageHeader";
import { Panel } from "@/components/primitives/Panel";
import { StatusBadge } from "@/components/primitives/StatusBadge";
import { useDemoRole } from "@/lib/demo-role";
import { ApiError, getAuditEvents } from "@/lib/tradeops-api";

export const Route = createFileRoute("/audit")({ component: AuditPage });

function AuditPage() {
  const { role } = useDemoRole();
  const query = useQuery({
    queryKey: ["audit", role],
    queryFn: () => getAuditEvents(role),
    retry: false,
  });
  const denied = query.error instanceof ApiError && query.error.status === 403;

  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-5">
      <PageHeader
        title="Audit explorer"
        summary="Append-only workflow, reviewer, and synthetic resolution events. Switch to auditor or administrator in the role selector to inspect them."
        meta={<StatusBadge tone="neutral">Role · {role}</StatusBadge>}
      />
      <Panel
        title="Application audit events"
        description="Newest first. Event content is safe metadata only."
        flush
      >
        {query.isPending ? <LoadingState label="Loading audit events" /> : null}
        {denied ? <PermissionDeniedState resource="the immutable audit record" /> : null}
        {query.data?.length === 0 ? (
          <EmptyState
            title="No audit events yet"
            description="Start and review a workflow to create the first immutable events."
          />
        ) : null}
        {query.data?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[52rem] text-left text-xs">
              <caption className="sr-only">Immutable synthetic application audit events</caption>
              <thead className="border-b border-border bg-muted/40 text-2xs uppercase tracking-wide text-muted-foreground">
                <tr>
                  <th className="px-4 py-2 font-medium">Event</th>
                  <th className="px-4 py-2 font-medium">Actor</th>
                  <th className="px-4 py-2 font-medium">Subject</th>
                  <th className="px-4 py-2 font-medium">Summary</th>
                  <th className="px-4 py-2 font-medium">Time</th>
                </tr>
              </thead>
              <tbody>
                {query.data.map((event) => (
                  <tr key={event.id} className="border-b border-border last:border-0">
                    <th scope="row" className="px-4 py-2.5 font-medium">
                      <span className="flex items-center gap-2">
                        <ScrollText className="size-3.5 text-info" aria-hidden="true" />
                        {event.event_type}
                      </span>
                    </th>
                    <td className="px-4 py-2.5 text-muted-foreground">{event.actor}</td>
                    <td className="num px-4 py-2.5 text-muted-foreground">
                      {event.subject_id.slice(0, 8)}
                    </td>
                    <td className="px-4 py-2.5 text-muted-foreground">{event.summary}</td>
                    <td className="num px-4 py-2.5 text-muted-foreground">
                      {new Date(event.occurred_at).toISOString()}
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
