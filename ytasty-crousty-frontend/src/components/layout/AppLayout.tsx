import { Box, Container } from "@mui/material";
import { Outlet } from "react-router-dom";
import { ClosedRestaurantBanner } from "./ClosedRestaurantBanner";
import { Footer } from "./Footer";
import { Header } from "./Header";

export function AppLayout() {
  return (
    <Box sx={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <Header />
      <ClosedRestaurantBanner />
      <Container
        component="main"
        maxWidth="lg"
        sx={{ flexGrow: 1, py: { xs: 3, md: 5 }, px: { xs: 2, md: 3 } }}
      >
        <Outlet />
      </Container>
      <Footer />
    </Box>
  );
}