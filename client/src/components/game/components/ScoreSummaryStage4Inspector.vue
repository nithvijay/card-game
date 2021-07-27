<template>
  <div class="bg-blue-800 py-2 px-4 rounded-md shadow-md text-indigo-50">
    <div class="flex flex-col gap-2">
      <div class="text-gray-100 font-semibold">{{ name }} - Inspector</div>
      <div
        class="flex justify-between rounded-md px-1 gap-4"
        v-for="(items, index) in summary"
        :key="index"
        :class="{
          'bg-green-700': items[0].sign === '+',
          'bg-red-700': items[0].sign === '-',
        }"
      >
        <div class="flex items-center py-1">
          <div
            class="rounded-md px-3"
            :class="{
              'bg-green-800': items[0].sign === '+',
              'bg-red-800': items[0].sign === '-',
            }"
          >
            {{ items[0].username }}
          </div>
        </div>

        <div class="flex flex-col text-right text-sm">
          <div v-for="(item, index) in items" :key="index">
            {{ item.quantity }} x {{ item.name }} -
            {{ totalValue(item.value, item.quantity) }}
            <i class="fas fa-coins" />
          </div>
        </div>
      </div>
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