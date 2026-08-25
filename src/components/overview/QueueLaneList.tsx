import { StatusBadge } from "@/components/primitives/StatusBadge";
import type { QueueLane } from "@/data/overview";

export function QueueLaneList({ lanes }: { readonly lanes: readonly QueueLane[] }) {
  return (
    <ul className="divide-y divide-border">
      {lanes.map((lane) => (
        <li
          key={lane.id}
          className="flex flex-wrap items-center justify-between gap-2 py-2.5 first:pt-0 last:pb-0"
        >
          <div className="min-w-0 flex-1">
            <p className="truncate text-xs font-medium text-foreground">{lane.name}</p>
            <p className="num text-2xs text-muted-foreground">{lane.open} open items</p>
          </div>
          <div className="flex shrink-0 items-center gap-1.5">
            <StatusBadge tone="pending">{lane.pending} pending</StatusBadge>
            <StatusBadge tone="verified">{lane.verified} verified</StatusBadge>
          </div>
        </li>
      ))}
    </ul>
  );
}
