import axios from "axios";
import axiosInstance from "./axiosInstance";
import { logout } from "../features/auth/authSlice";
import { STORAGE_KEYS, safeGet } from "../utils/storage";
import type { AppDispatch } from "../app/store";

export const SESSION_EXPIRED_EVENT = "auth:session-expired";

let responseInterceptorId: number | null = null;

export function setupInterceptors(dispatch: AppDispatch): void {
  if (responseInterceptorId !== null) {
    axiosInstance.interceptors.response.eject(responseInterceptorId);
  }

  responseInterceptorId = axiosInstance.interceptors.response.use(
    (response) => response,
    (error: unknown) => {
      if (axios.isAxiosError(error)) {
        const isUnauthorized = error.response?.status === 401;
        const isLoginCall = (error.config?.url ?? "").includes("/auth/login");
        const hadToken = safeGet(STORAGE_KEYS.token) !== null;

        if (isUnauthorized && !isLoginCall && hadToken) {
          dispatch(logout());
          window.dispatchEvent(new Event(SESSION_EXPIRED_EVENT));
        }
      }
      return Promise.reject(error);
    },
  );
}