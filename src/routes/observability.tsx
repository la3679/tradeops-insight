import { createFileRoute } from "@tanstack/react-router";
import { Activity, CheckCircle2, Clock3 } from "lucide-react";
import { PageHeader } from "@/components/primitives/PageHeader";
import { Panel } from "@/components/primitives/Panel";
import { StatusBadge } from "@/components/primitives/StatusBadge";

export const Route = createFileRoute("/observability")({ component: ObservabilityPage });

const services = [
  ["API", "FastAPI", "Healthy"],
  ["Worker", "Celery · concurrency 2", "Ready"],
  ["Database", "PostgreSQL 18", "Healthy"],
  ["Checkpoint store", "PostgreSQL", "Ready"],
  ["Queue", "Redis 8", "Healthy"],
  ["Telemetry", "OTLP collector", "Receiving"],
] as const;

function ObservabilityPage() {
  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-5">
      <PageHeader
        title="Observability and health"
        summary="Safe operational metadata for the local synthetic stack. Logs exclude prompts, secrets, and full evidence payloads."
        meta={<StatusBadge tone="verified">Local stack healthy</StatusBadge>}
      />
      <div className="grid gap-4 lg:grid-cols-[1fr_.8fr]">
        <Panel
          title="Service health"
          description="Reference snapshot from the verified Compose environment."
        >
          <ul className="divide-y divide-border">
            {services.map(([name, detail, state]) => (
              <li
                key={name}
                className="flex items-center justify-between gap-4 py-2.5 first:pt-0 last:pb-0"
              >
                <div>
                  <p className="text-xs font-semibold">{name}</p>
                  <p className="text-2xs text-muted-foreground">{detail}</p>
                </div>
                <StatusBadge tone="verified">
                  <CheckCircle2 aria-hidden="true" />
                  {state}
                </StatusBadge>
              </li>
            ))}
          </ul>
        </Panel>
        <Panel
          title="Telemetry coverage"
          description="OpenTelemetry spans exported through OTLP/gRPC."
        >
          <ul className="space-y-2 text-xs text-muted-foreground">
            {[
              "HTTP request and response status",
              "Workflow and checkpoint boundaries",
              "Retrieval and provider metadata",
              "Safe tool latency and error class",
              "Request, trace, and workflow correlation IDs",
            ].map((item) => (
              <li key={item} className="flex gap-2">
                <Activity className="mt-0.5 size-3.5 shrink-0 text-info" aria-hidden="true" />
                {item}
              </li>
            ))}
          </ul>
        </Panel>
      </div>
      <Panel
        title="Recent trace example"
        description="Illustrative safe metadata, not a live performance claim."
      >
        <div className="grid gap-3 sm:grid-cols-4">
          {[
            ["Request", "GET /api/v1/exceptions"],
            ["Trace", "8f41…d29c"],
            ["Status", "200"],
            ["Environment", "local"],
          ].map(([label, value]) => (
            <div key={label} className="rounded-md border border-border bg-muted/30 p-3">
              <p className="text-2xs uppercase tracking-wide text-muted-foreground">{label}</p>
              <p className="num mt-1 text-xs font-semibold">{value}</p>
            </div>
          ))}
        </div>
      </Panel>
      <p className="flex items-center gap-2 text-2xs text-muted-foreground">
        <Clock3 className="size-3.5" aria-hidden="true" /> Durations are recorded per run; this
        screen makes no latency guarantee.
      </p>
    </div>
  );
}
