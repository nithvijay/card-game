<template>
  <div>
    {{ stage5Data }}
    <div class="flex flex-col gap-1 p-2">
      <div
        class="flex bg-green-700 text-gray-100"
        v-for="(user, index) in generalGameData.usernames"
        :key="`username-${index}`"
      >
        <div>
          {{ user }}
        </div>
        <div>
          {{ generalGameData.scores[index] }}
        </div>
      </div>
    </div>

    <div class="text-center">
      <button
        type="button"
        class="
          text-lg
          bg-blue-700
          hover:bg-blue-600
          transition
          duration:300
          rounded-xl
          text-gray-100
          py-2
          px-20
        "
        @click="goToLobby"
      >
        Go To Lobby
      </button>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState("GameStage5", ["stage5Data"]),
    ...mapState("GeneralGame", ["generalGameData"]),
  },
  methods: {
    goToLobby() {
      this.$socket.client.emit("stage5GoToLobby", {
        pid: this.pid,
        room: this.room,
      });
    },
  },
  components: {},
};
</script>
