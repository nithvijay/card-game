import Vue from "vue";
import VueSocketIOExt from "vue-socket.io-extended";
import { io } from "socket.io-client";

import App from "./App.vue";
import store from "./store";
import "./index.css";

const host =
  process.env.NODE_ENV !== "production"
    ? "http://localhost:5000"
    : process.env.REACT_APP_AWS_ADDRESS;
const socket = io(host);

Vue.config.productionTip = false;

Vue.use(VueSocketIOExt, socket, { store });

new Vue({
  store,
  render: (h) => h(App),
}).$mount("#app");
