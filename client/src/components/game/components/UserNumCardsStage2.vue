<template>
  <div
    class="
      flex flex-col
      text-center
      w-32
      h-32
      bg-blue-700
      text-gray-100
      shadow-md
      rounded-md
    "
  >
    <div class="border-b-2 border-blue-500">
      {{ name }}
    </div>
    <div>{{ numCards }} Card(s)</div>

    <!-- <button @click.prevent="increment">Increment</button> -->
    <div class="relative mx-2">
      <transition-group name="fade">
        <div
          class="
            absolute
            border-blue-200 border-2
            bg-green-700
            rounded-md
            w-12
            h-16
          "
          :class="`left-${(index - 1) * 4}`"
          v-for="index in numCards"
          :key="index"
        />
      </transition-group>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    name: String,
    numCards: Number,
  },
  methods: {
    increment() {
      this.numCards++;
    },
  },
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>