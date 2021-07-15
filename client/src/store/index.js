import Vue from "vue";
import Vuex from "vuex";
import General from "./modules/general";
import RoomLobby from "./modules/roomLobby";
import GeneralGame from "./modules/generalGame";
import GameStage1 from "./modules/gameStage1";
import GameStage2 from "./modules/gameStage2";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  getters: {},
  modules: { RoomLobby, General, GeneralGame, GameStage1, GameStage2 },
  strict: process.env.NODE_ENV !== "production",
});
