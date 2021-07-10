<template>
  <div class="grid grid-cols-12 w-48 bg-blue-800 p-2 rounded-md shadow-md">
    <div class="text-left col-span-12 text-gray-100 font-semibold">
      {{ name }}
    </div>
    <template v-for="(item, index) in summary">
      <div
        :key="`symbol-${index}`"
        class="col-span-1 text-center text-gray-200"
      >
        {{ item.symbol }}
      </div>
      <div :key="`text-${index}`" class="text-right text-gray-200 col-span-11">
        {{ item.text }}
      </div>
    </template>
    <div
      class="border-t-2 border-blue-200 text-right text-gray-100 col-span-12"
    >
      Total: 12
    </div>
  </div>
</template>

<script>
export default {
  props: {
    summary: Array,
    name: String,
  },
};
</script>

<style>
</style>