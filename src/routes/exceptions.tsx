import { createFileRoute } from "@tanstack/react-router";
import { PlaceholderSection } from "@/components/PlaceholderSection";

const title = "Exception Queue — TradeOps Copilot";
const description =
  "Placeholder triage queue for synthetic fixed-income trade exceptions in an educational operations console.";

export const Route = createFileRoute("/exceptions")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
    ],
  }),
  component: ExceptionsPage,
});

function ExceptionsPage() {
  return (
    <PlaceholderSection
      title="Exception Queue"
      summary="Triage list for individual synthetic trade exceptions. Filtering, detail views, and reviewer actions are out of scope for this frontend foundation."
      plannedItems={[
        "Sortable queue table with severity and review state columns",
        "Detail drawer showing the synthetic trade record and break fields",
        "Saved views per desk lane",
        "Reviewer notes captured for the audit record",
      ]}
    />
  );
}
