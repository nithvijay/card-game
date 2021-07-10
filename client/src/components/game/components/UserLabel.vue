<template>
  <div
    class="
      flex
      bg-gradient-to-tr
      from-green-700
      to-green-800
      rounded-lg
      gap-1
      px-2
    "
  >
    <div class="font-extrabold text-gray-100">{{ name }}</div>
    <div v-if="isSherriff" class="text-gray-200">
      <i class="fas fa-gavel" />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isSherriff: Boolean,
    name: String,
  },
};
</script>

<style>
</style>