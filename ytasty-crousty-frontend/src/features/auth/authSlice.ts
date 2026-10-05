import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import { jwtDecode } from "jwt-decode";
import { isRole, type AuthUser } from "../../types/auth";
import { STORAGE_KEYS, safeGet, safeRemove } from "../../utils/storage";
import type { RootState } from "../../app/store";

interface JwtPayload {
  sub?: string;
  role?: string;
  restaurant_id?: number | null;
  exp?: number;
}

interface AuthState {
  token: string | null;
  user: AuthUser | null;
}

export function userFromToken(token: string): AuthUser | null {
  try {
    const payload = jwtDecode<JwtPayload>(token);
    if (payload.exp !== undefined && payload.exp * 1000 <= Date.now()) return null;
    if (!payload.sub || !isRole(payload.role)) return null;
    return {
      username: payload.sub,
      role: payload.role,
      restaurant_id: payload.restaurant_id ?? null,
    };
  } catch {
    return null;
  }
}

function loadInitialState(): AuthState {
  const token = safeGet(STORAGE_KEYS.token);
  if (token === null) return { token: null, user: null };

  const user = userFromToken(token);
  if (user === null) {
    safeRemove(STORAGE_KEYS.token);
    return { token: null, user: null };
  }
  return { token, user };
}

const authSlice = createSlice({
  name: "auth",
  initialState: loadInitialState(),
  reducers: {

    setCredentials: (state, action: PayloadAction<{ token: string }>) => {
      const user = userFromToken(action.payload.token);
      if (user === null) return;
      state.token = action.payload.token;
      state.user = user;
    },
    logout: (state) => {
      state.token = null;
      state.user = null;
    },
  },
});

export const { setCredentials, logout } = authSlice.actions;

export const selectCurrentUser = (state: RootState) => state.auth.user;
export const selectIsAuthenticated = (state: RootState) => state.auth.token !== null;

export default authSlice.reducer;