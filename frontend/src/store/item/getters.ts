import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';
import { ItemState } from './state';

export const getters = {
    items: (state: ItemState) => state.items,
    itemsOneUser: (state: ItemState) => (userId: number) => {
        const filteredItems = state.items.filter((item) => {
            return item.owner_id === userId;
        });
        return filteredItems;
    },
    itemsOneItem: (state: ItemState) => (itemId: number) => {
        const filtered = state.items.filter((i) => i.id === itemId);
        if (filtered.length > 0) {
            return { ...filtered[0] };
        }
    },
};

const { read } = getStoreAccessors<ItemState, State>('');
export const readItemsOneUser = read(getters.itemsOneUser);
export const readItems = read(getters.items);
export const readItemsOne = read(getters.itemsOneItem);
