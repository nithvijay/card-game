<template>
  <div class="flex flex-wrap gap-2 justify-center">
    <template v-if="generalGameData.inspectorIndex === userIndex">
      <component
        v-for="(user, index) in nonInspectorCards"
        :key="index"
        :name="user.username"
        :pid="user.pid"
        :numCards="user.numCards"
        :cards="user.cards"
        :is="mapDecisionToComponent(user.inspectorDecision)"
        :inspectorDecision="user.inspectorDecision"
      />
    </template>
    <template v-else>
      <user-inspect-panel-other
        v-for="(user, index) in nonInspectorCards"
        :key="index"
        :name="user.username"
        :numCards="user.numCards"
        :cards="user.cards"
        :inspectorDecision="user.inspectorDecision"
      />
    </template>

    <div v-if="isRoundDone" class="text-center">
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
        @click="markReady"
      >
        Submit
      </button>
    </div>
  </div>
</template>

<script>
import UserInspectPanelInspector from "../components/UserInspectPanelInspector.vue";
import UserInspectPanelOther from "../components/UserInspectPanelOther.vue";
import { mapState } from "vuex";
export default {
  computed: {
    ...mapState("GameStage3", ["stage3Data", "numCardsForEachUser"]),
    ...mapState("GeneralGame", ["generalGameData", "userIndex"]),
    ...mapState("General", ["pid", "room"]),
    nonInspectorCards() {
      const toReturn = [];
      for (
        let index = 0;
        index < this.generalGameData.usernames.length;
        index++
      ) {
        if (index !== this.generalGameData.inspectorIndex) {
          toReturn.push({
            username: this.generalGameData.usernames[index],
            pid: this.generalGameData.pids[index],
            cards: this.stage3Data.cardsInBag[index],
            numCards: this.numCardsForEachUser[index],
            inspectorDecision: this.stage3Data.inspectorDecisions[index],
          });
        }
      }
      return toReturn;
    },
    isRoundDone() {
      return (
        this.generalGameData.inspectorIndex === this.userIndex &&
        this.stage3Data.isChecked.every(Boolean)
      );
    },
  },
  methods: {
    mapDecisionToComponent(inspectorDecision) {
      return inspectorDecision === ""
        ? "user-inspect-panel-inspector"
        : "user-inspect-panel-other";
    },
    markReady() {
      this.$socket.client.emit("stage3Ready", {
        room: this.room,
      });
    },
  },
  components: {
    UserInspectPanelInspector,
    UserInspectPanelOther,
  },
};
</script>

<style>
</style>