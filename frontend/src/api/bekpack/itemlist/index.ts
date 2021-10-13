import { authHeaders, paginated } from "@/api/utils";
import { apiUrl } from "@/env";
import {
  IBekpackItemList,
  IBekpackItemListCreate,
  IBekpackItemListUpdate,
} from "@/interfaces/bekpack.ts/bekpackitemlist";
import { IPage, IPageRead } from "@/interfaces/common";
import axios from "axios";

export const api = {
  async getMulti(token: string, payload: { tripId: number; page: IPageRead }) {
    return axios.get<IPage<IBekpackItemList>>(
      `${apiUrl}/api/v1/bekpack/bekpacktrips/${payload.tripId}/lists`,
      paginated(authHeaders(token), payload.page)
    );
  },
  async getOne(token: string, payload: { id: number }) {
    return axios.get<IBekpackItemList>(
      `${apiUrl}/api/v1/bekpack/bekpackitemlists/${payload.id}`,
      authHeaders(token)
    );
  },
  async updateOne(
    token: string,
    payload: { id: number; item: IBekpackItemListUpdate }
  ) {
    return axios.put<IBekpackItemList>(
      `${apiUrl}/api/v1/bekpack/bekpackitemlists/${payload.id}`,
      payload.item,
      authHeaders(token)
    );
  },
  async createOne(token: string, payload: { item: IBekpackItemListCreate }) {
    return axios.post<IBekpackItemList>(
      `${apiUrl}/api/v1/bekpack/bekpackitemlists/?parent_trip_id=${payload.item.parent_trip_id}`,
      payload.item,
      authHeaders(token)
    );
  },
  async deleteOne(token: string, payload: { id: number }) {
    return axios.delete(
      `${apiUrl}/api/v1/bekpack/bekpackitemlists/${payload.id}`,
      authHeaders(token)
    );
  },
};
