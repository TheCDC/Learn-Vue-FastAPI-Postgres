import { authHeaders, paginated } from "@/api/utils";
import { apiUrl } from "@/env";
import {
  IBekpackItemListItem,
  IBekpackItemListItemCreate,
  IBekpackItemListItemUpdate,
} from "@/interfaces/bekpack.ts/bekpackitemlistitem";
import { IPage, IPageRead } from "@/interfaces/common";
import axios from "axios";

export const api = {
  async getMulti(token: string, payload: { tripId: number; page: IPageRead }) {
    return axios.get<IPage<IBekpackItemListItem>>(
      `${apiUrl}/api/v1/bekpack/bekpacktrips/${payload.tripId}/lists`,
      paginated(authHeaders(token), payload.page)
    );
  },
  async getOne(token: string, payload: { id: number }) {
    return axios.get<IBekpackItemListItem>(
      `${apiUrl}/api/v1/bekpack/bekpackitemlistitems/${payload.id}`,
      authHeaders(token)
    );
  },
  async updateOne(
    token: string,
    payload: { id: number; item: IBekpackItemListItemUpdate }
  ) {
    return axios.put<IBekpackItemListItem>(
      `${apiUrl}/api/v1/bekpack/bekpackitemlistitems/${payload.id}`,
      payload.item,
      authHeaders(token)
    );
  },
  async createOne(
    token: string,
    payload: { item: IBekpackItemListItemCreate }
  ) {
    return axios.post<IBekpackItemListItem>(
      `${apiUrl}/api/v1/bekpack/bekpackitemlistitems/?parent_list_id=${payload.item.parent_itemlist_id}`,
      payload.item,
      authHeaders(token)
    );
  },
  async deleteOne(token: string, payload: { id: number }) {
    return axios.delete(
      `${apiUrl}/api/v1/bekpack/bekpackitemlistitems/${payload.id}`,
      authHeaders(token)
    );
  },
};
