import { useEffect, useState } from "react";
import { Chip } from "@mui/material";
import FiberManualRecordIcon from "@mui/icons-material/FiberManualRecord";
import { getHealth } from "../../api/healthApi";

type ApiStatus = "checking" | "online" | "offline";

const POLL_INTERVAL_MS = 30_000;

const STATUS_CONFIG: Record<ApiStatus, { label: string; color: "default" | "success" | "error" }> = {
  checking: { label: "Vérification de l'API…", color: "default" },
  online: { label: "API en ligne", color: "success" },
  offline: { label: "API injoignable", color: "error" },
};

// Consomme GET /health toutes les 30 secondes.
export function ApiStatusIndicator() {
  const [status, setStatus] = useState<ApiStatus>("checking");

  useEffect(() => {
    let cancelled = false;

    const check = async () => {
      try {
        await getHealth();
        if (!cancelled) setStatus("online");
      } catch {
        if (!cancelled) setStatus("offline");
      }
    };

    void check();
    const intervalId = window.setInterval(() => void check(), POLL_INTERVAL_MS);

    return () => {
      cancelled = true;
      window.clearInterval(intervalId);
    };
  }, []);

  const { label, color } = STATUS_CONFIG[status];

  return (
    <Chip
      size="small"
      variant="outlined"
      color={color}
      icon={<FiberManualRecordIcon sx={{ fontSize: 12 }} />}
      label={label}
      role="status"
    />
  );
}