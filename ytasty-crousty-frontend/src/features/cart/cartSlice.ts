import { createSlice } from "@reduxjs/toolkit";
import type { RootState } from "../../app/store";

export interface CartItem {
  product_id: number;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];

  restaurant_id: number | null;
}

const initialState: CartState = {
  items: [],
  restaurant_id: null,
};

const cartSlice = createSlice({
  name: "cart",
  initialState,
  reducers: {
    
    clearCart: (state) => {
      state.items = [];
      state.restaurant_id = null;
    },
  },
});

export const { clearCart } = cartSlice.actions;

export const selectCartItemsCount = (state: RootState) =>
  state.cart.items.reduce((total, item) => total + item.quantity, 0);

export default cartSlice.reducer;