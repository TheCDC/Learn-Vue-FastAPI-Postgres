import Vue from "vue";
import Vuex, { StoreOptions } from "vuex";

import { adminModule } from "./admin";
import { bekpackModule } from "./bekpack";
import { itemModule } from "./item";
import { mainModule } from "./main";
import { State } from "./state";

Vue.use(Vuex);

const storeOptions: StoreOptions<State> = {
  modules: {
    main: mainModule,
    admin: adminModule,
    items: itemModule,
    bekpack: bekpackModule,
  },
};

export const store = new Vuex.Store<State>(storeOptions);

export default store;
