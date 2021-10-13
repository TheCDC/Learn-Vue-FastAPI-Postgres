import { IItem } from "@/interfaces";
import { getStoreAccessors } from "typesafe-vuex";
import { itemModule } from ".";
import { State } from "../state";
import { ItemState } from "./state";

export const mutations = {
    setItems(state: ItemState, payload: IItem[]) {
        state.items = payload;
    },
    setItem(state: ItemState, payload: IItem) {
        state.items.push(payload);
    },
    updateItem(state: ItemState, payload: IItem) {
        const otherItems = state.items.filter((item) => item.id !== payload.id);
        otherItems.push(payload);
        state.items = otherItems;
    },
    deleteItem(state: ItemState, payload: IItem) {
        const otherItems = state.items.filter((item) => item.id !== payload.id);
        state.items = otherItems;
    },
};

const { commit } = getStoreAccessors<ItemState, State>("");

export const commitSetItems = commit(mutations.setItems);
export const commitSetItem = commit(mutations.setItem);
export const commitUpdateItem = commit(mutations.setItem);
export const commitDeleteItem = commit(mutations.deleteItem);
