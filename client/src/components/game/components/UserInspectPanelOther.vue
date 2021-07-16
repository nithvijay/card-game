<template>
  <div
    class="flex flex-col p-2 rounded-md shadow-md items-center w-3/4 gap-1"
    :class="{
      'bg-green-600': inspectorDecision === '',
      'bg-red-400': inspectorDecision === 'inspected',
      'bg-purple-600': inspectorDecision === 'let go',
    }"
  >
    <div class="flex justify-between gap-1">
      <div
        class="px-2 rounded-md shadow-md text-gray-100"
        :class="{
          'bg-green-800': inspectorDecision === '',
          'bg-red-600': inspectorDecision === 'inspected',
          'bg-purple-800': inspectorDecision === 'let go',
        }"
      >
        {{ text }}
      </div>
    </div>

    <user-num-cards-stage-2 :name="name" :numCards="numCards" />
    <transition name="fade">
      <div class="flex flex-wrap justify-center gap-1 p-1">
        <user-card
          :key="index"
          v-for="(card, index) in cards"
          :card="card"
          :active="false"
          :isUserReady="true"
        />
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
    inspectorDecision: String,
  },
  data() {
    return {
      decisionMapper: {
        "": "Waiting for inspector",
        inspected: "Inspected",
        "let go": "Not Checked",
      },
    };
  },
  computed: {
    text() {
      return this.decisionMapper[this.inspectorDecision];
    },
  },
  components: {
    UserCard,
    UserNumCardsStage2,
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