import { api } from "@/api";
import { ActionContext } from "vuex";
import { dispatchCheckApiError } from "../main/actions";
import { State } from "../state";
import { commitSetItems } from "./mutations";
import { ItemState } from "./state";

type MainContext = ActionContext<ItemState, State>;

export const actions = {
    async actionGetItems(context: MainContext) {
        try {
            const response = await api.getMyItems(context.rootState.main.token)
            if (response) {
                commitSetItems(context, response.data)
            }
        }
        catch (error) {
            await dispatchCheckApiError(context, error);
        }
    }
}