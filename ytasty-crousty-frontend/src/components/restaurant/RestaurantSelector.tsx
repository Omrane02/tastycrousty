import { Chip, MenuItem, Select, Skeleton, Typography, type SelectChangeEvent } from "@mui/material";
import StorefrontIcon from "@mui/icons-material/Storefront";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import {
  fetchRestaurantById,
  selectRestaurant,
  selectRestaurants,
  selectRestaurantStatus,
  selectSelectedRestaurant,
} from "../../features/restaurant/restaurantSlice";

interface RestaurantSelectorProps {
  fullWidth?: boolean;
}

// Sélecteur du restaurant actif (Header).
export function RestaurantSelector({ fullWidth = false }: RestaurantSelectorProps) {
  const dispatch = useAppDispatch();
  const restaurants = useAppSelector(selectRestaurants);
  const status = useAppSelector(selectRestaurantStatus);
  const selected = useAppSelector(selectSelectedRestaurant);

  if (status === "idle" || (status === "loading" && restaurants.length === 0)) {
    return (
      <Skeleton
        variant="rounded"
        width={fullWidth ? "100%" : 220}
        height={40}
        sx={{ borderRadius: "999px" }}
      />
    );
  }

  if (restaurants.length === 0) return null;

  const handleChange = (event: SelectChangeEvent<string>) => {
    const id = Number(event.target.value);
    dispatch(selectRestaurant(id));
    // GET /restaurants/{id} : is_open a pu changer depuis le chargement de la liste.
    void dispatch(fetchRestaurantById(id));
  };

  return (
    <Select<string>
      size="small"
      displayEmpty
      value={selected !== null ? String(selected.id) : ""}
      onChange={handleChange}
      inputProps={{ "aria-label": "Restaurant actif" }}
      startAdornment={<StorefrontIcon sx={{ mr: 1, ml: 0.5, color: "primary.main" }} />}
      renderValue={(value) =>
        value === "" ? (
          <Typography component="span" color="text.secondary">
            Choisir un restaurant
          </Typography>
        ) : (
          (selected?.city ?? "")
        )
      }
      sx={{
        minWidth: fullWidth ? undefined : 220,
        width: fullWidth ? "100%" : undefined,
        borderRadius: "999px",
        bgcolor: "background.paper",
        fontWeight: 600,
      }}
    >
      {restaurants.map((restaurant) => (
        <MenuItem key={restaurant.id} value={String(restaurant.id)} sx={{ gap: 1, fontWeight: 500 }}>
          {restaurant.city}
          {!restaurant.is_open && <Chip size="small" color="error" label="Fermé" />}
        </MenuItem>
      ))}
    </Select>
  );
}