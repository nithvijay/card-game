<template>
  <div class="text-center">
    <button
      type="button"
      v-if="isReady"
      @click.prevent="clickedReady"
      class="
        text-lg
        w-32
        bg-green-100
        hover:bg-green-200
        transition
        duration:300
        text-green-900
        rounded-xl
        p-2
      "
    >
      Ready <i class="fas fa-check text-green-500" />
    </button>
    <button
      type="button"
      v-else
      @click.prevent="clickedReady"
      class="
        text-lg
        w-32
        bg-red-100
        hover:bg-red-200
        transition
        duration:300
        rounded-xl
        p-2
        text-red-900
      "
    >
      Not Ready <i class="fas fa-times text-red-500" />
    </button>
  </div>
</template>

<script>
export default {
  data: function () {
    return { isReady: false };
  },
  methods: {
    clickedReady() {
      this.isReady = !this.isReady;
    },
  },
};
</script>

<style>
</style>