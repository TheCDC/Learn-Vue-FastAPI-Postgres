import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { BekpackState } from './state';

const defaultState: BekpackState = {
    user: null,
    trips: [],
    hasBekpackAccount: null,
};

export const bekpackModule = {
    state: defaultState,
    mutations,
    actions,
    getters,
};
