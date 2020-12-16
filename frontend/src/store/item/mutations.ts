import { IItem } from "@/interfaces";
import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../state";
import { ItemState } from "./state";

export const mutations = {
    setItems(state: ItemState, payload: IItem[]) {
        state.items = payload;
    }
}

const { commit } = getStoreAccessors<ItemState, State>('');

export const commitSetItems = commit(mutations.setItems);