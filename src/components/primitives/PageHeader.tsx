import type { ReactNode } from "react";

export type PageHeaderProps = {
  readonly title: string;
  readonly summary: string;
  readonly actions?: ReactNode;
  readonly meta?: ReactNode;
};

export function PageHeader({ title, summary, actions, meta }: PageHeaderProps) {
  return (
    <header className="flex flex-wrap items-end justify-between gap-4 border-b border-border pb-4">
      <div className="min-w-0 max-w-2xl">
        <h1 className="text-lg font-semibold text-foreground">{title}</h1>
        <p className="mt-1 text-xs text-muted-foreground">{summary}</p>
        {meta ? <div className="mt-2">{meta}</div> : null}
      </div>
      {actions ? <div className="flex items-center gap-2">{actions}</div> : null}
    </header>
  );
}
