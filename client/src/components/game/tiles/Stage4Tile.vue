<template>
  <div>
    <div class="flex flex-wrap items-start justify-center gap-1 p-2">
      <score-summary-stage-4-inspector
        :summary="stage4Data.scoringData[generalGameData.inspectorIndex]"
        :name="generalGameData.usernames[generalGameData.inspectorIndex]"
        :score="generalGameData.scores[generalGameData.inspectorIndex]"
      />

      <score-summary-stage-4
        v-for="(user, index) in nonInspectorCards"
        :key="index"
        :summary="user.summary"
        :name="user.name"
        :score="user.score"
      />
    </div>

    <div class="text-center">
      <button
        v-if="isUserNotReady"
        type="button"
        class="
          text-lg
          bg-blue-800
          hover:bg-blue-700
          active:bg-blue-600
          transition
          duration:300
          rounded-md
          shadow-md
          text-gray-100
          py-2
          px-20
        "
        @click="markReady"
      >
        Next Round
      </button>
      <div v-else-if="getUsersNotReady.length">
        Waiting for {{ getUsersNotReady }}
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

import ScoreSummaryStage4 from "../components/ScoreSummaryStage4.vue";
import ScoreSummaryStage4Inspector from "../components/ScoreSummaryStage4Inspector.vue";

export default {
  computed: {
    ...mapState("GameStage4", ["stage4Data"]),
    ...mapState("GeneralGame", ["generalGameData", "userIndex"]),
    ...mapState("General", ["username", "room", "pid"]),
    nonInspectorCards() {
      const toReturn = [];
      for (
        let index = 0;
        index < this.generalGameData.usernames.length;
        index++
      ) {
        if (index !== this.generalGameData.inspectorIndex) {
          toReturn.push({
            summary: this.stage4Data.scoringData[index],
            name: this.generalGameData.usernames[index],
            score: this.generalGameData.scores[index],
          });
        }
      }
      return toReturn;
    },
    getUsersNotReady() {
      if (this.generalGameData.usernames && this.stage4Data.isReady) {
        const usersNotReady = this.generalGameData.usernames.filter(
          (username, index) => !this.stage4Data.isReady[index]
        );
        if (usersNotReady.length === 0) {
          return "";
        } else if (usersNotReady.length === 1) {
          return usersNotReady[0];
        } else {
          return (
            usersNotReady.slice(0, -1).join(", ") +
            ` and ${usersNotReady.slice(-1)}`
          );
        }
      } else {
        return [];
      }
    },
    isUserNotReady() {
      if (this.stage4Data.isReady) {
        return !this.stage4Data.isReady[this.userIndex];
      } else {
        return false;
      }
    },
  },
  methods: {
    markReady() {
      this.$socket.client.emit("stage4UserReady", {
        pid: this.pid,
        room: this.room,
      });
    },
  },
  components: {
    ScoreSummaryStage4,
    ScoreSummaryStage4Inspector,
  },
};
</script>
