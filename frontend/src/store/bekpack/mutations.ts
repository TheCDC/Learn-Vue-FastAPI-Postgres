import { IBekpackTrip, IBekpackUser } from '@/interfaces';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';
import { BekpackState } from './state';

export const mutations = {
    setUser(state: BekpackState, payload: IBekpackUser) {
        const others = state.users.filter((u) => {
            return u.id !== payload.id;
        });
        others.push(payload);
        state.users = others;
    },
    setUsers(state: BekpackState, payload: IBekpackUser[]) {
        state.users = payload;
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
export const commitSetUsers = commit(mutations.setUsers);
export const commitUpdateTrip = commit(mutations.updateTrip);
