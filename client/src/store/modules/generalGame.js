const state = () => ({
  generalGameData: {},
  userIndex: 0,
  isReady: [],
});

const getters = {
  getUserCards(state) {
    if (state.generalGameData.cards) {
      return state.generalGameData.cards[state.userIndex];
    } else {
      return [];
    }
  },
};

const actions = {
  socket_updateGeneralGameData: function ({ commit }, generalGameData) {
    commit("updateGeneralGameData", generalGameData);
  },
  socket_updateUserIndex: function ({ commit, state, rootState }) {
    const pid = rootState["General"]["pid"];
    commit("updateUserIndex", state.generalGameData.pids.indexOf(pid));
  },
};

const mutations = {
  updateGeneralGameData: function (state, generalGameData) {
    state.generalGameData = generalGameData;
  },
  updateUserIndex: function (state, userIndex) {
    state.userIndex = userIndex;
  },
  setIsReady: function (state, isReady) {
    state.isReady = isReady;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
