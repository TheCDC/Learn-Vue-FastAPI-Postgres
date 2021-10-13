import { actions } from "./actions";
import { getters } from "./getters";
import { mutations } from "./mutations";
import { BekpackItemListItemState } from "./state";

const defaultState: BekpackItemListItemState = {
  itemlistitems: [],
};

export const bekpackItemlistitemModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
