export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IItem {
    id: number;
    title: string;
    description: string;
    owner_id: number;
}

export interface IItemCreate {
    title: string;
    description: string;
}

export interface IItemUpdate {
    title?: string;
    description?: string;
}


export interface IBekpackUser {
    id: number;
    is_active: boolean;
    owner_id: number;
}

export interface IBekpackTrip {
    color: string;
    id: number;
    is_active: boolean;
    name: string;
    owner_id: number;
}

export interface IBekpackTripCreate {
    color: string;
    name: string;
}

export interface IBekpackTripUpdate {
    color?: string;
    is_active?: boolean;
    name?: string;
}
