import { afterEach, describe, expect, it, vi } from "vitest";
import {
  ApiError,
  approveWorkflow,
  getAuditEvents,
  getException,
  getExceptions,
  startWorkflow,
} from "./tradeops-api";

const exception = {
  id: "34036df2-cdf9-5e57-97d4-04234004c797",
  synthetic_trade_id: "TRD-DEMO-000001",
  exception_type: "currency_mismatch",
  severity: "high",
  status: "open",
  review_route: "review_correction",
  explanation: "Synthetic deterministic mismatch.",
  evidence: ["trade=EUR", "reference=USD"],
  suggested_actions: ["Review evidence."],
  created_at: "2026-01-15T00:00:00Z",
  version: 1,
};

const workflow = {
  id: "12aecfaf-a72c-5481-8e4b-eb52299817ab",
  exception_id: exception.id,
  status: "review_required",
  steps: ["intake_validation"],
  proposal: "Review the synthetic mismatch.",
  provider: "mock",
  model: "deterministic-v1",
  resolution_applied: false,
  version: "workflow-v1",
};

afterEach(() => vi.unstubAllGlobals());

describe("typed TradeOps API client", () => {
  it("validates queue responses and sends the selected role", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(
        new Response(
          JSON.stringify({ items: [exception], total: 1, data_classification: "synthetic" }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ),
      );
    vi.stubGlobal("fetch", fetchMock);

    const result = await getExceptions("auditor", { status: "open", search: "currency" });

    expect(result.items[0]?.synthetic_trade_id).toBe("TRD-DEMO-000001");
    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining("status=open&search=currency"),
      expect.objectContaining({ headers: expect.objectContaining({ "X-Demo-Role": "auditor" }) }),
    );
  });

  it("rejects malformed backend data at the browser boundary", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValue(
          new Response(JSON.stringify({ ...exception, version: "one" }), { status: 200 }),
        ),
    );

    await expect(getException("analyst", exception.id)).rejects.toThrow();
  });

  it("surfaces RFC problem details as a typed API error", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ detail: "Role denied." }), {
          status: 403,
          headers: { "Content-Type": "application/problem+json" },
        }),
      ),
    );

    await expect(getException("analyst", exception.id)).rejects.toEqual(
      new ApiError("Role denied.", 403),
    );
  });

  it("builds every queue filter and supports an unfiltered request", async () => {
    const fetchMock = vi.fn().mockImplementation(() =>
      Promise.resolve(
        new Response(JSON.stringify({ items: [], total: 0, data_classification: "synthetic" }), {
          status: 200,
        }),
      ),
    );
    vi.stubGlobal("fetch", fetchMock);

    await getExceptions("analyst");
    await getExceptions("analyst", { severity: "high" });

    expect(fetchMock.mock.calls[0]?.[0]).toBe("http://localhost:8000/api/v1/exceptions");
    expect(fetchMock.mock.calls[1]?.[0]).toContain("severity=high");
  });

  it("runs workflow, reviewed edit, and audit contracts with idempotency headers", async () => {
    const audit = {
      id: "b6f0d71f-a895-5f9b-a0d4-1f06b684cbf1",
      event_type: "workflow.started.v1",
      actor: "demo:analyst",
      subject_id: exception.id,
      occurred_at: "2026-01-15T00:00:00Z",
      summary: "Workflow paused for review",
    };
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(workflow), { status: 200 }))
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({ ...workflow, status: "resolved", resolution_applied: true }),
          {
            status: 200,
          },
        ),
      )
      .mockResolvedValueOnce(new Response(JSON.stringify([audit]), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);

    expect((await startWorkflow("analyst", exception.id)).provider).toBe("mock");
    expect((await approveWorkflow("reviewer", workflow.id, "edit", 1, "currency=USD")).status).toBe(
      "resolved",
    );
    expect(await getAuditEvents("auditor")).toHaveLength(1);
    expect(fetchMock.mock.calls[0]?.[1]).toEqual(
      expect.objectContaining({
        method: "POST",
        headers: expect.objectContaining({ "Idempotency-Key": expect.any(String) }),
      }),
    );
    expect(fetchMock.mock.calls[1]?.[1]?.body).toContain('"edit":"currency=USD"');
  });

  it("uses a safe fallback when an error response is not JSON", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("not-json", { status: 500 })));

    await expect(getException("analyst", exception.id)).rejects.toEqual(
      new ApiError("Request failed.", 500),
    );
  });
});
