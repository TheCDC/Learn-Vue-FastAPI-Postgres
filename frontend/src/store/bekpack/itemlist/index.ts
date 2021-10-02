import { actions } from "./actions";
import { getters } from "./getters";
import { mutations } from "./mutations";
import { BekpackItemListState } from "./state";

const defaultState: BekpackItemListState = {
  itemlists: [],
  itemlistPage: { page: 0, items: [], size: 0, total: -1 },
};

export const bekpackItemlistModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
