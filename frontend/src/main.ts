import vuetify from "@/plugins/vuetify";
import store from "@/store";
import "@babel/polyfill";
import Vue from "vue";
import "vuetify/dist/vuetify.min.css";
import App from "./App.vue";
// Import Component hooks before component definitions
import "./component-hooks";
import "./plugins/vee-validate";
import "./plugins/vuetify";
import "./registerServiceWorker";
import router from "./router";
import { bootstrapFilters } from "./views/filters";
Vue.config.productionTip = false;

bootstrapFilters();
new Vue({
  vuetify,
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
