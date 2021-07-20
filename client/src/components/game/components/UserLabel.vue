<template>
  <div
    class="flex rounded-lg gap-1 px-2"
    :class="{ 'bg-green-700': state, 'bg-red-700': !state }"
  >
    <div class="font-extrabold text-gray-100">{{ name }} ({{ score }})</div>
    <div v-if="isInspector" class="text-gray-200">
      <i class="fas fa-gavel" />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isInspector: Boolean,
    name: String,
    state: Boolean,
    score: Number,
  },
};
</script>

<style>
</style>