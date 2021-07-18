<template>
  <div
    class="
      grid grid-cols-12
      w-full
      max-w-sm
      bg-blue-800
      p-2
      rounded-md
      shadow-md
    "
  >
    <div class="text-left col-span-12 text-gray-100 font-semibold">
      {{ name }} - Inspector
    </div>
    <template v-for="(item, index) in summary">
      <div
        :key="`symbol-${index}`"
        class="col-span-6 text-left text-gray-200 px-2"
        :class="{
          'bg-green-700': item.sign === '+',
          'bg-red-700': item.sign === '-',
        }"
      >
        From {{ item.username }}
      </div>
      <div
        :key="`text-${index}`"
        class="col-span-6 text-right text-gray-200 px-2"
        :class="{
          'bg-green-700': item.sign === '+',
          'bg-red-700': item.sign === '-',
        }"
      >
        {{ item.quantity }} x {{ item.name }} -
        {{ totalValue(item.value, item.quantity) }}
        <i class="fas fa-coins" />
      </div>
    </template>
    <div
      class="
        border-t-2 border-blue-200
        text-right text-gray-100
        col-span-12
        px-1
      "
    >
      Total: {{ score }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    summary: Array,
    name: String,
    score: Number,
    inspectorIndex: Number,
  },
  methods: {
    totalValue(value, quantity) {
      return parseInt(value) * parseInt(quantity);
    },
  },
};
</script>

<style>
</style>