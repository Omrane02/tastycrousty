import { Route, Routes } from "react-router-dom";
import { AppLayout } from "../components/layout/AppLayout";
import { HomePage } from "../pages/HomePage";
import { PlaceholderPage } from "../pages/PlaceholderPage";

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<HomePage />} />
        <Route
          path="menu"
          element={<PlaceholderPage title="La carte" description="La carte du restaurant arrive au prochain module." />}
        />
        <Route
          path="cart"
          element={<PlaceholderPage title="Mon panier" description="Le panier arrive au prochain module." />}
        />
        <Route
          path="login"
          element={<PlaceholderPage title="Connexion" description="La page de connexion arrive au prochain module." />}
        />
        <Route
          path="*"
          element={<PlaceholderPage title="Page introuvable" description="Cette page n'existe pas." />}
        />
      </Route>
    </Routes>
  );
}