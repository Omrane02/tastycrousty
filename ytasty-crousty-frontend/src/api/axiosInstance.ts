import axios from "axios";
import { STORAGE_KEYS, safeGet } from "../utils/storage";

const rawBaseURL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

const baseURL = rawBaseURL.replace(/\/+$/, "");

const axiosInstance = axios.create({
  baseURL,
  timeout: 15000,

  headers: baseURL.includes("ngrok") ? { "ngrok-skip-browser-warning": "true" } : {},
});

axiosInstance.interceptors.request.use((config) => {
  const token = safeGet(STORAGE_KEYS.token);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default axiosInstance;