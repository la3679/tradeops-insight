import { createFileRoute } from "@tanstack/react-router";
import { Database, FileCheck2, Search, ShieldAlert } from "lucide-react";
import { PageHeader } from "@/components/primitives/PageHeader";
import { Panel } from "@/components/primitives/Panel";
import { StatusBadge } from "@/components/primitives/StatusBadge";
import { Input } from "@/components/ui/input";

export const Route = createFileRoute("/knowledge")({ component: KnowledgePage });

const stages = [
  "Source registration and provenance",
  "Safe extraction and normalization",
  "Content hash and deduplication",
  "Overlapping semantic chunks",
  "Deterministic embedding and FAISS index",
  "Filtered retrieval and citation gate",
] as const;

const sources = [
  ["Synthetic operations policies", "30 documents", "Local · version 1.0"],
  ["GLEIF API sample", "1 transformed row", "Hash verified"],
  ["SEC EDGAR sample", "1 transformed row", "Hash verified"],
  ["U.S. Treasury auction sample", "1 transformed row", "Hash verified"],
] as const;

function KnowledgePage() {
  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-5">
      <PageHeader
        title="Knowledge base"
        summary="Synthetic playbooks and minimal public-reference fixtures used for grounded investigation evidence. Retrieved content cannot authorize tools or redefine policy."
        meta={<StatusBadge tone="verified">Offline index ready</StatusBadge>}
      />
      <Panel
        title="Search indexed evidence"
        description="Search is local, deterministic, and metadata-filtered."
      >
        <label className="grid max-w-2xl gap-1.5 text-xs font-medium">
          Evidence query
          <span className="relative">
            <Search
              className="pointer-events-none absolute top-2.5 left-3 size-4 text-muted-foreground"
              aria-hidden="true"
            />
            <Input className="pl-9" placeholder="Settlement-date review policy" />
          </span>
        </label>
      </Panel>
      <div className="grid gap-4 lg:grid-cols-[1fr_.8fr]">
        <Panel
          title="Registered sources"
          description="Public sources enrich reference context; they never supply trades."
        >
          <ul className="divide-y divide-border">
            {sources.map(([name, count, state]) => (
              <li
                key={name}
                className="flex items-center justify-between gap-4 py-3 first:pt-0 last:pb-0"
              >
                <div className="flex min-w-0 items-center gap-3">
                  <FileCheck2 className="size-4 shrink-0 text-verified" aria-hidden="true" />
                  <div>
                    <p className="text-xs font-semibold">{name}</p>
                    <p className="text-2xs text-muted-foreground">{count}</p>
                  </div>
                </div>
                <StatusBadge tone="verified">{state}</StatusBadge>
              </li>
            ))}
          </ul>
        </Panel>
        <Panel
          title="Ingestion pipeline"
          description="Every stage is replayable without internet access."
        >
          <ol className="space-y-2">
            {stages.map((stage, index) => (
              <li key={stage} className="flex items-center gap-3 text-xs">
                <span className="num flex size-6 items-center justify-center rounded-full bg-muted text-2xs font-semibold">
                  {index + 1}
                </span>
                {stage}
              </li>
            ))}
          </ol>
        </Panel>
      </div>
      <section className="flex items-start gap-3 rounded-md border border-pending/30 bg-pending-subtle p-4">
        <ShieldAlert className="mt-0.5 size-4 shrink-0 text-pending" aria-hidden="true" />
        <div>
          <h2 className="text-xs font-semibold">Adversarial evidence boundary</h2>
          <p className="mt-1 text-xs leading-5 text-muted-foreground">
            Prompt-like instructions remain visible for audit but force escalation. The model
            receives no shell, network, arbitrary database, or code-execution tool.
          </p>
        </div>
      </section>
      <p className="flex items-center gap-2 text-2xs text-muted-foreground">
        <Database className="size-3.5" aria-hidden="true" /> Vector metadata maps back to relational
        document and chunk IDs.
      </p>
    </div>
  );
}
