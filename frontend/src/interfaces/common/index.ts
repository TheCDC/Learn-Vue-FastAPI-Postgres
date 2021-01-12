export interface IPage<T> {
    items: T[];
    total: number;
    page: number;
    size: number;
}

export interface IPageRead {
    page: number;
    size: number;
}
