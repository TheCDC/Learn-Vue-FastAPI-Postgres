import { IPageRead } from "@/interfaces/common";

export function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export function paginated(headerObject: object, page: IPageRead) {
  return { ...headerObject, params: page };
}
