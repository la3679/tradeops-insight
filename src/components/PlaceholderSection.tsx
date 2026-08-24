import { PageHeader } from "@/components/primitives/PageHeader";
import { Panel } from "@/components/primitives/Panel";
import { EmptyState } from "@/components/primitives/StateBlocks";

export type PlaceholderSectionProps = {
  readonly title: string;
  readonly summary: string;
  readonly plannedItems: readonly string[];
};

/**
 * Structural placeholder for a route that is scoped for a later change.
 * Intentionally makes no claims about behaviour that does not exist yet.
 */
export function PlaceholderSection({
  title,
  summary,
  plannedItems,
}: PlaceholderSectionProps) {
  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-6">
      <PageHeader title={title} summary={summary} />

      <div className="grid gap-4 lg:grid-cols-3">
        <Panel
          title="Not yet implemented"
          description="This route exists so navigation and layout can be reviewed."
          className="lg:col-span-2"
        >
          <EmptyState
            title="No content in this build"
            description="This screen is a placeholder in the frontend foundation. Data and logic arrive in a later, separately reviewed change."
          />
        </Panel>

        <Panel title="Planned scope" description="Reviewed before implementation.">
          <ul className="space-y-2">
            {plannedItems.map((item) => (
              <li key={item} className="flex gap-2 text-xs text-muted-foreground">
                <span aria-hidden="true" className="mt-1.5 size-1 shrink-0 rounded-full bg-border" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </Panel>
      </div>
    </div>
  );
}
