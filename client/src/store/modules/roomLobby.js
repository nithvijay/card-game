import { getField, updateField } from "vuex-map-fields";

const state = () => ({
  scoreToWin: "",
  numCardsInHand: "",
  roomLobbyStatus: {},
});

const getters = {
  someGetter(state) {
    return state.roomLobbyStatus.members;
  },
  getField,
};

const actions = {
  setScoreToWin: function ({ commit }, scoreToWin) {
    commit("setScoreToWin", scoreToWin);
  },
  setNumCardsInHand: function ({ commit }, numCardsInHand) {
    commit("setNumCardsInHand", numCardsInHand);
  },
  socket_updateRoomLobbyStatus: function ({ commit }, roomLobbyStatus) {
    commit("updateRoomLobbyStatus", roomLobbyStatus);
    commit("setScoreToWin", roomLobbyStatus["config"]["scoreToWin"]);
    commit("setNumCardsInHand", roomLobbyStatus["config"]["numCardsInHand"]);
  },
  socket_updateRoomConfig: function ({ commit }, roomConfig) {
    // potentially remove because redundant code, but improves efficiency a little bit?
    switch (roomConfig["setting"]) {
      case "scoreToWin":
        commit("setScoreToWin", roomConfig["value"]);
        break;
      case "numCardsInHand":
        commit("setNumCardsInHand", roomConfig["value"]);
        break;
    }
  },
};

const mutations = {
  setScoreToWin: function (state, scoreToWin) {
    state.scoreToWin = scoreToWin;
  },
  setNumCardsInHand: function (state, numCardsInHand) {
    state.numCardsInHand = numCardsInHand;
  },
  updateRoomLobbyStatus: function (state, roomLobbyStatus) {
    state.roomLobbyStatus = roomLobbyStatus;
  },
  updateField,
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
