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
    bag_id?: number;
    description: string;
    name: string;
    parent_list_id: number;
    quantity: number;
}

export interface IBekpackItemListItemUpdate {
    bag_id?: number;
    description?: string;
    list_index?: number;
    name?: string;
    quantity?: number;
}
