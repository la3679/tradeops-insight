import { createFileRoute } from "@tanstack/react-router";
import { Database, LockKeyhole, ServerCog } from "lucide-react";
import { PageHeader } from "@/components/primitives/PageHeader";
import { Panel } from "@/components/primitives/Panel";
import { PermissionDeniedState } from "@/components/primitives/StateBlocks";
import { StatusBadge } from "@/components/primitives/StatusBadge";
import { useDemoRole } from "@/lib/demo-role";

export const Route = createFileRoute("/settings")({ component: SettingsPage });

const sources = [
  ["GLEIF", "https://api.gleif.org/api/v1/lei-records", "Fixture only"],
  ["SEC EDGAR", "https://data.sec.gov/submissions/", "Fixture only"],
  ["U.S. Treasury", "https://api.fiscaldata.treasury.gov/", "Fixture only"],
] as const;

function SettingsPage() {
  const { role } = useDemoRole();
  const isAdmin = role === "administrator";
  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-5">
      <PageHeader
        title="Settings and sources"
        summary="Administrative source metadata and safe local runtime configuration. Secrets and credentials are never rendered in the browser."
        meta={<StatusBadge tone="neutral">Role · {role}</StatusBadge>}
      />
      {!isAdmin ? (
        <PermissionDeniedState resource="administrator source configuration" />
      ) : (
        <div className="grid gap-4 lg:grid-cols-[1fr_.75fr]">
          <Panel
            title="Public reference sources"
            description="Network synchronization is opt-in; CI uses hash-verified fixtures."
          >
            <ul className="divide-y divide-border">
              {sources.map(([name, url, mode]) => (
                <li key={name} className="py-3 first:pt-0 last:pb-0">
                  <div className="flex items-center justify-between gap-3">
                    <p className="text-xs font-semibold">{name}</p>
                    <StatusBadge tone="verified">{mode}</StatusBadge>
                  </div>
                  <p className="mt-1 break-all text-2xs text-muted-foreground">{url}</p>
                </li>
              ))}
            </ul>
          </Panel>
          <Panel
            title="Runtime policy"
            description="Configuration resolved by the backend process."
          >
            <dl className="space-y-3 text-xs">
              <div className="flex gap-3">
                <ServerCog className="size-4 shrink-0 text-info" aria-hidden="true" />
                <div>
                  <dt className="font-semibold">Model mode</dt>
                  <dd className="text-muted-foreground">Mock provider · deterministic fallback</dd>
                </div>
              </div>
              <div className="flex gap-3">
                <Database className="size-4 shrink-0 text-info" aria-hidden="true" />
                <div>
                  <dt className="font-semibold">Persistence</dt>
                  <dd className="text-muted-foreground">PostgreSQL + durable checkpoints</dd>
                </div>
              </div>
              <div className="flex gap-3">
                <LockKeyhole className="size-4 shrink-0 text-info" aria-hidden="true" />
                <div>
                  <dt className="font-semibold">Identity</dt>
                  <dd className="text-muted-foreground">
                    Local demo role selector; OIDC required in production
                  </dd>
                </div>
              </div>
            </dl>
          </Panel>
        </div>
      )}
      <Panel
        title="Personal display preferences"
        description="Presentation settings do not alter authorization or business rules."
      >
        <div className="grid gap-3 sm:grid-cols-3">
          {["Compact table density", "UTC timestamps", "Reduced motion respected"].map((item) => (
            <div
              key={item}
              className="rounded-md border border-border bg-muted/30 px-3 py-2.5 text-xs"
            >
              {item}
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
}
