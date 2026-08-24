import { createFileRoute } from "@tanstack/react-router";
import { PlaceholderSection } from "@/components/PlaceholderSection";

const title = "Settings — TradeOps Copilot";
const description =
  "Placeholder workspace settings for display and queue preferences in an educational operations console.";

export const Route = createFileRoute("/settings")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
    ],
  }),
  component: SettingsPage,
});

function SettingsPage() {
  return (
    <PlaceholderSection
      title="Settings"
      summary="Display and queue preferences. No credentials, keys, or account management appear in this console."
      plannedItems={[
        "Density and table column preferences",
        "Default desk lane for the queue view",
        "Notification preferences for pending reviews",
        "Accessibility options such as reduced motion",
      ]}
    />
  );
}
