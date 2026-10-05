import { createTheme, responsiveFontSizes } from "@mui/material/styles";

const headingFont = "'Poppins', 'Inter', system-ui, sans-serif";
const bodyFont = "'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif";

const baseTheme = createTheme({
  palette: {
    mode: "light",
    // Rouge tomate
    primary: { main: "#D7301F", light: "#F0604D", dark: "#A31F12", contrastText: "#FFFFFF" },
    // Jaune
    secondary: { main: "#F5A300", light: "#FFC247", dark: "#C27F00", contrastText: "#2B1708" },
    success: { main: "#2E7D32" },
    error: { main: "#B3261E" },
    info: { main: "#1E6FA8" },
    background: { default: "#FFF7EC", paper: "#FFFFFF" }, // crème
    text: { primary: "#2B1708", secondary: "#6B5444" }, // brun chocolat
  },
  shape: { borderRadius: 14 },
  typography: {
    fontFamily: bodyFont,
    h1: { fontFamily: headingFont, fontWeight: 800, letterSpacing: "-0.02em" },
    h2: { fontFamily: headingFont, fontWeight: 800, letterSpacing: "-0.02em" },
    h3: { fontFamily: headingFont, fontWeight: 700 },
    h4: { fontFamily: headingFont, fontWeight: 700 },
    h5: { fontFamily: headingFont, fontWeight: 700 },
    h6: { fontFamily: headingFont, fontWeight: 600 },
    button: { textTransform: "none", fontWeight: 600, letterSpacing: 0 },
  },
  components: {
    MuiButton: {
      defaultProps: { disableElevation: true },
      styleOverrides: {
        root: { borderRadius: 999, paddingInline: 22 },
        sizeLarge: { paddingBlock: 12, fontSize: "1rem" },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 20,
          border: "1px solid rgba(43, 23, 8, 0.06)",
          boxShadow: "0 8px 30px rgba(43, 23, 8, 0.08)",
        },
      },
    },
    MuiChip: {
      styleOverrides: { root: { fontWeight: 600 } },
    },
    MuiAppBar: {
      defaultProps: { elevation: 0, color: "inherit" },
      styleOverrides: {
        root: {
          backgroundColor: "rgba(255, 255, 255, 0.92)",
          backdropFilter: "blur(10px)",
          borderBottom: "1px solid rgba(43, 23, 8, 0.08)",
        },
      },
    },
    MuiAlert: {
      styleOverrides: { root: { borderRadius: 14 } },
    },
  },
});


const theme = responsiveFontSizes(baseTheme);

export default theme;