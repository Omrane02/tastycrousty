import {
  AppBar,
  Avatar,
  Badge,
  Box,
  Button,
  Chip,
  Container,
  IconButton,
  Toolbar,
  Tooltip,
  Typography,
} from "@mui/material";
import ShoppingCartOutlinedIcon from "@mui/icons-material/ShoppingCartOutlined";
import LoginIcon from "@mui/icons-material/Login";
import LogoutIcon from "@mui/icons-material/Logout";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { logout, selectCurrentUser } from "../../features/auth/authSlice";
import { selectCartItemsCount } from "../../features/cart/cartSlice";
import { useNotify } from "../common/NotificationContext";
import { RestaurantSelector } from "../restaurant/RestaurantSelector";
import { Logo } from "./Logo";
import type { Role } from "../../types/auth";

const ROLE_BADGES: Record<Role, { label: string; color: "primary" | "secondary" | "info" }> = {
  admin: { label: "Admin", color: "primary" },
  staff: { label: "Staff", color: "secondary" },
  direction: { label: "Direction", color: "info" },
};

export function Header() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const notify = useNotify();
  const user = useAppSelector(selectCurrentUser);
  const cartCount = useAppSelector(selectCartItemsCount);

  const handleLogout = () => {
    dispatch(logout());
    notify("Vous avez été déconnecté.", "success");
    navigate("/");
  };

  return (
    <AppBar position="sticky">
      <Container maxWidth="lg" disableGutters sx={{ px: { xs: 2, md: 3 } }}>
        <Toolbar disableGutters sx={{ minHeight: 64, gap: 1.5 }}>
          <Logo />


          <Box sx={{ display: { xs: "none", sm: "block" }, ml: { sm: 2 } }}>
            <RestaurantSelector />
          </Box>

          <Box sx={{ flexGrow: 1 }} />

          <Tooltip title="Mon panier">
            <IconButton
              component={RouterLink}
              to="/cart"
              color="inherit"
              aria-label={`Panier : ${cartCount} article${cartCount > 1 ? "s" : ""}`}
            >
              <Badge badgeContent={cartCount} color="secondary" max={99}>
                <ShoppingCartOutlinedIcon />
              </Badge>
            </IconButton>
          </Tooltip>

          {user === null ? (
            <Button component={RouterLink} to="/login" variant="contained" startIcon={<LoginIcon />}>
              Connexion
            </Button>
          ) : (
            <Box sx={{ display: "flex", alignItems: "center", gap: 1.25 }}>
              <Avatar sx={{ width: 36, height: 36, bgcolor: "primary.main", fontWeight: 700 }}>
                {user.username.charAt(0).toUpperCase()}
              </Avatar>
              <Typography
                variant="body2"
                sx={{ fontWeight: 700, display: { xs: "none", md: "block" } }}
              >
                {user.username}
              </Typography>
              <Chip
                size="small"
                label={ROLE_BADGES[user.role].label}
                color={ROLE_BADGES[user.role].color}
              />
              <Button
                variant="outlined"
                color="inherit"
                startIcon={<LogoutIcon />}
                onClick={handleLogout}
                sx={{ display: { xs: "none", sm: "inline-flex" } }}
              >
                Déconnexion
              </Button>
              <Tooltip title="Déconnexion">
                <IconButton
                  color="inherit"
                  onClick={handleLogout}
                  aria-label="Se déconnecter"
                  sx={{ display: { xs: "inline-flex", sm: "none" } }}
                >
                  <LogoutIcon />
                </IconButton>
              </Tooltip>
            </Box>
          )}
        </Toolbar>


        <Box sx={{ display: { xs: "block", sm: "none" }, pb: 1.5 }}>
          <RestaurantSelector fullWidth />
        </Box>
      </Container>
    </AppBar>
  );
}