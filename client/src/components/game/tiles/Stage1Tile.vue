<template>
  <div class="flex flex-col">
    <div>
      {{ userIndex }}
    </div>
    <transition-group
      name="fade"
      class="flex flex-wrap gap-2 p-2 justify-center"
      tag="div"
    >
      <user-card
        :key="card.id"
        v-for="(card, index) in getUserCards"
        :card="card"
        :active="cardsSelected[index]"
        :clickMethod="selectCardToDiscard"
        :isUserReady="!isUserNotReady"
      />
    </transition-group>
    {{ cardsSelected }}
    <div class="text-center">
      <button
        v-if="isUserNotReady"
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
      <div v-else-if="getUsersNotReady.length">
        Waiting for {{ getUsersNotReady }}
      </div>
    </div>
  </div>
</template>

<script>
import UserCard from "../components/UserCard.vue";
import { mapState, mapGetters, mapMutations } from "vuex";

export default {
  data() {
    return {};
  },
  methods: {
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
      this.$socket.client.emit("stage1UserReady", {
        pid: this.pid,
        room: this.room,
        cardsSelectedIds: cardsSelectedIds,
      });
    },
    ...mapMutations("GameStage1", ["flipCardInCardsSelected"]),
  },
  computed: {
    ...mapState("General", ["username", "room", "pid"]),
    ...mapState("GeneralGame", ["generalGameData", "userIndex"]),
    ...mapState("GameStage1", ["stage1Data", "cardsSelected"]),
    ...mapGetters("GeneralGame", ["getUserCards"]),
    getUsersNotReady() {
      if (this.generalGameData.usernames && this.stage1Data.isReady) {
        const usersNotReady = this.generalGameData.usernames.filter(
          (username, index) => !this.stage1Data.isReady[index]
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
      if (this.stage1Data.isReady) {
        return !this.stage1Data.isReady[this.userIndex];
      } else {
        return false;
      }
    },
  },
  components: {
    UserCard,
  },
};
</script>

<style scoped>
/* .fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
} */

/* .fade-complete-item {
  transition: all 1s;
}

.fade-complete-enter,
.fade-complete-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
.fade-complete-leave-active {
  position: absolute;
} */
</style>