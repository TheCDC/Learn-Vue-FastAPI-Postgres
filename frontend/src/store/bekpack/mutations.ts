import { IBekpackTrip, IBekpackUser } from '@/interfaces';
import { IPage } from '@/interfaces/common';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';
import { BekpackState } from './state';

export const mutations = {
    setUser(state: BekpackState, payload: IBekpackUser) {
        state.user = payload;
        state.hasBekpackAccount = true;
    },

    setTrips(state: BekpackState, payload: IPage<IBekpackTrip>) {
        state.trips = payload;
    },
    setTripsOne(state: BekpackState, payload: IBekpackTrip) {

        const others = state.trips.items.filter((u) => {
            return u.id !== payload.id;
        });
        others.unshift(payload);
        state.trips.items = others;
    },
    setTripToEdit(state: BekpackState, payload: IBekpackTrip) {
        state.tripToEdit = payload;
    },
    updateTrip(state: BekpackState, payload: IBekpackTrip) {
        const others = state.trips.items.filter((u) => {
            return u.id !== payload.id;
        });
        others.unshift(payload);
        state.trips.items = others;
    },
    deleteTrip(state: BekpackState, payload: IBekpackTrip) {
        const others = state.trips.items.filter((u) => {
            return u.id !== payload.id;
        });
        state.trips.items = others;
    },
};

const { commit } = getStoreAccessors<BekpackState, State>('');

export const commitDeleteTrip = commit(mutations.deleteTrip);
export const commitSetTrip = commit(mutations.setTripsOne);
export const commitSetTripToEdit = commit(mutations.setTripToEdit);
export const commitSetTrips = commit(mutations.setTrips);
export const commitSetUser = commit(mutations.setUser);
