import { configureStore } from "@reduxjs/toolkit";
import authReducer from "../features/auth/authSlice";
import cartReducer from "../features/cart/cartSlice";
import restaurantReducer from "../features/restaurant/restaurantSlice";
import { STORAGE_KEYS, safeRemove, safeSet } from "../utils/storage";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    cart: cartReducer,
    restaurant: restaurantReducer,
  },
});


store.subscribe(() => {
  const { auth, restaurant } = store.getState();

  if (auth.token !== null) {
    safeSet(STORAGE_KEYS.token, auth.token);
  } else {
    safeRemove(STORAGE_KEYS.token);
  }

  if (restaurant.selectedId !== null) {
    safeSet(STORAGE_KEYS.selectedRestaurantId, String(restaurant.selectedId));
  } else {
    safeRemove(STORAGE_KEYS.selectedRestaurantId);
  }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;