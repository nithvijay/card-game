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
    <transition-group
      name="fade"
      tag="div"
      class="flex flex-wrap justify-center gap-1 p-1"
    >
      <user-card
        :key="card.id"
        v-for="card in cards"
        :card="card"
        :active="false"
        :isUserReady="true"
      />
    </transition-group>
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
.fade-move {
  transition: transform 1s;
}
</style>