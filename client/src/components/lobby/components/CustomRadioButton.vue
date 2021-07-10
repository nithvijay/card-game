<template>
  <div class="flex-grow">
    <label>
      <input
        type="radio"
        class="appearance-none hidden"
        name="radio"
        :value="text"
        v-model="scoreToWinRadioGroupModel"
      />
      <div
        class="cursor-pointer py-1 shadow-md rounded-xl text-center"
        :class="{
          'bg-blue-800 text-gray-100': scoreToWinRadioGroupModel === text, // checked
          'bg-blue-50 hover:bg-blue-100': scoreToWinRadioGroupModel !== text,
        }"
      >
        {{ text }}
      </div>
    </label>
  </div>
</template>

<script>
export default {
  props: {
    text: String,
    namespace: String,
    vuexRadioGroupState: String,
    vuexRadioGroupMutator: String,
  },
  computed: {
    scoreToWinRadioGroupModel: {
      get() {
        // this syntax is needed to reuse this component in other areas
        return this.$store.state[this.namespace][this.vuexRadioGroupState];
      },
      set(value) {
        this.$store.commit(
          `${[this.namespace]}/${this.vuexRadioGroupMutator}`,
          value
        );
      },
    },
  },
};
</script>

<style>
</style>