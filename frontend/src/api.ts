import axios from 'axios';
import { apiUrl } from '@/env';
import {
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
  IItemCreate,
  IItemUpdate,
  IBekpackTripCreate,
  IBekpackTripUpdate,
  IItem,
  IBekpackUser,
  IBekpackTrip,
} from './interfaces';
import { IPage, IPageRead } from './interfaces/common';


function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

function paginated(headerObject: object, page: IPageRead) {
  return { ...headerObject, params: page };
}
export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(`${apiUrl}/api/v1/users/me`, data, authHeaders(token));
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiUrl}/api/v1/users/`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${apiUrl}/api/v1/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
  async getMyItems(token: string) {
    return axios.get<IItem[]>(`${apiUrl}/api/v1/items`, authHeaders(token));
  },
  async createItem(token: string, data: IItemCreate) {
    return axios.post<IItem>(`${apiUrl}/api/v1/items`, data, authHeaders(token));
  },
  async updateItem(token: string, itemId: number, data: IItemUpdate) {
    return axios.put<IItem>(`${apiUrl}/api/v1/items/${itemId}`, data, authHeaders(token));
  },
  async deleteItem(token: string, itemId) {
    return axios.delete(`${apiUrl}/api/v1/items/${itemId}`, authHeaders(token));
  },
  async createBekpackUser(token: string) {
    return axios.post<IBekpackUser>(`${apiUrl}/api/v1/bekpack/bekpackusers`, {}, authHeaders(token));
  },
  async getMyBekpackUser(token: string) {
    return axios.get<IBekpackUser>(`${apiUrl}/api/v1/bekpack/bekpackusers/me`, authHeaders(token))
      .catch((error) => {
        if (error.response.status !== 404) {
          return error;
        }
        return null;
      });
  },
  async getBekpackTrip(token: string, id: number) {
    return axios.get<IBekpackTrip>(`${apiUrl}/api/v1/bekpack/bekpacktrips/${id}`, authHeaders(token));
  },
  async createBekpackTrip(token: string, data: IBekpackTripCreate) {
    return axios.post<IBekpackTrip>(`${apiUrl}/api/v1/bekpack/bekpacktrips/`, data, authHeaders(token));
  },
  async updateBekpackTrip(token: string, tripId: number, data: IBekpackTripUpdate) {
    return axios.put<IBekpackTrip>(`${apiUrl}/api/v1/bekpack/bekpacktrips/${tripId}`, data, authHeaders(token));
  },
  async deleteBekpackTrip(token: string, tripId: number) {
    return axios.delete(`${apiUrl}/api/v1/bekpack/bekpacktrips/${tripId}`, authHeaders(token));
  },
  async getMyBekpackTrips(token: string, page: IPageRead) {
    return axios.get<IPage<IBekpackTrip>>(
      `${apiUrl}/api/v1/bekpack/bekpacktrips/mine/all`, paginated(authHeaders(token), page)).catch((error) => {
        if (error.response.status !== 404) {
          return error;
        }
        return null;
      });
  },
};
