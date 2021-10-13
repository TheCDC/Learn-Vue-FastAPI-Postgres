import { api } from "@/api";
import {
  IBekpackTripCreate,
  IBekpackTripUpdate,
  IItemCreate,
  IItemUpdate,
} from "@/interfaces";
import {
  IBekpackItemList,
  IBekpackItemListCreate,
} from "@/interfaces/bekpack.ts/bekpackitemlist";
import { IBekpackItemListItemUpdate } from "@/interfaces/bekpack.ts/bekpackitemlistitem";
import { IPageRead } from "@/interfaces/common";
import { getStoreAccessors } from "typesafe-vuex";
import { ActionContext } from "vuex";
import { dispatchCheckApiError } from "../../main/actions";
import {
  commitAddNotification,
  commitRemoveNotification,
} from "../../main/mutations";
import { State } from "../../state";
import {
  commitDeleteItemlistOne,
  commitSetItemlistOne,
  commitSetItemlistPage,
} from "./mutations";
import { BekpackItemListState } from "./state";
type MainContext = ActionContext<BekpackItemListState, State>;

export const actions = {
  async actionItemlistGetOne(context: MainContext, payload: { id: number }) {
    try {
      const response = await api.bekpack.itemlist.getOne(
        context.rootState.main.token,
        payload
      );
      if (response) {
        commitSetItemlistOne(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionItemlistGetMulti(
    context: MainContext,
    payload: { tripId: number; page: IPageRead }
  ) {
    try {
      const response = await api.bekpack.itemlist.getMulti(
        context.rootState.main.token,
        payload
      );
      if (response) {
        commitSetItemlistPage(context, { page: response.data });
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionItemlistCreateOne(
    context: MainContext,
    payload: IBekpackItemListCreate
  ) {
    try {
      const loadingNotification = { content: "saving", showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.bekpack.itemlist.createOne(context.rootState.main.token, {
            item: payload,
          }),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitSetItemlistOne(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Trip successfully created",
        color: "success",
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionItemlistUpdateOne(
    context: MainContext,
    payload: { id: number; item: IBekpackItemListItemUpdate }
  ) {
    try {
      const loadingNotification = { content: "saving", showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.bekpack.itemlist.updateOne(context.rootState.main.token, {
            id: payload.id,
            item: payload.item,
          }),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitSetItemlistOne(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Trip successfully updated",
        color: "success",
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionItemlistDeleteOne(
    context: MainContext,
    payload: IBekpackItemList
  ) {
    try {
      const loadingNotification = { content: "deleting", showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.bekpack.itemlist.deleteOne(context.rootState.main.token, payload),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitDeleteItemlistOne(context, payload);
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
};
const { dispatch } = getStoreAccessors<BekpackItemListState, State>("");
export const dispatchCreateBekpackItemlist = dispatch(
  actions.actionItemlistCreateOne
);
export const dispatchDeleteBekpackItemlist = dispatch(
  actions.actionItemlistDeleteOne
);
export const dispatchUpdateBekpackItemlist = dispatch(
  actions.actionItemlistUpdateOne
);
export const dispatchGetBekpackItemlist = dispatch(
  actions.actionItemlistGetOne
);
export const dispatchGetBekpackItemlistMulti = dispatch(
  actions.actionItemlistGetMulti
);
