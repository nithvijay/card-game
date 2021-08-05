<template>
  <div class="flex flex-col">
    <div class="flex flex-col gap-1 p-2 items-center">
      <div
        class="flex justify-center gap-1 rounded-md w-80"
        :class="{
          'bg-yellow-300': index === 0,
          'bg-gray-300': index === 1,
          'bg-yellow-600': index === 2,
        }"
        v-for="(userIndex, index) in stage5Data.sortedScoresIndex"
        :key="index"
      >
        <div class="flex-1 text-right">
          <div class="text-3xl">
            {{ placementWording(index) }}
          </div>
        </div>
        <div class="flex-1 flex gap-1 self-center">
          <div class="px-1 text-lg self-center">
            {{ generalGameData.usernames[userIndex] }}
          </div>
          <div class="self-center">
            {{ generalGameData.scores[userIndex] }} <i class="fas fa-coins" />
          </div>
        </div>
      </div>
    </div>

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
    placementWording(index) {
      return `${index + 1}${this.placementEnding(index)}`;
    },
    placementEnding(place) {
      switch (place) {
        case 0:
          return "st";
        case 1:
          return "nd";
        case 2:
          return "rd";
        default:
          return "th";
      }
    },
  },
  components: {},
};
</script>
