import {
  createAsyncThunk,
  createSlice,
  isAnyOf,
  type PayloadAction,
} from "@reduxjs/toolkit";
import {
  getRestaurantById,
  getRestaurants,
  updateRestaurantAvailability,
} from "../../api/restaurantApi";
import type { Restaurant } from "../../types/restaurant";
import { getErrorMessage } from "../../utils/errors";
import { STORAGE_KEYS, safeGet } from "../../utils/storage";
import type { RootState } from "../../app/store";

type Status = "idle" | "loading" | "succeeded" | "failed";

interface RestaurantState {
  list: Restaurant[];
  selectedId: number | null;
  status: Status;
  error: string | null;
}

function readStoredSelectedId(): number | null {
  const raw = safeGet(STORAGE_KEYS.selectedRestaurantId);
  if (raw === null) return null;
  const id = Number(raw);
  return Number.isInteger(id) ? id : null;
}

const initialState: RestaurantState = {
  list: [],
  selectedId: readStoredSelectedId(),
  status: "idle",
  error: null,
};

interface ThunkConfig {
  rejectValue: string;
}

export const fetchRestaurants = createAsyncThunk<Restaurant[], void, ThunkConfig>(
  "restaurant/fetchAll",
  async (_, { rejectWithValue }) => {
    try {
      return await getRestaurants();
    } catch (error) {
      return rejectWithValue(getErrorMessage(error));
    }
  },
  {
    condition: (_, { getState }) => (getState() as RootState).restaurant.status !== "loading",
  },
);


export const fetchRestaurantById = createAsyncThunk<Restaurant, number, ThunkConfig>(
  "restaurant/fetchById",
  async (id, { rejectWithValue }) => {
    try {
      return await getRestaurantById(id);
    } catch (error) {
      return rejectWithValue(getErrorMessage(error));
    }
  },
);

// Admin uniquement
export const toggleRestaurantAvailability = createAsyncThunk<
  Restaurant,
  { id: number; isOpen: boolean },
  ThunkConfig
>("restaurant/toggleAvailability", async ({ id, isOpen }, { rejectWithValue }) => {
  try {
    return await updateRestaurantAvailability(id, isOpen);
  } catch (error) {
    return rejectWithValue(getErrorMessage(error));
  }
});

function upsert(list: Restaurant[], restaurant: Restaurant): void {
  const index = list.findIndex((item) => item.id === restaurant.id);
  if (index === -1) {
    list.push(restaurant);
  } else {
    list[index] = restaurant;
  }
}

const restaurantSlice = createSlice({
  name: "restaurant",
  initialState,
  reducers: {
    selectRestaurant: (state, action: PayloadAction<number | null>) => {
      state.selectedId = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchRestaurants.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchRestaurants.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.list = action.payload;

        if (state.selectedId !== null && !action.payload.some((r) => r.id === state.selectedId)) {
          state.selectedId = null;
        }
      })
      .addCase(fetchRestaurants.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload ?? action.error.message ?? "Impossible de charger les restaurants.";
      })
      .addMatcher(
        isAnyOf(fetchRestaurantById.fulfilled, toggleRestaurantAvailability.fulfilled),
        (state, action) => {
          upsert(state.list, action.payload);
        },
      );
  },
});

export const { selectRestaurant } = restaurantSlice.actions;

export const selectRestaurants = (state: RootState) => state.restaurant.list;
export const selectRestaurantStatus = (state: RootState) => state.restaurant.status;
export const selectRestaurantError = (state: RootState) => state.restaurant.error;

export const selectSelectedRestaurant = (state: RootState): Restaurant | null =>
  state.restaurant.list.find((r) => r.id === state.restaurant.selectedId) ?? null;


export const selectIsOrderingDisabled = (state: RootState): boolean => {
  const restaurant = selectSelectedRestaurant(state);
  return restaurant !== null && !restaurant.is_open;
};

export default restaurantSlice.reducer;