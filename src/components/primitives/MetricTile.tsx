import { cn } from "@/lib/utils";
import { StatusBadge, type StatusBadgeProps } from "./StatusBadge";

export type MetricTileProps = {
  readonly label: string;
  readonly value: string;
  readonly unit?: string | undefined;
  readonly note: string;
  readonly tone?: StatusBadgeProps["tone"] | undefined;
  readonly badge?: string | undefined;
  readonly className?: string | undefined;
};

/** Compact figure tile. No trend arrows or claims that the data cannot support. */
export function MetricTile({ label, value, unit, note, tone, badge, className }: MetricTileProps) {
  return (
    <div className={cn("rounded-md border border-border bg-surface px-4 py-3", className)}>
      <div className="flex items-start justify-between gap-2">
        <p className="text-xs font-medium text-balance text-muted-foreground">{label}</p>
        {badge ? <StatusBadge tone={tone}>{badge}</StatusBadge> : null}
      </div>
      <p className="num mt-2 text-2xl leading-none font-semibold text-foreground">
        {value}
        {unit ? (
          <span className="ml-1 text-sm font-medium text-muted-foreground">{unit}</span>
        ) : null}
      </p>
      <p className="mt-2 text-2xs text-muted-foreground">{note}</p>
    </div>
  );
}
