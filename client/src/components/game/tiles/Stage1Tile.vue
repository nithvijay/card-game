<template>
  <div class="flex flex-col">
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
          p-2
        "
      >
        Discard Cards
      </button>
    </div>
  </div>
</template>

<script>
import UserCard from "../components/UserCard.vue";

export default {
  data: function () {
    return {
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
  },
};
</script>

<style>
</style>