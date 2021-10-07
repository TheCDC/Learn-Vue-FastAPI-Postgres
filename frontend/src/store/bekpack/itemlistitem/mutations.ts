import { IBekpackItemListItem } from "@/interfaces/bekpack.ts/bekpackitemlistitem";
import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../../state";
import { BekpackItemListItemState } from "./state";

export const mutations = {
  setOne(state: BekpackItemListItemState, payload: IBekpackItemListItem) {
    state.itemlistitems = [
      ...state.itemlistitems.filter((i) => i.id !== payload.id),
      payload,
    ];
  },
  deleteOne(state: BekpackItemListItemState, payload: IBekpackItemListItem) {
    state.itemlistitems = [
      ...state.itemlistitems.filter((i) => i.id !== payload.id),
    ];
  },
};

const { commit } = getStoreAccessors<BekpackItemListItemState, State>("");

export const commitSetItemlistitemOne = commit(mutations.setOne);
export const commitDeleteItemlistitemOne = commit(mutations.deleteOne);
