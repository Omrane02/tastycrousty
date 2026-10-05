import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";
import { BrowserRouter } from "react-router-dom";
import { CssBaseline, ThemeProvider } from "@mui/material";
import App from "./App";
import { setupInterceptors } from "./api/setupInterceptors";
import { store } from "./app/store";
import { NotificationProvider } from "./components/common/NotificationProvider";
import theme from "./theme/theme";

setupInterceptors(store.dispatch);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <NotificationProvider>
          <BrowserRouter>
            <App />
          </BrowserRouter>
        </NotificationProvider>
      </ThemeProvider>
    </Provider>
  </StrictMode>,
);