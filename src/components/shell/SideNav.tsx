import { Link } from "@tanstack/react-router";
import { navItems } from "@/lib/nav";
import { cn } from "@/lib/utils";

export type SideNavProps = {
  readonly onNavigate?: (() => void) | undefined;
};

export function SideNav({ onNavigate }: SideNavProps) {
  return (
    <nav aria-label="Primary" className="flex h-full flex-col bg-nav text-nav-foreground">
      <div className="flex items-center gap-2 px-4 py-4">
        <span
          aria-hidden="true"
          className="flex size-7 items-center justify-center rounded-sm bg-nav-active text-2xs font-semibold tracking-widest text-nav-foreground"
        >
          TO
        </span>
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold">TradeOps Copilot</p>
          <p className="text-2xs text-nav-muted">Synthetic operations console</p>
        </div>
      </div>

      <ul className="flex-1 space-y-0.5 overflow-y-auto px-2 py-2">
        {navItems.map((item) => (
          <li key={item.to}>
            <Link
              to={item.to}
              onClick={onNavigate}
              activeOptions={{ exact: item.to === "/" }}
              className={cn(
                "group flex items-center gap-2 rounded-sm px-2 py-2 text-xs font-medium text-nav-muted transition-colors",
                "hover:bg-nav-active hover:text-nav-foreground",
              )}
              activeProps={{
                className: "bg-nav-active text-nav-foreground",
                "aria-current": "page",
              }}
            >
              <item.icon className="size-4 shrink-0" aria-hidden="true" />
              <span className="truncate">{item.label}</span>
            </Link>
          </li>
        ))}
      </ul>

      <div className="border-t border-white/10 px-4 py-3">
        <p className="text-2xs leading-relaxed text-nav-muted">
          Educational portfolio project. Synthetic data only — no trade execution.
        </p>
      </div>
    </nav>
  );
}
