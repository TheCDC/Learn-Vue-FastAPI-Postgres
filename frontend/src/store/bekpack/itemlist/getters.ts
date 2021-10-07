import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../../state";
import { BekpackItemListState } from "./state";

export const getters = {
  itemlistPage: (state: BekpackItemListState) => state.itemlistPage,
  itemlistOne: (state: BekpackItemListState) => (id: number) => {
    const filtered = state.itemlists.filter((i) => i.id === id);
    if (filtered.length > 0) {
      return { ...filtered[0] };
    }
  },
};

const { read } = getStoreAccessors<BekpackItemListState, State>("");
export const readItemlist = read(getters.itemlistOne);
export const readItemlistPage = read(getters.itemlistPage);
