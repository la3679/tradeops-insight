import { createFileRoute } from "@tanstack/react-router";
import { PlaceholderSection } from "@/components/PlaceholderSection";

const title = "Evaluations — TradeOps Copilot";
const description =
  "Placeholder evaluation workspace for reviewing assistant behaviour against synthetic exception test cases.";

export const Route = createFileRoute("/evaluations")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
    ],
  }),
  component: EvaluationsPage,
});

function EvaluationsPage() {
  return (
    <PlaceholderSection
      title="Evaluations"
      summary="Where curated test cases and their reviewed outcomes will be listed. No scores, benchmarks, or accuracy figures are presented in this build."
      plannedItems={[
        "Test case list with expected reviewer outcome",
        "Run history with human-labelled results",
        "Diff view between two runs of the same case",
        "Export of a review pack for offline sign-off",
      ]}
    />
  );
}
