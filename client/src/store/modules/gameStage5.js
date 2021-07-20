const state = () => ({
  stage5Data: {},
});

const getters = {};

const actions = {
  socket_updateStage5Data: function ({ commit }, stage5Data) {
    commit("updateStage5Data", stage5Data);
    console.log("asdf");
  },
};

const mutations = {
  updateStage5Data: function (state, stage5Data) {
    state.stage5Data = stage5Data;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
