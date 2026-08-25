import { z } from "zod";

export const demoRoles = ["analyst", "reviewer", "auditor", "administrator"] as const;
export type DemoRole = (typeof demoRoles)[number];

const exceptionSchema = z.object({
  id: z.string().uuid(),
  synthetic_trade_id: z.string(),
  exception_type: z.string(),
  severity: z.string(),
  status: z.string(),
  review_route: z.string(),
  explanation: z.string(),
  evidence: z.array(z.string()),
  suggested_actions: z.array(z.string()),
  created_at: z.string(),
  version: z.number().int().positive(),
});

const exceptionListSchema = z.object({
  items: z.array(exceptionSchema),
  total: z.number().int().nonnegative(),
  data_classification: z.literal("synthetic"),
});

const workflowSchema = z.object({
  id: z.string().uuid(),
  exception_id: z.string().uuid(),
  status: z.string(),
  steps: z.array(z.string()),
  proposal: z.string().nullable(),
  provider: z.string().nullable(),
  model: z.string().nullable(),
  resolution_applied: z.boolean(),
  version: z.string(),
});

const auditSchema = z.object({
  id: z.string().uuid(),
  event_type: z.string(),
  actor: z.string(),
  subject_id: z.string().uuid(),
  occurred_at: z.string(),
  summary: z.string(),
});

export type TradeException = z.infer<typeof exceptionSchema>;
export type Workflow = z.infer<typeof workflowSchema>;
export type AuditEvent = z.infer<typeof auditSchema>;
export type ReviewDecision = "approve" | "edit" | "reject" | "request_more_evidence" | "escalate";

const apiBase =
  (import.meta.env["VITE_API_BASE_URL"] as string | undefined) ?? "http://localhost:8000/api/v1";

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
  }
}

async function request(path: string, role: DemoRole, init?: RequestInit): Promise<unknown> {
  const response = await fetch(`${apiBase}${path}`, {
    ...init,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Demo-Role": role,
      ...init?.headers,
    },
  });
  if (!response.ok) {
    const problem = (await response.json().catch(() => null)) as { detail?: unknown } | null;
    const detail = typeof problem?.detail === "string" ? problem.detail : "Request failed.";
    throw new ApiError(detail, response.status);
  }
  return response.json();
}

export async function getExceptions(
  role: DemoRole,
  filters: { status?: string; severity?: string; search?: string } = {},
) {
  const query = new URLSearchParams();
  if (filters.status) query.set("status", filters.status);
  if (filters.severity) query.set("severity", filters.severity);
  if (filters.search) query.set("search", filters.search);
  const suffix = query.size ? `?${query}` : "";
  return exceptionListSchema.parse(await request(`/exceptions${suffix}`, role));
}

export async function getException(role: DemoRole, id: string) {
  return exceptionSchema.parse(await request(`/exceptions/${id}`, role));
}

export async function startWorkflow(role: DemoRole, exceptionId: string) {
  return workflowSchema.parse(
    await request(`/exceptions/${exceptionId}/workflows`, role, {
      method: "POST",
      headers: { "Idempotency-Key": crypto.randomUUID() },
    }),
  );
}

export async function approveWorkflow(
  role: DemoRole,
  workflowId: string,
  decision: ReviewDecision,
  expectedExceptionVersion: number,
  edit?: string,
) {
  return workflowSchema.parse(
    await request(`/workflows/${workflowId}/approvals`, role, {
      method: "POST",
      headers: { "Idempotency-Key": crypto.randomUUID() },
      body: JSON.stringify({
        decision,
        expected_exception_version: expectedExceptionVersion,
        ...(edit ? { edit } : {}),
      }),
    }),
  );
}

export async function getAuditEvents(role: DemoRole) {
  return z.array(auditSchema).parse(await request("/audit-events", role));
}
