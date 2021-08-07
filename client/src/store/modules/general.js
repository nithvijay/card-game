const state = () => ({
  username: localStorage.getItem("username")
    ? localStorage.getItem("username")
    : "",
  room: localStorage.getItem("room") ? localStorage.getItem("room") : "",
  pid: "",
  pageView: "login-view",
});

const getters = {
  sampleGetter(state) {
    return state.username;
  },
};

const actions = {
  setUsername: function ({ commit }, username) {
    commit("setUsername", username);
  },
  setRoom: function ({ commit }, room) {
    commit("setRoom", room);
  },
  socket_customEmit: function ({ commit }, data) {
    commit("setRoom", data);
  },
  socket_setPageView: function ({ commit }, data) {
    commit("setPageView", data);
  },
  socket_setPid: function ({ commit }, data) {
    commit("setPid", data);
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
    localStorage.setItem("pid", pid);
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
