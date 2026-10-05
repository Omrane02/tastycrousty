import axiosInstance from "./axiosInstance";
import type { Restaurant } from "../types/restaurant";

export const getRestaurants = async (): Promise<Restaurant[]> => {
  const response = await axiosInstance.get<Restaurant[]>("/restaurants");
  return response.data;
};

export const getRestaurantById = async (id: number): Promise<Restaurant> => {
  const response = await axiosInstance.get<Restaurant>(`/restaurants/${id}`);
  return response.data;
};

// Admin uniquement
export const updateRestaurantAvailability = async (
  id: number,
  isOpen: boolean,
): Promise<Restaurant> => {
  const response = await axiosInstance.patch<Restaurant>(`/restaurants/${id}/availability`, {
    is_open: isOpen,
  });
  return response.data;
};