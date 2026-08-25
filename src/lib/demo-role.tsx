import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { demoRoles, type DemoRole } from "./tradeops-api";

type DemoRoleContextValue = {
  readonly role: DemoRole;
  readonly setRole: (role: DemoRole) => void;
};

const DemoRoleContext = createContext<DemoRoleContextValue | null>(null);
const storageKey = "tradeops-demo-role";

export function DemoRoleProvider({ children }: { readonly children: ReactNode }) {
  const [role, updateRole] = useState<DemoRole>("analyst");
  useEffect(() => {
    const stored = localStorage.getItem(storageKey);
    if (demoRoles.some((candidate) => candidate === stored)) updateRole(stored as DemoRole);
  }, []);
  const setRole = useCallback((nextRole: DemoRole) => {
    localStorage.setItem(storageKey, nextRole);
    updateRole(nextRole);
  }, []);
  const value = useMemo(() => ({ role, setRole }), [role, setRole]);
  return <DemoRoleContext.Provider value={value}>{children}</DemoRoleContext.Provider>;
}

// Hook export intentionally shares the provider module to keep the context identity singular.
// eslint-disable-next-line react-refresh/only-export-components
export function useDemoRole(): DemoRoleContextValue {
  const value = useContext(DemoRoleContext);
  if (!value) throw new Error("useDemoRole must be rendered inside DemoRoleProvider");
  return value;
}
