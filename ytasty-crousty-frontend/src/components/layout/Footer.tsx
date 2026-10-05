import { Box, Container, Typography } from "@mui/material";
import { ApiStatusIndicator } from "../common/ApiStatusIndicator";

export function Footer() {
  return (
    <Box component="footer" sx={{ mt: 8, py: 3, borderTop: "1px solid", borderColor: "divider" }}>
      <Container
        maxWidth="lg"
        sx={{
          px: { xs: 2, md: 3 },
          display: "flex",
          flexWrap: "wrap",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 2,
        }}
      >
        <Typography variant="body2" color="text.secondary">
          © {new Date().getFullYear()} Ytasty Crousty · Aix · Lyon · Paris
        </Typography>
        <ApiStatusIndicator />
      </Container>
    </Box>
  );
}