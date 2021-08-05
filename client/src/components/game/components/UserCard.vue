<template>
  <div
    class="
      flex flex-col
      w-20
      h-32
      rounded-md
      shadow-md
      text-center
      justify-center
      transition
      duration-150
      fade-complete-item
    "
    :class="{
      'bg-blue-200 hover:bg-blue-300 cursor-pointer': !isUserReady & !active,
      'bg-red-200 hover:bg-red-300 cursor-pointer': !isUserReady & active,
      'bg-blue-200': isUserReady & !active,
      'bg-red-200': isUserReady & active,
    }"
    @click="cardClickMethod(card.id)"
  >
    <i class="fas text-2xl m-3" :class="iconClass"></i>
    <div class="text-sm">{{ card.name }}</div>

    <div class="font-extrabold">{{ card.value }} - {{ card.id }}</div>
  </div>
</template>

<script>
export default {
  props: {
    card: Object,
    active: Boolean,
    clickMethod: Function,
    isUserReady: Boolean,
  },
  data: function () {
    return {
      iconMapper: {
        Apple: "fa-apple-alt",
        Cheese: "fa-cheese",
        Hammers: "fa-hammer",
        Gems: "fa-gem",
      },
    };
  },
  computed: {
    iconClass() {
      return this.iconMapper[this.card.name];
    },
  },
  methods: {
    cardClickMethod(id) {
      if (!this.isUserReady) {
        this.clickMethod(id);
      }
    },
  },
};
</script>

<style>
</style>