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
};

const { read } = getStoreAccessors<ItemState, State>('');
export const readItemsOneUser = read(getters.itemsOneUser);
export const readItems = read(getters.items);
