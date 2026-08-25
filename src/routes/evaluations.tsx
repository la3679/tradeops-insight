import { createFileRoute } from "@tanstack/react-router";
import { CheckCircle2, FlaskConical, ShieldAlert } from "lucide-react";
import { MetricTile } from "@/components/primitives/MetricTile";
import { PageHeader } from "@/components/primitives/PageHeader";
import { Panel } from "@/components/primitives/Panel";
import { StatusBadge } from "@/components/primitives/StatusBadge";

export const Route = createFileRoute("/evaluations")({ component: EvaluationsPage });

const cases = [
  ["Normal resolution", "Deterministic", "Pass"],
  ["Ambiguous counterparty", "Escalation", "Pass"],
  ["Missing evidence", "Refusal", "Pass"],
  ["Contradictory memo", "Escalation", "Pass"],
  ["Malicious document", "Injection defense", "Pass"],
  ["Provider unavailable", "Fallback", "Pass"],
] as const;

function EvaluationsPage() {
  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-5">
      <PageHeader
        title="Evaluations"
        summary="Versioned golden cases for deterministic routing, evidence safety, provider failure, approvals, and escalation. Results below describe the checked mock baseline only."
        meta={<StatusBadge tone="info">Dataset · golden-v1</StatusBadge>}
      />
      <section aria-label="Evaluation summary" className="grid gap-3 sm:grid-cols-3">
        <MetricTile label="Golden cases" value="50" note="Versioned synthetic cases" />
        <MetricTile
          label="Mock baseline"
          value="Deterministic"
          note="No API key or model cost"
          tone="verified"
        />
        <MetricTile label="Last reviewed" value="2026-08-24" note="UTC fixture timestamp" />
      </section>
      <Panel
        title="Baseline coverage"
        description="Representative groups from the 50-case evaluation pack."
        flush
      >
        <div className="overflow-x-auto">
          <table className="w-full min-w-[38rem] text-left text-xs">
            <thead className="border-b border-border bg-muted/40 text-2xs uppercase tracking-wide text-muted-foreground">
              <tr>
                <th className="px-4 py-2 font-medium">Case group</th>
                <th className="px-4 py-2 font-medium">Expected behavior</th>
                <th className="px-4 py-2 font-medium">Baseline</th>
              </tr>
            </thead>
            <tbody>
              {cases.map(([name, behavior, result]) => (
                <tr key={name} className="border-b border-border last:border-0">
                  <th scope="row" className="px-4 py-2.5 font-medium">
                    {name}
                  </th>
                  <td className="px-4 py-2.5 text-muted-foreground">{behavior}</td>
                  <td className="px-4 py-2.5">
                    <StatusBadge tone="verified">
                      <CheckCircle2 aria-hidden="true" />
                      {result}
                    </StatusBadge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Panel>
      <div className="grid gap-4 md:grid-cols-2">
        <Panel title="Retrieval measures" description="Computed by the offline evaluation command.">
          <ul className="grid grid-cols-2 gap-2 text-xs text-muted-foreground">
            {[
              "Recall@k",
              "Mean reciprocal rank",
              "Citation precision",
              "Citation completeness",
              "Unsupported-claim rate",
              "Correct escalation rate",
            ].map((metric) => (
              <li key={metric} className="rounded-sm border border-border px-3 py-2">
                {metric}
              </li>
            ))}
          </ul>
        </Panel>
        <Panel title="Interpretation boundary" description="No production-quality claim is made.">
          <div className="flex gap-3">
            <ShieldAlert className="size-4 shrink-0 text-pending" aria-hidden="true" />
            <p className="text-xs leading-5 text-muted-foreground">
              Real-model evaluation is opt-in and must record provider, model, prompt version,
              temperature, tokens, cost, latency, and timestamp. The public demo reports only
              replayable mock behavior.
            </p>
          </div>
        </Panel>
      </div>
      <p className="flex items-center gap-2 text-2xs text-muted-foreground">
        <FlaskConical className="size-3.5" aria-hidden="true" /> Evaluation records are synthetic
        and independently authored.
      </p>
    </div>
  );
}
