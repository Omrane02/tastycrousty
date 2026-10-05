import { useState, type ChangeEvent, type ReactNode } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  Chip,
  CircularProgress,
  FormControlLabel,
  Stack,
  Switch,
  Typography,
} from "@mui/material";
import StorefrontIcon from "@mui/icons-material/Storefront";
import PlaceOutlinedIcon from "@mui/icons-material/PlaceOutlined";
import PhoneOutlinedIcon from "@mui/icons-material/PhoneOutlined";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import FiberManualRecordIcon from "@mui/icons-material/FiberManualRecord";
import RestaurantMenuIcon from "@mui/icons-material/RestaurantMenu";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import type { Restaurant } from "../../types/restaurant";

const BANNER_GRADIENTS = [
  "linear-gradient(135deg, #D7301F 0%, #F26B1D 100%)",
  "linear-gradient(135deg, #F26B1D 0%, #F5A300 100%)",
  "linear-gradient(135deg, #8E1B10 0%, #D7301F 100%)",
];

interface RestaurantCardProps {
  restaurant: Restaurant;
  isSelected: boolean;
  isAdmin: boolean;
  onSelect: (restaurant: Restaurant) => void;
  // Ne doit jamais rejeter : le parent gère les erreurs (Snackbar).
  onToggleAvailability: (restaurant: Restaurant, isOpen: boolean) => Promise<void>;
}

interface InfoRowProps {
  icon: ReactNode;
  label: string;
  value: string | null;
}

function InfoRow({ icon, label, value }: InfoRowProps) {
  return (
    <Box sx={{ display: "flex", gap: 1.25, alignItems: "flex-start" }}>
      <Box aria-hidden sx={{ color: "primary.main", display: "flex", mt: "2px" }}>
        {icon}
      </Box>
      <Box>
        <Typography
          variant="caption"
          sx={{
            display: "block",
            textTransform: "uppercase",
            letterSpacing: 0.6,
            fontWeight: 700,
            color: "text.secondary",
          }}
        >
          {label}
        </Typography>
        <Typography
          variant="body2"
          color={value ? "text.primary" : "text.disabled"}
          sx={{ fontStyle: value ? "normal" : "italic" }}
        >
          {value ?? "Non renseigné"}
        </Typography>
      </Box>
    </Box>
  );
}

export function RestaurantCard({
  restaurant,
  isSelected,
  isAdmin,
  onSelect,
  onToggleAvailability,
}: RestaurantCardProps) {
  const [updating, setUpdating] = useState(false);

  const handleToggle = async (event: ChangeEvent<HTMLInputElement>) => {
    const nextValue = event.target.checked;
    setUpdating(true);
    try {
      await onToggleAvailability(restaurant, nextValue);
    } finally {
      setUpdating(false);
    }
  };

  const ctaLabel = restaurant.is_open
    ? isSelected
      ? "Voir la carte"
      : "Commander ici"
    : "Consulter la carte";

  return (
    <Card
      sx={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        outline: "2px solid",
        outlineColor: isSelected ? "primary.main" : "transparent",
        transition: "transform 0.2s ease, box-shadow 0.2s ease",
        "&:hover": {
          transform: "translateY(-4px)",
          boxShadow: "0 14px 36px rgba(43, 23, 8, 0.14)",
        },
      }}
    >
      <Box
        sx={{
          position: "relative",
          height: 112,
          display: "grid",
          placeItems: "center",
          color: "#fff",
          background: BANNER_GRADIENTS[restaurant.id % BANNER_GRADIENTS.length],
          filter: restaurant.is_open ? "none" : "grayscale(0.55)",
        }}
      >
        <StorefrontIcon sx={{ fontSize: 56 }} />
        <Chip
          size="small"
          color={restaurant.is_open ? "success" : "error"}
          icon={<FiberManualRecordIcon sx={{ fontSize: 12 }} />}
          label={restaurant.is_open ? "Ouvert" : "Fermé"}
          sx={{ position: "absolute", top: 12, right: 12 }}
        />
      </Box>

      <CardContent sx={{ flexGrow: 1, display: "flex", flexDirection: "column", gap: 2 }}>
        <Box>
          <Box sx={{ display: "flex", alignItems: "center", gap: 1, flexWrap: "wrap" }}>
            <Typography variant="h5" component="h3">
              {restaurant.name}
            </Typography>
            {isSelected && <Chip size="small" color="primary" variant="outlined" label="Sélectionné" />}
          </Box>
          <Typography variant="body2" color="text.secondary">
            {restaurant.city}
          </Typography>
        </Box>

        <Stack spacing={1.5}>
          <InfoRow icon={<PlaceOutlinedIcon fontSize="small" />} label="Adresse" value={restaurant.address} />
          <InfoRow icon={<PhoneOutlinedIcon fontSize="small" />} label="Contact" value={restaurant.contact} />
          <InfoRow
            icon={<AccessTimeIcon fontSize="small" />}
            label="Horaires"
            value={restaurant.opening_hours}
          />
        </Stack>

        {!restaurant.is_open && (
          <Alert severity="warning" variant="outlined">
            Restaurant fermé : la prise de commande est désactivée.
          </Alert>
        )}

        {isAdmin && (
          <Box
            sx={{
              mt: "auto",
              px: 1.5,
              py: 0.5,
              border: "1px dashed",
              borderColor: "divider",
              borderRadius: "14px",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
            }}
          >
            <FormControlLabel
              control={
                <Switch
                  checked={restaurant.is_open}
                  onChange={(event) => void handleToggle(event)}
                  disabled={updating}
                  color="success"
                />
              }
              label={`Admin · ${restaurant.is_open ? "Ouvert" : "Fermé"}`}
            />
            {updating && <CircularProgress size={18} />}
          </Box>
        )}
      </CardContent>

      <CardActions sx={{ p: 2, pt: 0 }}>
        <Button
          fullWidth
          size="large"
          variant={restaurant.is_open ? "contained" : "outlined"}
          startIcon={isSelected ? <CheckCircleIcon /> : <RestaurantMenuIcon />}
          onClick={() => onSelect(restaurant)}
        >
          {ctaLabel}
        </Button>
      </CardActions>
    </Card>
  );
}