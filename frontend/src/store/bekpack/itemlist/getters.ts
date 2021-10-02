import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../../state";
import { BekpackItemListState } from "./state";

export const getters = {
  page: (state: BekpackItemListState) => state.itemlistPage,
  one: (state: BekpackItemListState) => (id: number) => {
    const filtered = state.itemlists.filter((i) => i.id === id);
    if (filtered.length > 0) {
      return { ...filtered[0] };
    }
  },
};

const { read } = getStoreAccessors<BekpackItemListState, State>("");
export const readItemlist = read(getters.one);
export const readItemlistPage = read(getters.page);
