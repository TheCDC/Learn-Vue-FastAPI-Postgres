import { api } from '@/api';
import { IItemCreate, IItemUpdate } from '@/interfaces';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { dispatchCheckApiError } from '../main/actions';
import { commitAddNotification, commitRemoveNotification } from '../main/mutations';
import { State } from '../state';
import { commitDeleteItem, commitSetItem, commitSetItems, commitUpdateItem } from './mutations';
import { ItemState } from './state';

type MainContext = ActionContext<ItemState, State>;

export const actions = {
    async actionGetItems(context: MainContext) {
        try {
            const response = await api.getMyItems(context.rootState.main.token);
            if (response) {
                commitSetItems(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCreateItem(context: MainContext, payload: IItemCreate) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.createItem(context.rootState.main.token, payload),
                await new Promise<void>((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetItem(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Item successfully created', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionUpdateItem(context: MainContext, payload: { id: number, item: IItemUpdate }) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.updateItem(context.rootState.main.token, payload.id, payload.item),
                await new Promise<void>((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitUpdateItem(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Item successfully updated', color: 'success' });

        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionDeleteItem(context: MainContext, payload: { id: number }) {
        try {

            const loadingNotification = { content: 'deleting', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.deleteItem(context.rootState.main.token, payload.id),
                await new Promise<void>((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitDeleteItem(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Item successfully deleted', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }

    },
};

const { dispatch } = getStoreAccessors<ItemState, State>('');

export const dispatchGetItems = dispatch(actions.actionGetItems);
export const dispatchCreateItem = dispatch(actions.actionCreateItem);
export const dispatchUpdateItem = dispatch(actions.actionUpdateItem);
export const dispatchDeleteItem = dispatch(actions.actionDeleteItem);
