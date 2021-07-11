import { getField, updateField } from "vuex-map-fields";

const state = () => ({
  scoreToWin: 50,
  scoreToWinRadioGroup: "50",
  numCardsInHandRadioGroup: "5",
  roomLobbyStatus: {},
});

const getters = {
  // getRoomLobbyMembers: (state) => (pid) => {
  //   return state.roomLobbyStatus.members.filter(
  //     (member) => member.pid !== pid
  //   )[0].isReady;
  // },
  getScoreToWin: (state) => {
    state.scoreToWin;
  },
  getField,
};

const actions = {
  setScoreToWin: function ({ commit }, scoreToWin) {
    commit("setScoreToWin", scoreToWin);
  },
  setScoreToWinRadioGroup: function ({ commit }, scoreToWinRadioGroup) {
    commit("setScoreToWinRadioGroup", scoreToWinRadioGroup);
  },
  setNumCardsInHandRadioGroup: function ({ commit }, numCardsInHandRadioGroup) {
    commit("setNumCardsInHandRadioGroup", numCardsInHandRadioGroup);
  },
  socket_updateRoomLobbyStatus: function ({ commit }, roomLobbyStatus) {
    commit("updateRoomLobbyStatus", roomLobbyStatus);
  },
};

const mutations = {
  setScoreToWin: function (state, scoreToWin) {
    state.scoreToWin = scoreToWin;
  },
  setScoreToWinRadioGroup: function (state, scoreToWinRadioGroup) {
    state.scoreToWinRadioGroup = scoreToWinRadioGroup;
  },
  setNumCardsInHandRadioGroup: function (state, numCardsInHandRadioGroup) {
    state.numCardsInHandRadioGroup = numCardsInHandRadioGroup;
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
