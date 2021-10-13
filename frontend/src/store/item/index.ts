import { actions } from "./actions";
import { getters } from "./getters";
import { mutations } from "./mutations";
import { ItemState } from "./state";

const defaultState: ItemState = {
    items: [],
};

export const itemModule = {
    state: defaultState,
    mutations,
    actions,
    getters,
};
