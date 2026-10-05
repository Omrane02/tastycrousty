import { useEffect } from "react";
import { SESSION_EXPIRED_EVENT } from "./api/setupInterceptors";
import { useAppDispatch, useAppSelector } from "./app/hooks";
import { useNotify } from "./components/common/NotificationContext";
import { fetchRestaurants, selectRestaurantStatus } from "./features/restaurant/restaurantSlice";
import { AppRoutes } from "./routes/AppRoutes";

export default function App() {
  const dispatch = useAppDispatch();
  const notify = useNotify();
  const status = useAppSelector(selectRestaurantStatus);

  // Charge la liste des restaurants une seule fois au démarrage (GET /restaurants).
  useEffect(() => {
    if (status === "idle") {
      void dispatch(fetchRestaurants());
    }
  }, [dispatch, status]);

  // L'intercepteur axios émet cet événement quand un 401 force la déconnexion.
  useEffect(() => {
    const handleSessionExpired = () => {
      notify("Votre session a expiré, veuillez vous reconnecter.", "warning");
    };
    window.addEventListener(SESSION_EXPIRED_EVENT, handleSessionExpired);
    return () => window.removeEventListener(SESSION_EXPIRED_EVENT, handleSessionExpired);
  }, [notify]);

  return <AppRoutes />;
}