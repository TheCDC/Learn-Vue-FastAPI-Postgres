import { IBekpackItemList } from "@/interfaces/bekpack.ts/bekpackitemlist";
import { IPage } from "@/interfaces/common";
import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../../state";
import { BekpackItemListState } from "./state";

export const mutations = {
  setPage(
    state: BekpackItemListState,
    payload: { page: IPage<IBekpackItemList> }
  ) {
    const idsIncoming = new Set(payload.page.items.map((i) => i.id));
    state.itemlists = state.itemlists.filter((i) => !idsIncoming.has(i.id));
    state.itemlists = [...state.itemlists, ...payload.page.items];
  },
  setOne(state: BekpackItemListState, payload: IBekpackItemList) {
    state.itemlists = [
      ...state.itemlists.filter((i) => i.id !== payload.id),
      payload,
    ];
  },
  deleteOne(state: BekpackItemListState, payload: IBekpackItemList) {
    state.itemlists = [...state.itemlists.filter((i) => i.id !== payload.id)];
  },
};

const { commit } = getStoreAccessors<BekpackItemListState, State>("");

export const commitSetItemlistPage = commit(mutations.setPage);
export const commitSetItemlistOne = commit(mutations.setOne);
export const commitDeleteItemlistOne = commit(mutations.deleteOne);
