<template>
  <div class="flex flex-col">
    <div class="flex flex-wrap gap-2 p-2 justify-center">
      <div v-for="(username, index) in generalGameData.usernames" :key="index">
        <user-num-cards-stage-2
          v-if="index !== generalGameData.inspectorIndex"
          :name="username"
          :numCards="stage2Data.numCardsForEachUser[index]"
        />
      </div>
    </div>
    <div
      v-if="generalGameData.inspectorIndex !== userIndex"
      class="flex flex-wrap gap-2 p-2 justify-center"
    >
      <user-card
        :key="card.id"
        v-for="(card, index) in getUserCards"
        :card="card"
        :active="activeCards[index]"
        :clickMethod="selectCardToDiscard"
        :isUserReady="!isUserNotReady"
      />
    </div>
    <div>
      <div class="text-center">
        <button
          v-if="validCardsSelected && isUserNotReady"
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
        <div v-else-if="isUserNotReady">
          <i class="fas fa-exclamation-circle" />
          Select between 1-5 cards
        </div>
        <div v-else-if="getUsersNotReady.length">
          Waiting for {{ getUsersNotReady }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions, mapMutations } from "vuex";
import UserCard from "../components/UserCard.vue";
import UserNumCardsStage2 from "../components/UserNumCardsStage2.vue";

export default {
  methods: {
    ...mapActions("GameStage2", ["flipCardInCardsSelected"]),
    ...mapMutations("GameStage2", ["updateCardsSelected"]),
    selectCardToDiscard(id) {
      if (this.isUserNotReady) {
        this.flipCardInCardsSelected(
          this.getUserCards.map((card) => card.id).indexOf(id)
        );
      }
      // inefficient
    },
    markReady() {
      const cardsSelectedIds = this.getUserCards
        .filter((card, index) => this.cardsSelected[index])
        .map((card) => card.id);
      this.$socket.client.emit("stage2UserReady", {
        pid: this.pid,
        room: this.room,
        cardsSelectedIds: cardsSelectedIds,
      });
    },
  },
  computed: {
    ...mapState("GameStage2", ["stage2Data", "cardsSelected"]),
    ...mapState("GeneralGame", ["generalGameData", "userIndex"]),
    ...mapState("General", ["pid", "room"]),
    ...mapGetters("GeneralGame", ["getUserCards"]),
    getUsersNotReady() {
      if (this.generalGameData.usernames && this.stage2Data.isReady) {
        const usersNotReady = this.generalGameData.usernames.filter(
          (username, index) => !this.stage2Data.isReady[index]
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
      if (this.stage2Data.isReady) {
        return !this.stage2Data.isReady[this.userIndex];
      } else {
        return false;
      }
    },
    validCardsSelected() {
      const numSelected = this.cardsSelected.filter(Boolean).length;
      return numSelected > 0 && numSelected < 6;
    },
    activeCards() {
      if (!this.isUserNotReady) {
        // they are ready
        const chosenCards = this.stage2Data.cardsChosen[this.userIndex]; //ids of cards chosen
        const to_mutate = new Array(this.cardsSelected.length)
          .fill(false)
          .map((value, index) =>
            chosenCards.includes(this.getUserCards[index].id)
          );
        this.updateCardsSelected(to_mutate);
        console.log("in activeCards");
      }
      return this.cardsSelected;
    },
  },

  components: {
    UserCard,
    UserNumCardsStage2,
  },
};
</script>

<style>
</style>