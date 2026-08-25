import { afterEach, describe, expect, it, vi } from "vitest";
import { ApiError, getException, getExceptions } from "./tradeops-api";

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
});
