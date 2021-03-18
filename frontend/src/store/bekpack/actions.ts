import { api } from "@/api";
import { IBekpackTripCreate, IBekpackTripUpdate, IItemCreate, IItemUpdate } from "@/interfaces";
import { IPageRead } from "@/interfaces/common";
import { getStoreAccessors } from "typesafe-vuex";
import { ActionContext } from "vuex";
import { dispatchCheckApiError } from "../main/actions";
import { commitAddNotification, commitRemoveNotification } from "../main/mutations";
import { State } from "../state";
import { commitDeleteTrip, commitSetTrip, commitSetTrips, commitSetTripToEdit, commitSetUser } from "./mutations";
import { BekpackState } from "./state";
type MainContext = ActionContext<BekpackState, State>;

export const actions = {
    async actionCreateUser(context: MainContext) {
        try {
            const response = await api.createBekpackUser(context.rootState.main.token);
            if (response) {
                commitSetUser(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetUser(context: MainContext) {
        try {
            const response = await api.getMyBekpackUser(context.rootState.main.token);
            if (response) {
                commitSetUser(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetMyTrips(context: MainContext, payload: { page: IPageRead; }) {
        try {
            const response = await api.getMyBekpackTrips(context.rootState.main.token, payload.page);
            if (response) {
                commitSetTrips(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetTripToEdit(context: MainContext, payload: { id: number; }) {
        try {
            const response = await api.getBekpackTrip(context.rootState.main.token, payload.id);
            if (response) {
                commitSetTripToEdit(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetTrip(context: MainContext, payload: { id: number; }) {
        try {
            const response = await api.getBekpackTrip(context.rootState.main.token, payload.id);
            if (response) {
                commitSetTrip(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCreateTrip(context: MainContext, payload: IBekpackTripCreate) {
        try {
            const loadingNotification = { content: "saving", showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.createBekpackTrip(context.rootState.main.token, payload),
                await new Promise<void>((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetTrip(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: "Trip successfully created", color: "success" });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionUpdateTrip(context: MainContext, payload: { id: number, item: IBekpackTripUpdate; }) {
        try {
            const loadingNotification = { content: "saving", showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.updateBekpackTrip(context.rootState.main.token, payload.id, payload.item),
                await new Promise<void>((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetTrip(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: "Trip successfully updated", color: "success" });

        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionDeleteTrip(context: MainContext, payload: { id: number; }) {
        try {

            const loadingNotification = { content: "deleting", showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.deleteBekpackTrip(context.rootState.main.token, payload.id),
                await new Promise<void>((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitDeleteTrip(context, response.data);
            // refresh this page of trips
            const responseRead = await api.getMyBekpackTrips(context.rootState.main.token, context.state.trips);
            commitSetTrips(context, responseRead.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: "Item successfully deleted", color: "success" });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
};
const { dispatch } = getStoreAccessors<BekpackState, State>("");
export const dispatchCreateBekpackUser = dispatch(actions.actionCreateUser);
export const dispatchCreateTrip = dispatch(actions.actionCreateTrip);
export const dispatchDeleteTrip = dispatch(actions.actionDeleteTrip);
export const dispatchGetBekpackUser = dispatch(actions.actionGetUser);
export const dispatchGetMyTrips = dispatch(actions.actionGetMyTrips);
export const dispatchGetTripToEdit = dispatch(actions.actionGetTripToEdit);
export const dispatchGetTrip = dispatch(actions.actionGetTrip);
export const dispatchUpdateTrip = dispatch(actions.actionUpdateTrip);
