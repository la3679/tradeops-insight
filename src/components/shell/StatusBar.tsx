import { Menu, X } from "lucide-react";
import { StatusBadge } from "@/components/primitives/StatusBadge";
import { dataAsOf } from "@/data/overview";
import { useDemoRole } from "@/lib/demo-role";
import { demoRoles, type DemoRole } from "@/lib/tradeops-api";

export type StatusBarProps = {
  readonly navOpen: boolean;
  readonly onToggleNav: () => void;
};

export function StatusBar({ navOpen, onToggleNav }: StatusBarProps) {
  const { role, setRole } = useDemoRole();
  return (
    <div className="flex h-14 items-center gap-3 border-b border-border bg-surface px-4">
      <button
        type="button"
        onClick={onToggleNav}
        aria-expanded={navOpen}
        aria-controls="app-side-nav"
        className="inline-flex size-11 items-center justify-center rounded-sm text-muted-foreground hover:bg-accent hover:text-accent-foreground lg:hidden"
      >
        {navOpen ? (
          <X className="size-4" aria-hidden="true" />
        ) : (
          <Menu className="size-4" aria-hidden="true" />
        )}
        <span className="sr-only">{navOpen ? "Close navigation" : "Open navigation"}</span>
      </button>

      <div className="flex min-w-0 flex-1 flex-wrap items-center gap-x-4 gap-y-1">
        <StatusBadge tone="info">Synthetic data</StatusBadge>
        <StatusBadge tone="neutral">Local demo</StatusBadge>
        <p className="num hidden truncate text-2xs text-muted-foreground sm:block">
          Fixture as of {dataAsOf}
        </p>
      </div>

      <dl className="hidden items-center gap-4 md:flex">
        <div className="flex items-center gap-1.5">
          <dt className="text-2xs text-muted-foreground">Environment</dt>
          <dd className="text-2xs font-medium text-foreground">Demo</dd>
        </div>
        <div className="flex items-center gap-1.5">
          <dt>
            <label htmlFor="demo-role" className="text-2xs text-muted-foreground">
              Demo role
            </label>
          </dt>
          <dd>
            <select
              id="demo-role"
              value={role}
              onChange={(event) => setRole(event.target.value as DemoRole)}
              className="h-9 cursor-pointer rounded-sm border border-input bg-background px-2 text-xs font-medium text-foreground"
            >
              {demoRoles.map((candidate) => (
                <option key={candidate} value={candidate}>
                  {candidate.replace("_", " ")}
                </option>
              ))}
            </select>
          </dd>
        </div>
      </dl>
    </div>
  );
}
