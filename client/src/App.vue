<template>
  <div id="app" class="font-Montserrat">
    <div class="min-h-screen bg-gray-200">
      <game-view v-if="pageView === 'game-view'" />
      <login-view v-if="pageView === 'login-view'" />
      <room-lobby-view v-if="pageView === 'room-lobby-view'" />
      <button
        class="bg-white p-1 rounded-md"
        type="button"
        @click.prevent="clearStorage"
      >
        Clear Storage
      </button>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import GameView from "./views/GameView.vue";
import LoginView from "./views/LoginView.vue";
import RoomLobbyView from "./views/RoomLobbyView.vue";

export default {
  name: "App",
  data: function () {
    return {
      screenOptions: ["login", "game", "room-lobby"],
      screenIndex: 0,
    };
  },
  methods: {
    switchViews: function () {
      this.screenIndex = (this.screenIndex + 1) % this.screenOptions.length;
    },
    clearStorage: function () {
      localStorage.clear();
      this.$socket.client.emit("delete");
    },
  },
  computed: {
    screen: function () {
      return this.screenOptions[this.screenIndex];
    },
    ...mapState("General", ["pageView"]),
  },
  components: {
    GameView,
    LoginView,
    RoomLobbyView,
  },
  sockets: {
    connect() {
      console.log("socket connected");
    },
    debug(data) {
      console.log(data);
    },
  },
  created() {
    const pid = localStorage.getItem("pid");
    this.$socket.client.emit("pageLoaded", pid);
  },
};
</script>