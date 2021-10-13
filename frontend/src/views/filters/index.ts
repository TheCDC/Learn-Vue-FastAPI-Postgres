export interface IFilter {
    name: string;
    filter: (...args) => void;
}
import Vue from "vue";

import { localeDate } from "./dateFormat";
import { truncate } from "./truncate";
export const filters: IFilter[] = [
    { name: "truncate", filter: truncate },
    { name: "localeDate", filter: localeDate },
];

export function bootstrapFilters() {
    filters.forEach((filter) => {
        Vue.filter(filter.name, filter.filter);
    });
}
