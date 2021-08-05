const state = () => ({
  stage3Data: {},
  numCardsForEachUser: [],
});

const getters = {};

const actions = {
  socket_updateStage3Data: function ({ commit }, stage3Data) {
    commit("updateStage3Data", stage3Data);
    commit(
      "setNumCardsForEachUser",
      stage3Data.cardsInBag.map((cards) => cards.length)
    );
  },
};

const mutations = {
  updateStage3Data: function (state, stage3Data) {
    state.stage3Data = stage3Data;
  },
  setNumCardsForEachUser: function (state, numCardsForEachUser) {
    state.numCardsForEachUser = numCardsForEachUser;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
