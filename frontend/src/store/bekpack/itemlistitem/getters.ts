import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../../state";
import { BekpackItemListItemState } from "./state";

export const getters = {
  itemlistitemOne: (state: BekpackItemListItemState) => (id: number) => {
    const filtered = state.itemlistitems.filter((i) => i.id === id);
    if (filtered.length > 0) {
      return { ...filtered[0] };
    }
  },
};

const { read } = getStoreAccessors<BekpackItemListItemState, State>("");
export const readItemlistitem = read(getters.itemlistitemOne);
