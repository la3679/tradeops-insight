import { createContext, useContext, useMemo, useState, type ReactNode } from "react";
import type { DemoRole } from "./tradeops-api";

type DemoRoleContextValue = {
  readonly role: DemoRole;
  readonly setRole: (role: DemoRole) => void;
};

const DemoRoleContext = createContext<DemoRoleContextValue | null>(null);

export function DemoRoleProvider({ children }: { readonly children: ReactNode }) {
  const [role, setRole] = useState<DemoRole>("analyst");
  const value = useMemo(() => ({ role, setRole }), [role]);
  return <DemoRoleContext.Provider value={value}>{children}</DemoRoleContext.Provider>;
}

// Hook export intentionally shares the provider module to keep the context identity singular.
// eslint-disable-next-line react-refresh/only-export-components
export function useDemoRole(): DemoRoleContextValue {
  const value = useContext(DemoRoleContext);
  if (!value) throw new Error("useDemoRole must be rendered inside DemoRoleProvider");
  return value;
}
