import Vue from "vue";
import VueSocketIOExt from "vue-socket.io-extended";
import { io } from "socket.io-client";

import App from "./App.vue";
import store from "./store";
import "./index.css";

const socket = io("http://localhost:5000");

Vue.config.productionTip = false;

Vue.use(VueSocketIOExt, socket, { store });

new Vue({
  store,
  render: (h) => h(App),
}).$mount("#app");
