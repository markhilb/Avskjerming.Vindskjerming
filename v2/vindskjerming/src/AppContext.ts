import {
  createContext,
  useContext,
  type Dispatch,
  type SetStateAction,
} from "react";
import type { AppState } from "./AppState";

export interface AppStateCtx {
  state: AppState;
  onChange: Dispatch<SetStateAction<AppState>>;
}

export const AppStateContext = createContext<AppStateCtx | undefined>(
  undefined,
);

export function useAppState(): AppStateCtx {
  const ctx = useContext(AppStateContext);
  if (!ctx) {
    throw new Error(
      "useAppState must be used within an AppStateContext Provider",
    );
  }
  return ctx;
}
