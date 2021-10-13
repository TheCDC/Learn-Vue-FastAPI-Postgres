export interface IBekpackItemListItem {
  id: number;
  bag_id?: number;
  parent_list_id: number;
  description: string;
  list_index: number;
  name: string;
  quantity: number;
}
export interface IBekpackItemListItemCreate {
  parent_list_id: number;
  bag_id?: number;

  description: string;
  name: string;
  quantity: number;
  list_index?: number;
}

export interface IBekpackItemListItemUpdate {
  bag_id?: number;
  description?: string;
  list_index?: number;
  name?: string;
  quantity?: number;
}
