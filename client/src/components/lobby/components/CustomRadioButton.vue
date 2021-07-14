<template>
  <div class="flex-grow">
    <label>
      <input
        type="radio"
        class="appearance-none hidden"
        name="radio"
        :value="text"
        v-model="RadioGroupModel"
      />
      <div
        class="cursor-pointer py-1 shadow-md rounded-xl text-center"
        :class="{
          'bg-blue-800 text-gray-100': RadioGroupModel === text, // checked
          'bg-blue-50 hover:bg-blue-100': RadioGroupModel !== text,
        }"
      >
        {{ text }}
      </div>
    </label>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  props: {
    text: String,
    namespace: String,
    settingName: String,
    vuexRadioGroupState: String,
    vuexRadioGroupAction: String,
  },
  computed: {
    RadioGroupModel: {
      get() {
        // this syntax is needed to reuse this component in other areas
        return this.$store.state[this.namespace][this.vuexRadioGroupState];
      },
      set(value) {
        console.log("how");
        this.$socket.client.emit("changeRoomConfig", {
          room: this.room,
          setting: this.settingName,
          value: value,
        });

        // this.$store.dispatch(
        //   `${[this.namespace]}/${this.vuexRadioGroupAction}`,
        //   value
        // );
      },
    },
    ...mapState("General", ["room"]),
  },
};
</script>

<style>
</style>