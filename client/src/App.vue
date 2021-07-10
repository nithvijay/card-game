<template>
  <div id="app" class="font-Montserrat">
    <div class="min-h-screen bg-gray-200">
      <game-view v-if="screen === 'game'" />
      <login-view v-if="screen === 'login'" />
      <room-lobby-view v-if="screen === 'room-lobby'" />
      <button
        class="bg-white p-1 rounded-md"
        type="button"
        @click.prevent="switchViews"
      >
        Click Here
      </button>
    </div>
  </div>
</template>

<script>
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
  },
  computed: {
    screen: function () {
      return this.screenOptions[this.screenIndex];
    },
  },
  components: {
    GameView,
    LoginView,
    RoomLobbyView,
  },
};
</script>


<style>
</style>
