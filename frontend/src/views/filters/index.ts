export interface IFilter {
    name: string;
    filter: (...args) => void;
}
import Vue from 'vue';

import { truncate } from './truncate';
export const filters: IFilter[] = [
    { name: 'truncate', filter: truncate },
];

export function bootstrapFilters() {
    filters.forEach((filter) => {
        Vue.filter(filter.name, filter.filter);
    });
}
