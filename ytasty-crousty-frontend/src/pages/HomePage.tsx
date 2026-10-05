import { Alert, Box, Button, Chip, Typography } from "@mui/material";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";
import { useNavigate } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "../app/hooks";
import { RestaurantCard } from "../components/restaurant/RestaurantCard";
import { RestaurantCardSkeleton } from "../components/restaurant/RestaurantCardSkeleton";
import { useNotify } from "../components/common/NotificationContext";
import { selectCurrentUser } from "../features/auth/authSlice";
import {
  fetchRestaurants,
  selectRestaurant,
  selectRestaurantError,
  selectRestaurants,
  selectRestaurantStatus,
  selectSelectedRestaurant,
  toggleRestaurantAvailability,
} from "../features/restaurant/restaurantSlice";
import type { Restaurant } from "../types/restaurant";
import { getErrorMessage } from "../utils/errors";

export function HomePage() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const notify = useNotify();

  const restaurants = useAppSelector(selectRestaurants);
  const status = useAppSelector(selectRestaurantStatus);
  const error = useAppSelector(selectRestaurantError);
  const selected = useAppSelector(selectSelectedRestaurant);
  const user = useAppSelector(selectCurrentUser);

  const isAdmin = user?.role === "admin";
  const isLoading = status === "idle" || (status === "loading" && restaurants.length === 0);
  const hasFailed = status === "failed" && restaurants.length === 0;

  const handleSelect = (restaurant: Restaurant) => {
    dispatch(selectRestaurant(restaurant.id));
    navigate("/menu");
  };

  const handleToggleAvailability = async (restaurant: Restaurant, isOpen: boolean) => {
    try {
      await dispatch(toggleRestaurantAvailability({ id: restaurant.id, isOpen })).unwrap();
      notify(`${restaurant.name} est maintenant ${isOpen ? "ouvert" : "fermé"}.`, "success");
    } catch (err) {
      notify(getErrorMessage(err), "error");
    }
  };

  return (
    <>
      <Box
        component="section"
        sx={{
          position: "relative",
          overflow: "hidden",
          borderRadius: "28px",
          px: { xs: 3, md: 7 },
          py: { xs: 5, md: 8 },
          color: "#fff",
          background: "linear-gradient(135deg, #D7301F 0%, #F26B1D 55%, #F5A300 100%)",
          "&::after": {
            content: '""',
            position: "absolute",
            right: -80,
            top: -80,
            width: 320,
            height: 320,
            borderRadius: "50%",
            background: "rgba(255, 255, 255, 0.12)",
            pointerEvents: "none",
          },
        }}
      >
        <Chip
          label="Aix · Lyon · Paris"
          sx={{ bgcolor: "rgba(255, 255, 255, 0.2)", color: "#fff", mb: 2 }}
        />
        <Typography variant="h2" component="h1" sx={{ maxWidth: 640 }}>
          Croustillant, gourmand,{" "}
          <Box component="span" sx={{ color: "#FFE8A8" }}>
            Ytasty.
          </Box>
        </Typography>
        <Typography variant="h6" component="p" sx={{ mt: 2, maxWidth: 560, fontWeight: 400 }}>
          Choisissez votre restaurant, composez votre commande et suivez sa préparation en direct.
          Aucun compte nécessaire.
        </Typography>
        <Button
          component="a"
          href="#restaurants"
          variant="contained"
          color="secondary"
          size="large"
          endIcon={<ArrowDownwardIcon />}
          sx={{ mt: 4 }}
        >
          Choisir mon restaurant
        </Button>
      </Box>

      <Box component="section" id="restaurants" sx={{ mt: { xs: 5, md: 8 }, scrollMarginTop: "96px" }}>
        <Typography variant="h4" component="h2">
          Choisissez votre restaurant
        </Typography>
        <Typography color="text.secondary" sx={{ mt: 1, mb: 4 }}>
          Trois adresses, une même envie de croustillant.
        </Typography>

        {hasFailed ? (
          <Alert
            severity="error"
            action={
              <Button color="inherit" size="small" onClick={() => void dispatch(fetchRestaurants())}>
                Réessayer
              </Button>
            }
          >
            {error ?? "Impossible de charger les restaurants."}
          </Alert>
        ) : (
          <Box
            sx={{
              display: "grid",
              gap: 3,
              gridTemplateColumns: { xs: "1fr", sm: "repeat(2, 1fr)", lg: "repeat(3, 1fr)" },
            }}
          >
            {isLoading
              ? [0, 1, 2].map((index) => <RestaurantCardSkeleton key={index} />)
              : restaurants.map((restaurant) => (
                  <RestaurantCard
                    key={restaurant.id}
                    restaurant={restaurant}
                    isSelected={selected?.id === restaurant.id}
                    isAdmin={isAdmin}
                    onSelect={handleSelect}
                    onToggleAvailability={handleToggleAvailability}
                  />
                ))}
          </Box>
        )}
      </Box>
    </>
  );
}