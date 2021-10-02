import { IBekpackItemListItem } from "./bekpackitemlistitem";

export interface IBekpackItemList {
  color: string;
  name: string;
  id: number;
  items: IBekpackItemListItem;
}
export interface IBekpackItemListUpdate {
  color?: string;
  name?: string;
}
export interface IBekpackItemListCreate {
  color?: string;
  name: string;
}
