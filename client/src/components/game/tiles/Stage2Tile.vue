<template>
  <div class="flex flex-col">
    <div class="flex flex-wrap gap-2 p-2 justify-center">
      <user-num-cards-stage-2 :name="name1" :numCards="numCards1" />
      <user-num-cards-stage-2 :name="name2" :numCards="numCards2" />
      <user-num-cards-stage-2 :name="name3" :numCards="numCards3" />
      <user-num-cards-stage-2 :name="name4" :numCards="numCards4" />
      <user-num-cards-stage-2 :name="name5" :numCards="numCards5" />
    </div>

    <div class="flex flex-wrap gap-2 p-2 justify-center">
      <user-card :key="index" v-for="(card, index) in cards" :card="card" />
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
      >
        Submit
      </button>
    </div>
  </div>
</template>

<script>
import UserCard from "../components/UserCard.vue";
import UserNumCardsStage2 from "../components/UserNumCardsStage2.vue";

export default {
  data: function () {
    return {
      name1: "novahoo",
      name2: "Chungus",
      name3: "op",
      name4: "mangos",
      name5: "sherlock",
      numCards1: 1,
      numCards2: 5,
      numCards3: 4,
      numCards4: 2,
      numCards5: 3,
      cards: [
        {
          text: "Apples",
        },
        {
          text: "Cheeses",
        },
        {
          text: "Hammers",
        },
        {
          text: "Gems",
        },
        {
          text: "Apples",
        },
        {
          text: "Apples",
        },
      ],
    };
  },
  components: {
    UserCard,
    UserNumCardsStage2,
  },
};
</script>

<style>
</style>