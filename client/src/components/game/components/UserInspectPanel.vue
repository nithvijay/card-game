<template>
  <div
    class="
      flex flex-col
      p-2
      bg-green-600
      rounded-md
      shadow-md
      items-center
      w-3/4
      gap-1
    "
  >
    <div class="flex justify-between gap-1">
      <button @click="showCards" class="px-2 rounded-md shadow-md bg-green-200">
        Inspect
      </button>
      <button @click="hideCards" class="px-2 rounded-md shadow-md bg-green-200">
        Let Go
      </button>
    </div>

    <user-num-cards-stage-2 :name="name" :numCards="numCards" />
    <transition name="fade">
      <div v-if="isCardsShown" class="flex flex-wrap justify-center gap-1 p-1">
        <user-card :key="index" v-for="(card, index) in cards" :card="card" />
      </div>
    </transition>
  </div>
</template>

<script>
import UserCard from "./UserCard.vue";
import UserNumCardsStage2 from "./UserNumCardsStage2.vue";
export default {
  props: {
    name: String,
    numCards: Number,
    cards: Array,
  },
  data: function () {
    return {
      isCardsShown: false,
    };
  },
  components: {
    UserCard,
    UserNumCardsStage2,
  },
  methods: {
    showCards() {
      this.isCardsShown = true;
    },
    hideCards() {
      this.isCardsShown = false;
    },
  },
};
</script>


<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>