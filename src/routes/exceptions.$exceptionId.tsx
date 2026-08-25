import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link, createFileRoute } from "@tanstack/react-router";
import {
  ArrowLeft,
  Bot,
  CheckCircle2,
  Circle,
  ExternalLink,
  FileCheck2,
  GitBranch,
  ShieldCheck,
} from "lucide-react";
import { useState } from "react";
import { LoadingState, PermissionDeniedState } from "@/components/primitives/StateBlocks";
import { Panel } from "@/components/primitives/Panel";
import { StatusBadge } from "@/components/primitives/StatusBadge";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useDemoRole } from "@/lib/demo-role";
import {
  ApiError,
  approveWorkflow,
  getException,
  startWorkflow,
  type ReviewDecision,
  type Workflow,
} from "@/lib/tradeops-api";

export const Route = createFileRoute("/exceptions/$exceptionId")({
  component: ExceptionDetailPage,
});

const decisionLabels: Record<ReviewDecision, string> = {
  approve: "Approve",
  edit: "Approve edit",
  reject: "Reject",
  request_more_evidence: "Request evidence",
  escalate: "Escalate",
};

function ExceptionDetailPage() {
  const { exceptionId } = Route.useParams();
  const { role } = useDemoRole();
  const queryClient = useQueryClient();
  const [workflow, setWorkflow] = useState<Workflow | null>(null);
  const [edit, setEdit] = useState("");
  const exceptionQuery = useQuery({
    queryKey: ["exception", role, exceptionId],
    queryFn: () => getException(role, exceptionId),
  });
  const start = useMutation({
    mutationFn: () => startWorkflow(role, exceptionId),
    onSuccess: setWorkflow,
  });
  const decide = useMutation({
    mutationFn: (decision: ReviewDecision) => {
      if (!workflow || !exceptionQuery.data) throw new Error("Workflow is not ready for review.");
      return approveWorkflow(
        role,
        workflow.id,
        decision,
        exceptionQuery.data.version,
        decision === "edit" ? edit : undefined,
      );
    },
    onSuccess: (updated) => {
      setWorkflow(updated);
      void queryClient.invalidateQueries({ queryKey: ["exception"] });
      void queryClient.invalidateQueries({ queryKey: ["exceptions"] });
    },
  });

  if (exceptionQuery.isPending) return <LoadingState label="Loading investigation workspace" />;
  if (exceptionQuery.isError) {
    return (
      <div role="alert" className="rounded-md border border-severe/30 bg-severe-subtle p-5">
        <h1 className="text-base font-semibold">Exception detail unavailable</h1>
        <p className="mt-1 text-sm text-muted-foreground">{exceptionQuery.error.message}</p>
        <Link
          to="/exceptions"
          className="mt-4 inline-flex cursor-pointer text-sm font-semibold underline"
        >
          Return to queue
        </Link>
      </div>
    );
  }

  const item = exceptionQuery.data;
  const canStart = role === "analyst" || role === "reviewer" || role === "administrator";
  const canReview = role === "reviewer" || role === "administrator";
  const mutationError = start.error ?? decide.error;

  return (
    <div className="mx-auto flex w-full max-w-[96rem] flex-col gap-4">
      <nav aria-label="Breadcrumb">
        <Link
          to="/exceptions"
          className="inline-flex min-h-10 cursor-pointer items-center gap-2 text-xs font-medium text-muted-foreground transition-colors hover:text-foreground"
        >
          <ArrowLeft className="size-4" aria-hidden="true" /> Exception queue
        </Link>
      </nav>

      <header className="flex flex-col justify-between gap-4 border-b border-border pb-4 lg:flex-row lg:items-start">
        <div>
          <div className="flex flex-wrap items-center gap-2">
            <StatusBadge tone={item.severity === "high" ? "severe" : "pending"}>
              {item.severity}
            </StatusBadge>
            <StatusBadge tone={item.status === "escalated" ? "severe" : "pending"}>
              {item.status}
            </StatusBadge>
            <StatusBadge tone="info">Synthetic</StatusBadge>
          </div>
          <h1 className="mt-3 text-xl font-semibold tracking-tight text-foreground sm:text-2xl">
            {item.exception_type.replaceAll("_", " ")}
          </h1>
          <p className="num mt-1 text-xs text-muted-foreground">
            {item.synthetic_trade_id} · Exception {item.id.slice(0, 8)} · Version {item.version}
          </p>
        </div>
        <Button
          type="button"
          disabled={!canStart || start.isPending || Boolean(workflow)}
          onClick={() => start.mutate()}
          className="min-h-11"
        >
          <GitBranch aria-hidden="true" />
          {workflow ? "Workflow started" : start.isPending ? "Starting…" : "Start investigation"}
        </Button>
      </header>

      {mutationError ? (
        <div
          role="alert"
          className="rounded-md border border-severe/30 bg-severe-subtle px-4 py-3 text-sm"
        >
          {mutationError instanceof ApiError
            ? mutationError.message
            : "The workflow request failed."}
        </div>
      ) : null}

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1.15fr)_minmax(20rem,.85fr)_22rem]">
        <div className="flex min-w-0 flex-col gap-4">
          <Panel
            title="Trade and reference comparison"
            description="Original synthetic payload compared with independently observed fixture facts."
          >
            <dl className="divide-y divide-border text-xs">
              {item.evidence.map((fact) => {
                const [field, ...valueParts] = fact.split("=");
                return (
                  <div
                    key={fact}
                    className="grid grid-cols-[minmax(8rem,.55fr)_1fr] gap-3 py-2 first:pt-0 last:pb-0"
                  >
                    <dt className="font-medium text-muted-foreground">
                      {(field ?? "fact").replaceAll("_", " ")}
                    </dt>
                    <dd className="num break-words font-medium text-foreground">
                      {valueParts.join("=") || fact}
                    </dd>
                  </div>
                );
              })}
            </dl>
          </Panel>

          <Panel
            title="Detected mismatch"
            description={`Rule route: ${item.review_route.replaceAll("_", " ")}`}
          >
            <p className="text-sm leading-6 text-foreground">{item.explanation}</p>
            <div className="mt-4 rounded-md border border-pending/30 bg-pending-subtle px-3 py-2.5">
              <p className="text-xs font-semibold text-pending-foreground">
                Deterministic validation
              </p>
              <p className="mt-1 text-xs text-pending-foreground">
                Finding reproduced offline from versioned fixed-precision and reference checks. No
                model calculated the mismatch.
              </p>
            </div>
          </Panel>

          <Panel
            title="Suggested next actions"
            description="Suggestions never authorize a state change."
          >
            <ol className="space-y-3">
              {item.suggested_actions.map((action, index) => (
                <li key={action} className="flex gap-3 text-sm">
                  <span className="num flex size-6 shrink-0 items-center justify-center rounded-full bg-muted text-2xs font-semibold">
                    {index + 1}
                  </span>
                  <span className="pt-0.5 text-muted-foreground">{action}</span>
                </li>
              ))}
            </ol>
          </Panel>
        </div>

        <div className="flex min-w-0 flex-col gap-4">
          <Panel
            title="Evidence and citations"
            description="Retrieved text is always treated as untrusted evidence."
          >
            <article className="rounded-md border border-border bg-muted/35 p-3">
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-2">
                  <FileCheck2 className="size-4 text-verified" aria-hidden="true" />
                  <h3 className="text-xs font-semibold">Deterministic rule evidence</h3>
                </div>
                <StatusBadge tone="verified">Grounded</StatusBadge>
              </div>
              <p className="mt-2 text-xs leading-5 text-muted-foreground">
                {item.evidence.join(" · ")}
              </p>
              <a
                href="/about"
                className="mt-3 inline-flex min-h-10 cursor-pointer items-center gap-1.5 text-xs font-semibold text-primary underline-offset-4 hover:underline"
              >
                Evidence handling policy <ExternalLink className="size-3" aria-hidden="true" />
              </a>
            </article>
          </Panel>

          <Panel title="Agent proposal" description="Mock provider is the zero-cost local default.">
            {workflow?.proposal ? (
              <div>
                <div className="flex items-center gap-2">
                  <Bot className="size-4 text-info" aria-hidden="true" />
                  <StatusBadge tone="info">
                    {workflow.provider} · {workflow.model}
                  </StatusBadge>
                </div>
                <p className="mt-3 text-sm leading-6">{workflow.proposal}</p>
                <p className="mt-3 text-xs text-muted-foreground">
                  Confidence gate passed only because deterministic evidence was present. Human
                  review is still mandatory.
                </p>
              </div>
            ) : (
              <p className="text-xs text-muted-foreground">
                Start an investigation to generate a bounded proposal.
              </p>
            )}
          </Panel>

          <Panel title="Workflow timeline" description="Checkpoint-safe nodes in execution order.">
            <ol className="space-y-0">
              {(workflow?.steps ?? ["intake_validation"]).map((step, index, steps) => (
                <li key={step} className="relative flex gap-3 pb-4 last:pb-0">
                  {index < steps.length - 1 ? (
                    <span
                      aria-hidden="true"
                      className="absolute top-4 bottom-0 left-[7px] w-px bg-border"
                    />
                  ) : null}
                  {workflow ? (
                    <CheckCircle2
                      className="relative z-10 mt-0.5 size-4 shrink-0 bg-surface text-verified"
                      aria-hidden="true"
                    />
                  ) : (
                    <Circle
                      className="relative z-10 mt-0.5 size-4 shrink-0 bg-surface text-muted-foreground"
                      aria-hidden="true"
                    />
                  )}
                  <div>
                    <p className="text-xs font-medium text-foreground">
                      {step.replaceAll("_", " ")}
                    </p>
                    <p className="text-2xs text-muted-foreground">
                      Completed with safe metadata capture
                    </p>
                  </div>
                </li>
              ))}
            </ol>
          </Panel>
        </div>

        <aside aria-label="Reviewer controls" className="min-w-0">
          <Panel
            title="Human review"
            description="Every material demo-state action pauses here."
            className="xl:sticky xl:top-4"
          >
            {!canReview ? (
              <PermissionDeniedState resource="approval actions" className="py-6" />
            ) : !workflow ? (
              <p className="text-xs leading-5 text-muted-foreground">
                Start the workflow first. The review controls activate only after the confidence and
                citation gate pauses the graph.
              </p>
            ) : workflow.resolution_applied ? (
              <div className="rounded-md border border-verified/30 bg-verified-subtle p-3">
                <div className="flex items-center gap-2 text-sm font-semibold">
                  <ShieldCheck className="size-4 text-verified" aria-hidden="true" /> Resolution
                  applied
                </div>
                <p className="mt-1 text-xs text-muted-foreground">
                  Only local synthetic demonstration state changed. The audit record is immutable.
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <label className="grid gap-1.5 text-xs font-medium">
                  Optional reviewed edit
                  <Textarea
                    value={edit}
                    onChange={(event) => setEdit(event.target.value)}
                    placeholder="Example: currency=USD"
                    maxLength={500}
                  />
                  <span className="font-normal text-muted-foreground">
                    Only allowlisted synthetic fields are accepted by the backend tool.
                  </span>
                </label>
                <div className="grid gap-2">
                  {(Object.keys(decisionLabels) as ReviewDecision[]).map((decision) => (
                    <Button
                      key={decision}
                      type="button"
                      variant={decision === "approve" ? "default" : "outline"}
                      disabled={decide.isPending || (decision === "edit" && !edit.trim())}
                      onClick={() => decide.mutate(decision)}
                      className="min-h-11 justify-start"
                    >
                      {decisionLabels[decision]}
                    </Button>
                  ))}
                </div>
              </div>
            )}
          </Panel>
        </aside>
      </div>
    </div>
  );
}
