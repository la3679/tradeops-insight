import {
  Activity,
  BookOpen,
  ClipboardList,
  FlaskConical,
  Info,
  LayoutDashboard,
  ScrollText,
  Settings,
  type LucideIcon,
} from "lucide-react";

export type NavItem = {
  readonly label: string;
  readonly to: string;
  readonly icon: LucideIcon;
  readonly description: string;
};

export const navItems: readonly NavItem[] = [
  {
    label: "Overview",
    to: "/",
    icon: LayoutDashboard,
    description: "Portfolio-level snapshot of synthetic exception activity",
  },
  {
    label: "Exception Queue",
    to: "/exceptions",
    icon: ClipboardList,
    description: "Triage view for individual synthetic trade exceptions",
  },
  {
    label: "Knowledge",
    to: "/knowledge",
    icon: BookOpen,
    description: "Reference notes and investigation playbooks",
  },
  {
    label: "Evaluations",
    to: "/evaluations",
    icon: FlaskConical,
    description: "Test cases used to review assistant behaviour",
  },
  {
    label: "Observability",
    to: "/observability",
    icon: Activity,
    description: "Traces and run history for investigation sessions",
  },
  {
    label: "Audit",
    to: "/audit",
    icon: ScrollText,
    description: "Immutable record of console actions",
  },
  {
    label: "Settings",
    to: "/settings",
    icon: Settings,
    description: "Workspace preferences and display options",
  },
  {
    label: "About",
    to: "/about",
    icon: Info,
    description: "Scope, disclaimer, and project background",
  },
] as const;
