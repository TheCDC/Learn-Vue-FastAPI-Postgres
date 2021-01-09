import '@babel/polyfill';
// Import Component hooks before component definitions
import './component-hooks';
import Vue from 'vue';
import './plugins/vuetify';
import './plugins/vee-validate';
import App from './App.vue';
import router from './router';
import store from '@/store';
import './registerServiceWorker';
import 'vuetify/dist/vuetify.min.css';
import { bootstrapFilters } from './views/filters';
import vuetify from '@/plugins/vuetify';
Vue.config.productionTip = false;

bootstrapFilters();
new Vue({
  vuetify,
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
