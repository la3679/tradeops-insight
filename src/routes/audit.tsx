import { createFileRoute } from "@tanstack/react-router";
import { PlaceholderSection } from "@/components/PlaceholderSection";
import { PermissionDeniedState } from "@/components/primitives/StateBlocks";

const title = "Audit — TradeOps Copilot";
const description =
  "Placeholder audit record view for a synthetic trade-exception operations console.";

export const Route = createFileRoute("/audit")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
    ],
  }),
  component: AuditPage,
});

function AuditPage() {
  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-6">
      <PlaceholderSection
        title="Audit"
        summary="A record of console actions and reviewer decisions. Recording and retention are backend concerns and are not implemented in this change."
        plannedItems={[
          "Append-only action log with actor and timestamp",
          "Filter by queue item, actor, and action type",
          "Export for periodic review",
          "Role-scoped visibility",
        ]}
      />
      <div className="max-w-xl">
        {/* Demonstrates the permission-denied primitive; presentation only. */}
        <PermissionDeniedState resource="the full audit record" />
      </div>
    </div>
  );
}
