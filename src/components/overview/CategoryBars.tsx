import type { CategoryBreakdown } from "@/data/overview";

export function CategoryBars({ items }: { readonly items: readonly CategoryBreakdown[] }) {
  return (
    <ul className="space-y-3">
      {items.map((item) => (
        <li key={item.category}>
          <div className="flex items-baseline justify-between gap-2">
            <span className="truncate text-xs text-foreground">{item.category}</span>
            <span className="num text-2xs text-muted-foreground">
              {item.count} · {item.share}%
            </span>
          </div>
          <div
            role="img"
            aria-label={`${item.category}: ${item.count} items, ${item.share} percent of the sample`}
            className="mt-1.5 h-1.5 w-full overflow-hidden rounded-full bg-muted"
          >
            <div className="h-full rounded-full bg-info" style={{ width: `${item.share}%` }} />
          </div>
        </li>
      ))}
    </ul>
  );
}
