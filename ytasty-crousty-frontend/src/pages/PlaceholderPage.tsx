import { Box, Button, Typography } from "@mui/material";
import ConstructionIcon from "@mui/icons-material/Construction";
import { Link as RouterLink } from "react-router-dom";

interface PlaceholderPageProps {
  title: string;
  description: string;
}

// Page temporaire pour les routes des prochains modules (carte, panier, connexion...).
export function PlaceholderPage({ title, description }: PlaceholderPageProps) {
  return (
    <Box sx={{ textAlign: "center", py: { xs: 6, md: 10 } }}>
      <ConstructionIcon sx={{ fontSize: 64, color: "secondary.main" }} />
      <Typography variant="h4" component="h1" sx={{ mt: 2 }}>
        {title}
      </Typography>
      <Typography color="text.secondary" sx={{ mt: 1, mb: 4 }}>
        {description}
      </Typography>
      <Button component={RouterLink} to="/" variant="contained">
        Retour à l'accueil
      </Button>
    </Box>
  );
}