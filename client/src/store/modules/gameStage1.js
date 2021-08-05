const state = () => ({
  stage1Data: {},
  cardsSelected: [],
});

const getters = {};

const actions = {
  socket_updateStage1Data: function ({ commit }, stage1Data) {
    commit("updateStage1Data", stage1Data);
    commit("GeneralGame/setIsReady", stage1Data.isReady, { root: true });
  },
  socket_initializeCardsSelected: function ({ commit }, numCards) {
    commit("updateCardsSelected", new Array(parseInt(numCards)).fill(false));
  },
};

const mutations = {
  updateStage1Data: function (state, stage1Data) {
    state.stage1Data = stage1Data;
  },
  updateCardsSelected: function (state, cardsSelected) {
    state.cardsSelected = cardsSelected;
  },
  flipCardInCardsSelected: function (state, flipIndex) {
    const current = state.cardsSelected.slice();
    current[flipIndex] = !current[flipIndex];
    state.cardsSelected = current;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
