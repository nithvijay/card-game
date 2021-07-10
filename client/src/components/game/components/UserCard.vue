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
      cursor-pointer
      transition
      duration-150
      bg-blue-200
      hover:bg-blue-300
      active:bg-red-500
    "
  >
    <i class="fas text-2xl m-3" :class="iconClass"></i>
    <div class="text-sm">
      {{ card.text }}
    </div>

    <div class="font-extrabold">
      {{ materialValue }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    card: Object,
  },
  data: function () {
    return {
      iconMapper: {
        Apples: "fa-apple-alt",
        Cheeses: "fa-cheese",
        Hammers: "fa-hammer",
        Gems: "fa-gem",
      },
      valueMapper: {
        Apples: "3",
        Cheeses: "5",
        Hammers: "7",
        Gems: "9",
      },
    };
  },
  computed: {
    iconClass() {
      return this.iconMapper[this.card.text];
    },
    materialValue() {
      return this.valueMapper[this.card.text];
    },
  },
};
</script>

<style>
</style>