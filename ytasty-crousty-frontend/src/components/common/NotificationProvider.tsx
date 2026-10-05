import { useCallback, useState, type ReactNode } from "react";
import { Alert, Snackbar, type AlertColor } from "@mui/material";
import { NotificationContext, type Notify } from "./NotificationContext";

interface Notification {
  id: number;
  message: string;
  severity: AlertColor;
}

export function NotificationProvider({ children }: { children: ReactNode }) {
  const [current, setCurrent] = useState<Notification | null>(null);
  const [open, setOpen] = useState(false);

  const notify = useCallback<Notify>((message, severity = "info") => {
    setCurrent({ id: Date.now(), message, severity });
    setOpen(true);
  }, []);

  const handleClose = (_event: unknown, reason?: string) => {
    if (reason === "clickaway") return;
    setOpen(false);
  };

  return (
    <NotificationContext.Provider value={notify}>
      {children}
      <Snackbar
        key={current?.id}
        open={open}
        autoHideDuration={4500}
        onClose={handleClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          onClose={() => setOpen(false)}
          severity={current?.severity ?? "info"}
          variant="filled"
          sx={{ width: "100%" }}
        >
          {current?.message}
        </Alert>
      </Snackbar>
    </NotificationContext.Provider>
  );
}