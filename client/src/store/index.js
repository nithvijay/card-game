import Vue from "vue";
import Vuex from "vuex";
import General from "./modules/general";
import RoomLobby from "./modules/roomLobby";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  getters: {},
  modules: { RoomLobby, General },
  strict: process.env.NODE_ENV !== "production",
});
