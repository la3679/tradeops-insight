import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center gap-1 rounded-sm border px-1.5 py-0.5 text-2xs font-medium uppercase tracking-wide whitespace-nowrap",
  {
    variants: {
      tone: {
        neutral: "border-border bg-muted text-muted-foreground",
        info: "border-info/30 bg-info-subtle text-info",
        verified: "border-verified/30 bg-verified-subtle text-verified",
        pending: "border-pending/40 bg-pending-subtle text-pending-foreground",
        severe: "border-severe/35 bg-severe-subtle text-severe",
      },
    },
    defaultVariants: { tone: "neutral" },
  },
);

export type StatusBadgeProps = React.HTMLAttributes<HTMLSpanElement> &
  VariantProps<typeof badgeVariants>;

export function StatusBadge({ tone, className, ...props }: StatusBadgeProps) {
  return <span className={cn(badgeVariants({ tone }), className)} {...props} />;
}
