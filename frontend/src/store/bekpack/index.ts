import { actions } from "./actions";
import { getters } from "./getters";
import { mutations } from "./mutations";
import { BekpackState } from "./state";

const defaultState: BekpackState = {
    user: null,
    trips: { items: [], page: 0, size: 0, total: 0 },
    tripToEdit: null,
    hasBekpackAccount: null,
};

export const bekpackModule = {
    state: defaultState,
    mutations,
    actions,
    getters,
};
