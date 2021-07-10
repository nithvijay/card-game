<template>
  <div class="flex flex-col gap-2 items-center">
    <user-inspect-panel :name="name1" :numCards="numCards1" :cards="cards" />
    <user-inspect-panel :name="name2" :numCards="numCards2" :cards="cards" />
    <user-inspect-panel :name="name3" :numCards="numCards3" :cards="cards" />
    <user-inspect-panel :name="name4" :numCards="numCards4" :cards="cards" />

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
import UserInspectPanel from "../components/UserInspectPanel.vue";

export default {
  data: function () {
    return {
      name1: "novahoo",
      name2: "Chungus",
      name3: "op",
      name4: "mangos",
      name5: "sherlock",
      numCards1: 5,
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
    UserInspectPanel,
  },
};
</script>

<style>
</style>