import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/primitives/PageHeader";
import { Panel } from "@/components/primitives/Panel";
import { StatusBadge } from "@/components/primitives/StatusBadge";

const title = "About & Disclaimer — TradeOps Copilot";
const description =
  "TradeOps Copilot is an independent educational portfolio project for investigating synthetic fixed-income trade exceptions. No affiliation, no trade execution.";

export const Route = createFileRoute("/about")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
    ],
  }),
  component: AboutPage,
});

const scopeIncluded = [
  "Application shell, navigation, and route structure",
  "Design tokens and reusable presentation components",
  "An Overview screen built from a fixed synthetic fixture",
  "Loading, empty, and permission-denied state primitives",
] as const;

const scopeExcluded = [
  "Backend services, database, or persistence",
  "Authentication and authorization enforcement",
  "Financial, settlement, or break-classification rules",
  "Model calls, external APIs, and secret handling",
] as const;

function AboutPage() {
  return (
    <div className="mx-auto flex w-full max-w-4xl flex-col gap-6">
      <PageHeader
        title="About TradeOps Copilot"
        summary="An independent educational portfolio project: an operations console for investigating synthetic fixed-income trade exceptions."
        meta={
          <div className="flex flex-wrap gap-2">
            <StatusBadge tone="info">Educational portfolio</StatusBadge>
            <StatusBadge tone="neutral">Synthetic data only</StatusBadge>
            <StatusBadge tone="neutral">No trade execution</StatusBadge>
          </div>
        }
      />

      {/* Persistent, visible disclaimer. Do not remove or collapse. */}
      <section
        aria-labelledby="disclaimer-heading"
        className="rounded-md border border-pending/40 bg-pending-subtle px-4 py-4"
      >
        <h2
          id="disclaimer-heading"
          className="text-sm font-semibold text-pending-foreground"
        >
          Disclaimer
        </h2>
        <div className="mt-2 space-y-2 text-xs leading-relaxed text-pending-foreground">
          <p>
            TradeOps Copilot is a personal, independent portfolio project built for
            learning and demonstration. It is <strong>not affiliated with, endorsed
            by, or representative of</strong> any bank, broker, exchange, asset
            manager, or other financial institution.
          </p>
          <p>
            The application <strong>does not execute, route, confirm, or settle
            trades</strong> and does not connect to any trading or settlement system.
            Every instrument, counterparty, figure, and exception shown is{" "}
            <strong>synthetic</strong> or derived from public reference material.
          </p>
          <p>
            Nothing here is investment, legal, accounting, or operational advice, and
            no claim is made about accuracy, completeness, latency, or fitness for any
            operational or regulatory purpose.
          </p>
        </div>
      </section>

      <div className="grid gap-4 md:grid-cols-2">
        <Panel title="In scope for this build" description="Frontend foundation only.">
          <ul className="space-y-2">
            {scopeIncluded.map((item) => (
              <li key={item} className="flex gap-2 text-xs text-muted-foreground">
                <span
                  aria-hidden="true"
                  className="mt-1.5 size-1 shrink-0 rounded-full bg-verified"
                />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </Panel>

        <Panel
          title="Deliberately out of scope"
          description="Owned and reviewed outside this frontend."
        >
          <ul className="space-y-2">
            {scopeExcluded.map((item) => (
              <li key={item} className="flex gap-2 text-xs text-muted-foreground">
                <span
                  aria-hidden="true"
                  className="mt-1.5 size-1 shrink-0 rounded-full bg-border"
                />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </Panel>
      </div>

      <Panel title="How to read the interface" description="Conventions used throughout.">
        <dl className="grid gap-3 sm:grid-cols-3">
          <div>
            <dt className="flex items-center gap-2">
              <StatusBadge tone="verified">Verified</StatusBadge>
            </dt>
            <dd className="mt-1.5 text-xs text-muted-foreground">
              A person confirmed the sample outcome. Teal is used only for this state.
            </dd>
          </div>
          <div>
            <dt className="flex items-center gap-2">
              <StatusBadge tone="pending">Pending</StatusBadge>
            </dt>
            <dd className="mt-1.5 text-xs text-muted-foreground">
              Awaiting review. Amber signals waiting, not failure.
            </dd>
          </div>
          <div>
            <dt className="flex items-center gap-2">
              <StatusBadge tone="severe">High</StatusBadge>
            </dt>
            <dd className="mt-1.5 text-xs text-muted-foreground">
              Reserved for genuine high severity in the fixture — never decoration.
            </dd>
          </div>
        </dl>
      </Panel>
    </div>
  );
}
