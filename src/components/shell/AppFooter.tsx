import { Link } from "@tanstack/react-router";

export function AppFooter() {
  return (
    <footer className="border-t border-border bg-surface px-6 py-4">
      <p className="text-2xs leading-relaxed text-muted-foreground">
        TradeOps Copilot — independent educational portfolio project. Not affiliated
        with any financial institution, not investment advice, and no trades are
        executed. All figures are synthetic.{" "}
        <Link to="/about" className="font-medium text-foreground underline underline-offset-2">
          Full disclaimer
        </Link>
        .
      </p>
    </footer>
  );
}
