import Vue from 'vue';
import Vuex, { StoreOptions } from 'vuex';

import { mainModule } from './main';
import { State } from './state';
import { adminModule } from './admin';
import { itemModule } from './item';
import { bekpackModule } from './bekpack';

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
