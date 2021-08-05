<template>
  <div class="w-full flex justify-between gap-3 p-1">
    {{ name }}
    <div v-if="isReady" class="bg-green-100 rounded-xl px-2 text-green-900">
      Ready <i class="fas fa-check text-green-500" />
    </div>
    <div v-else class="bg-red-100 rounded-xl px-2 text-red-900">
      Not Ready <i class="fas fa-times text-red-500" />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isReady: Boolean,
    name: String,
  },
};
</script>

<style>
</style>