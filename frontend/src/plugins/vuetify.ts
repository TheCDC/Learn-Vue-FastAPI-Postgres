import Vue from "vue";
import Vuetify from "vuetify";

// import '@mdi/font/css/materialdesignicons.css'; // Ensure you are using css-loader
const opts = {
  iconfont: "md",
};
Vue.use(Vuetify);

export default new Vuetify({
  icons:
    { iconfont: "md" },
});
