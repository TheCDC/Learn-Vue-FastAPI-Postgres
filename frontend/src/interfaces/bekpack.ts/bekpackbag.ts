export interface IBekpackBag {
    id: number;
    color: string;
    name: string;
    owner_id: number;
    owner_trip_id: number;
}
export interface IBekpackBagCreate {
    name: string;
    owner_id: number;
    owner_trip_id: number;
}
export interface IBekpackBagUpdate {
    color?: string;
    name?: string;
    owner_id?: number;
}
