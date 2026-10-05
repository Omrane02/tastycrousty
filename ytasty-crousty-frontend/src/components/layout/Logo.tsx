import { Box, Typography } from "@mui/material";
import LunchDiningIcon from "@mui/icons-material/LunchDining";
import { Link as RouterLink } from "react-router-dom";

export function Logo() {
  return (
    <Box
      component={RouterLink}
      to="/"
      aria-label="Ytasty Crousty - Accueil"
      sx={{
        display: "inline-flex",
        alignItems: "center",
        gap: 1.25,
        textDecoration: "none",
        color: "inherit",
      }}
    >
      <Box
        sx={{
          width: 40,
          height: 40,
          borderRadius: "12px",
          display: "grid",
          placeItems: "center",
          color: "#fff",
          background: (theme) =>
            `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
          boxShadow: "0 6px 14px rgba(215, 48, 31, 0.35)",
        }}
      >
        <LunchDiningIcon />
      </Box>
      <Typography
        component="span"
        variant="h6"
        sx={{ fontWeight: 800, lineHeight: 1, display: { xs: "none", sm: "block" } }}
      >
        <Box component="span" sx={{ color: "primary.main" }}>
          Ytasty
        </Box>{" "}
        Crousty
      </Typography>
    </Box>
  );
}