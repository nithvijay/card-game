const state = () => ({
  stage4Data: {},
});

const getters = {};

const actions = {
  socket_updateStage4Data: function ({ commit }, stage4Data) {
    commit("updateStage4Data", stage4Data);
    commit("GeneralGame/setIsReady", stage4Data.isReady, { root: true });
    console.log("asdf");
  },
};

const mutations = {
  updateStage4Data: function (state, stage4Data) {
    state.stage4Data = stage4Data;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
