import { getField, updateField } from "vuex-map-fields";

const state = () => ({
  scoreToWin: "",
  numCardsInHand: "",
  seed: "",
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
    commit("setSeed", roomLobbyStatus["config"]["seed"]);
  },
};

const mutations = {
  setScoreToWin: function (state, scoreToWin) {
    state.scoreToWin = scoreToWin;
  },
  setNumCardsInHand: function (state, numCardsInHand) {
    state.numCardsInHand = numCardsInHand;
  },
  setSeed: function (state, seed) {
    state.seed = seed;
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
