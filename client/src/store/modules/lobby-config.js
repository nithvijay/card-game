const state = () => ({
  scoreToWin: 50,
  scoreToWinRadioGroup: "50",
  numCardsInHandRadioGroup: "5",
});

const getters = {};

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
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
