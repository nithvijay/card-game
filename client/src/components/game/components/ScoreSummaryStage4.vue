<template>
  <div class="flex flex-col bg-blue-800 p-2 rounded-md shadow-md gap-1">
    <div class="text-gray-100 font-semibold">
      {{ name }}
    </div>
    <div
      class="rounded-md shadow-md text-sm"
      :class="{
        'bg-green-700': summary[0].sign === '+',
        'bg-red-700': summary[0].sign === '-',
      }"
    >
      <div
        v-for="(item, index) in summary"
        :key="index"
        class="text-right text-gray-200 px-2"
      >
        {{ item.quantity }} x {{ item.name }} -
        {{ totalValue(item.value, item.quantity) }}
        <i class="fas fa-coins" />
      </div>
    </div>
    <div class="border-t-2 border-blue-200 text-right text-gray-100">
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