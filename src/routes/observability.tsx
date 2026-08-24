import { createFileRoute } from "@tanstack/react-router";
import { PlaceholderSection } from "@/components/PlaceholderSection";

const title = "Observability — TradeOps Copilot";
const description =
  "Placeholder observability view for investigation session traces in a synthetic operations console.";

export const Route = createFileRoute("/observability")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
    ],
  }),
  component: ObservabilityPage,
});

function ObservabilityPage() {
  return (
    <PlaceholderSection
      title="Observability"
      summary="Traces and run history for investigation sessions. Instrumentation is owned outside this frontend, so nothing is wired up here."
      plannedItems={[
        "Session timeline with step-level detail",
        "Filter by desk lane, category, and outcome",
        "Error and retry visibility for long-running steps",
        "Link from a trace back to the originating queue item",
      ]}
    />
  );
}
