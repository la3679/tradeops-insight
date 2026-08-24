import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export type PanelProps = {
  readonly title: string;
  readonly description?: string;
  readonly actions?: ReactNode;
  readonly children: ReactNode;
  readonly className?: string;
  /** Renders the panel body without inner padding (useful for tables). */
  readonly flush?: boolean;
};

/** A titled content region. Uses <section> so it is a real landmark child. */
export function Panel({
  title,
  description,
  actions,
  children,
  className,
  flush = false,
}: PanelProps) {
  return (
    <section
      aria-label={title}
      className={cn(
        "flex flex-col rounded-md border border-border bg-surface shadow-none",
        className,
      )}
    >
      <header className="flex flex-wrap items-start justify-between gap-2 border-b border-border px-4 py-3">
        <div className="min-w-0">
          <h2 className="text-sm font-semibold text-foreground">{title}</h2>
          {description ? (
            <p className="mt-0.5 text-xs text-muted-foreground">{description}</p>
          ) : null}
        </div>
        {actions ? <div className="flex items-center gap-2">{actions}</div> : null}
      </header>
      <div className={cn(flush ? "" : "p-4", "flex-1")}>{children}</div>
    </section>
  );
}
