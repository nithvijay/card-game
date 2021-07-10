const state = () => ({
  username,
  room,
  pid,
  pageView,
});

const getters = {};

const actions = {
  setUsername: function ({ commit }, username) {
    commit("setUsername", username);
  },
  setRoom: function ({ commit }, room) {
    commit("setRoom", room);
  },
  setRoom: function ({ commit }, room) {
    commit("setRoom", room);
  },
  setRoom: function ({ commit }, room) {
    commit("setRoom", room);
  },
};

const mutations = {
  setUsername: function (state, username) {
    state.username = username;
  },
  setRoom: function (state, room) {
    state.room = room;
  },
  setPid: function (state, pid) {
    state.pid = pid;
  },
  setPageView: function (state, pageView) {
    state.pageView = pageView;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
