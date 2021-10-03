export interface IBekpackItemListItem {
  id: number;
  bag_id?: number;
  description: string;
  list_index: number;
  name: string;
  parent_list_id: number;
  quantity: number;
}
export interface IBekpackItemListItemCreate {
  description: string;
  name: string;
  quantity: number;
}

export interface IBekpackItemListItemUpdate {
  bag_id?: number;
  description?: string;
  list_index?: number;
  name?: string;
  quantity?: number;
}
