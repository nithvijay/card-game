const state = () => ({
  stage2Data: {},
  cardsSelected: [],
});

const getters = {};

const actions = {
  socket_updateStage2Data: function ({ commit }, stage2Data) {
    commit("updateStage2Data", stage2Data);
    commit("GeneralGame/setIsReady", stage2Data.isReady, { root: true });
  },
  initializeCardsSelected: function ({ commit }, cards) {
    console.log("stage 2");
    commit("updateCardsSelected", new Array(cards.length).fill(false));
  },
  flipCardInCardsSelected: function ({ commit, state, rootState }, flipIndex) {
    const current = state.cardsSelected.slice();
    current[flipIndex] = !current[flipIndex];
    commit("updateCardsSelected", current);

    this._vm.$socket.client.emit("stage2SelectCard", {
      numCards: current.filter(Boolean).length,
      userIndex: rootState["GeneralGame"]["userIndex"],
      room: rootState["General"]["room"],
    });
  },
};

const mutations = {
  updateStage2Data: function (state, stage2Data) {
    state.stage2Data = stage2Data;
  },
  updateCardsSelected: function (state, cardsSelected) {
    state.cardsSelected = cardsSelected;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
