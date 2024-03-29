import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../state";
import { BekpackState } from "./state";

export const getters = {
    trips: (state: BekpackState) => state.trips,
    tripsOneUser: (state: BekpackState) => (userId: number) => {
        const filtered = state.trips.items.filter((item) => {
            return item.owner_id === userId;
        });
        return filtered;
    },
    tripsOneTrip: (state: BekpackState) => (tripId: number) => {
        const filtered = state.trips.items.filter((i) => i.id === tripId);
        if (filtered.length > 0) {
            return { ...filtered[0] };
        }
    },
    tripToEdit: (state: BekpackState) => {
        return state.tripToEdit;
    },
    user: (state: BekpackState) => state.user,
    userHasAccount: (state: BekpackState) => state.hasBekpackAccount,
};

const { read } = getStoreAccessors<BekpackState, State>("");
export const readTrips = read(getters.trips);
export const readTripsOne = read(getters.tripsOneTrip);
export const readTripsOneUser = read(getters.tripsOneUser);
export const readTripToEdit = read(getters.tripToEdit);
export const readUser = read(getters.user);
export const readUserHasAccount = read(getters.userHasAccount);
