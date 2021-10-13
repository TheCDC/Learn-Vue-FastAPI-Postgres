import { api } from "@/api";
import {
  IBekpackTripCreate,
  IBekpackTripUpdate,
  IItemCreate,
  IItemUpdate,
} from "@/interfaces";
import {
  IBekpackItemListItem,
  IBekpackItemListItemCreate,
  IBekpackItemListItemUpdate,
} from "@/interfaces/bekpack.ts/bekpackitemlistitem";
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
  commitDeleteItemlistitemOne,
  commitSetItemlistitemOne,
} from "./mutations";
import { BekpackItemListItemState } from "./state";
type MainContext = ActionContext<BekpackItemListItemState, State>;

export const actions = {
  async actionGetOne(context: MainContext, payload: { id: number }) {
    try {
      const response = await api.bekpack.itemlistitem.getOne(
        context.rootState.main.token,
        payload
      );
      if (response) {
        commitSetItemlistitemOne(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionCreateOne(
    context: MainContext,
    payload: IBekpackItemListItemCreate
  ) {
    try {
      const loadingNotification = { content: "saving", showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.bekpack.itemlistitem.createOne(context.rootState.main.token, {
            item: payload,
          }),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitSetItemlistitemOne(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Trip successfully created",
        color: "success",
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionUpdateOne(
    context: MainContext,
    payload: { id: number; item: IBekpackItemListItemUpdate }
  ) {
    try {
      const loadingNotification = { content: "saving", showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.bekpack.itemlistitem.updateOne(context.rootState.main.token, {
            id: payload.id,
            item: payload.item,
          }),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitSetItemlistitemOne(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Trip successfully updated",
        color: "success",
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionDeleteOne(context: MainContext, payload: IBekpackItemListItem) {
    try {
      const loadingNotification = { content: "deleting", showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.bekpack.itemlistitem.deleteOne(
            context.rootState.main.token,
            payload
          ),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitDeleteItemlistitemOne(context, payload);
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
};
const { dispatch } = getStoreAccessors<BekpackItemListItemState, State>("");
export const dispatchCreateBekpackItemlistitem = dispatch(
  actions.actionCreateOne
);
export const dispatchDeleteBekpackItemlistitem = dispatch(
  actions.actionDeleteOne
);
export const dispatchUpdateBekpackItemlistitem = dispatch(
  actions.actionUpdateOne
);
export const dispatchGetBekpackItemlistitem = dispatch(actions.actionGetOne);
