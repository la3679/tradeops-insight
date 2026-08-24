import { useState, type ReactNode } from "react";
import { AppFooter } from "./AppFooter";
import { SideNav } from "./SideNav";
import { StatusBar } from "./StatusBar";

export function AppShell({ children }: { readonly children: ReactNode }) {
  const [navOpen, setNavOpen] = useState(false);

  return (
    <div className="flex min-h-screen w-full bg-background">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:rounded-sm focus:bg-primary focus:px-3 focus:py-2 focus:text-xs focus:font-medium focus:text-primary-foreground"
      >
        Skip to main content
      </a>

      {/* Persistent nav from lg up; overlay drawer below. */}
      <div
        id="app-side-nav"
        className={
          navOpen
            ? "fixed inset-y-0 left-0 z-40 w-64 shrink-0 lg:sticky lg:top-0 lg:h-screen"
            : "hidden w-64 shrink-0 lg:sticky lg:top-0 lg:block lg:h-screen"
        }
      >
        <SideNav onNavigate={() => setNavOpen(false)} />
      </div>

      {navOpen ? (
        <button
          type="button"
          aria-label="Close navigation"
          onClick={() => setNavOpen(false)}
          className="fixed inset-0 z-30 bg-foreground/30 lg:hidden"
        />
      ) : null}

      <div className="flex min-w-0 flex-1 flex-col">
        <StatusBar navOpen={navOpen} onToggleNav={() => setNavOpen((open) => !open)} />
        <main id="main-content" className="flex-1 px-4 py-6 sm:px-6">
          {children}
        </main>
        <AppFooter />
      </div>
    </div>
  );
}
