import { createContext, useContext } from "react";
import type { AlertColor } from "@mui/material";

export type Notify = (message: string, severity?: AlertColor) => void;

export const NotificationContext = createContext<Notify | null>(null);


export function useNotify(): Notify {
  const notify = useContext(NotificationContext);
  if (notify === null) {
    throw new Error("useNotify doit être utilisé à l'intérieur d'un <NotificationProvider>.");
  }
  return notify;
}