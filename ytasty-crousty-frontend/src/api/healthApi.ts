import axiosInstance from "./axiosInstance";


export interface HealthResponse {
  status: string;
}

export const getHealth = async (): Promise<HealthResponse> => {
  const response = await axiosInstance.get<HealthResponse>("/health", { timeout: 5000 });
  return response.data;
};