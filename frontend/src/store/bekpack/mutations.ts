import { IBekpackTrip, IBekpackUser } from '@/interfaces';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';
import { BekpackState } from './state';

export const mutations = {
    setUser(state: BekpackState, payload: IBekpackUser) {
        state.user = payload;
        state.hasBekpackAccount = true;
    },

    setTrip(state: BekpackState, payload: IBekpackTrip) {
        state.trips.push(payload);
    },
    setTrips(state: BekpackState, payload: IBekpackTrip[]) {
        state.trips = payload;
    },
    updateTrip(state: BekpackState, payload: IBekpackTrip) {
        const others = state.trips.filter((u) => {
            return u.id !== payload.id;
        });
        others.push(payload);
        state.trips = others;

    },
    deleteTrip(state: BekpackState, payload: IBekpackTrip) {
        const others = state.trips.filter((u) => {
            return u.id !== payload.id;
        });
        state.trips = others;
    },
};

const { commit } = getStoreAccessors<BekpackState, State>('');

export const commitDeleteTrip = commit(mutations.deleteTrip);
export const commitSetTrip = commit(mutations.setTrip);
export const commitSetTrips = commit(mutations.setTrips);
export const commitSetUser = commit(mutations.setUser);
export const commitUpdateTrip = commit(mutations.updateTrip);
