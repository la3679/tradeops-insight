import { Loader2, Inbox, ShieldAlert } from "lucide-react";
import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

type FrameProps = {
  readonly children: ReactNode;
  readonly className?: string | undefined;
};

function StateFrame({ children, className }: FrameProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center gap-2 rounded-md border border-dashed border-border bg-surface px-6 py-10 text-center",
        className,
      )}
    >
      {children}
    </div>
  );
}

/** Indeterminate loading state for a panel or region. */
export function LoadingState({
  label = "Loading",
  className,
}: {
  readonly label?: string | undefined;
  readonly className?: string | undefined;
}) {
  return (
    <StateFrame className={className}>
      <Loader2 className="size-4 animate-spin text-muted-foreground" aria-hidden="true" />
      <p role="status" aria-live="polite" className="text-xs text-muted-foreground">
        {label}…
      </p>
    </StateFrame>
  );
}

/** Skeleton rows for tabular loading. */
export function SkeletonRows({ rows = 4 }: { readonly rows?: number }) {
  return (
    <div className="space-y-2" aria-hidden="true">
      {Array.from({ length: rows }, (_, index) => (
        <div key={index} className="h-8 animate-pulse rounded-sm bg-muted" />
      ))}
    </div>
  );
}

/** Nothing to show, without implying an error. */
export function EmptyState({
  title,
  description,
  action,
  className,
}: {
  readonly title: string;
  readonly description?: string | undefined;
  readonly action?: ReactNode | undefined;
  readonly className?: string | undefined;
}) {
  return (
    <StateFrame className={className}>
      <Inbox className="size-5 text-muted-foreground" aria-hidden="true" />
      <p className="text-sm font-medium text-foreground">{title}</p>
      {description ? (
        <p className="max-w-sm text-xs text-muted-foreground">{description}</p>
      ) : null}
      {action}
    </StateFrame>
  );
}

/**
 * Presentation-only permission notice. Authorization itself is enforced
 * outside this frontend.
 */
export function PermissionDeniedState({
  resource,
  className,
}: {
  readonly resource: string;
  readonly className?: string | undefined;
}) {
  return (
    <StateFrame className={cn("border-severe/30 bg-severe-subtle/40", className)}>
      <ShieldAlert className="size-5 text-severe" aria-hidden="true" />
      <p className="text-sm font-medium text-foreground">Access not available</p>
      <p className="max-w-sm text-xs text-muted-foreground">
        Your workspace role does not include access to {resource}. Entitlements are
        managed outside this console.
      </p>
    </StateFrame>
  );
}
