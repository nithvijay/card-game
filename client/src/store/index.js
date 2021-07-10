import Vue from "vue";
import Vuex from "vuex";
import LobbyConfig from "./modules/lobby-config";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: { LobbyConfig },
  strict: process.env.NODE_ENV !== "production",
});
