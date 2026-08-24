import { createFileRoute } from "@tanstack/react-router";
import { PlaceholderSection } from "@/components/PlaceholderSection";

const title = "Knowledge — TradeOps Copilot";
const description =
  "Placeholder reference library for investigation playbooks used in a synthetic trade-exception console.";

export const Route = createFileRoute("/knowledge")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
    ],
  }),
  component: KnowledgePage,
});

function KnowledgePage() {
  return (
    <PlaceholderSection
      title="Knowledge"
      summary="Reference notes and investigation playbooks that describe how a break category is examined. Content authoring is a later change."
      plannedItems={[
        "Playbook documents grouped by exception category",
        "Search across reference notes",
        "Version and last-reviewed metadata per document",
        "Links from a queue item to the relevant playbook",
      ]}
    />
  );
}
