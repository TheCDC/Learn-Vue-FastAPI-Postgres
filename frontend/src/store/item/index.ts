import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { ItemState } from './state';

const defaultState: ItemState = {
    items: [],
};

export const itemModule = {
    state: defaultState,
    mutations,
    actions,
    getters,
};
