import { Alert } from "@mui/material";
import BlockIcon from "@mui/icons-material/Block";
import { useAppSelector } from "../../app/hooks";
import { selectSelectedRestaurant } from "../../features/restaurant/restaurantSlice";


export function ClosedRestaurantBanner() {
  const restaurant = useAppSelector(selectSelectedRestaurant);

  if (restaurant === null || restaurant.is_open) return null;

  return (
    <Alert
      severity="warning"
      icon={<BlockIcon />}
      sx={{ borderRadius: 0, justifyContent: "center", alignItems: "center" }}
    >
      <strong>{restaurant.name}</strong> est actuellement fermé : la prise de commande est
      désactivée.
      {restaurant.opening_hours ? ` Horaires : ${restaurant.opening_hours}.` : ""}
    </Alert>
  );
}