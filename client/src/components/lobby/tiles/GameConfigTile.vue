<template>
  <div class="flex flex-col p-3 gap-2">
    <div>Points to Win</div>
    <div class="flex gap-1">
      <!-- scoreToWin Radio Group -->
      <custom-radio-button
        v-for="value in scoreToWinValues"
        :key="value"
        :text="value"
        namespace="RoomLobby"
        settingName="scoreToWin"
        :vuexRadioGroupState="scoreToWinRadioGroupStateName"
      />
    </div>

    <!-- numCardsInHand Radio Group -->
    <div class="mt-5">Number of Cards in Hand</div>
    <div class="flex gap-1">
      <custom-radio-button
        v-for="value in numCardsInHandValues"
        :key="value"
        :text="value"
        namespace="RoomLobby"
        settingName="numCardsInHand"
        :vuexRadioGroupState="numCardsInHandRadioGroupStateName"
      />
    </div>

    <div class="mt-5">Seed</div>
    <input
      class="
        bg-gray-100
        appearance-none
        border-2
        rounded
        py-2
        px-4
        text-gray-700
        focus:outline-none
        transition
        duration-300
        focus:bg-white
        border-gray-100
        focus:border-blue-800
      "
      :maxlength="15"
      type="text"
      v-model="seedModel"
      placeholder="Leave empty for random seed"
    />
  </div>
</template>

<script>
import { mapState } from "vuex";
import CustomRadioButton from "../components/CustomRadioButton.vue";

export default {
  data: function () {
    return {
      scoreToWinValues: ["30", "50", "70"],
      numCardsInHandValues: ["3", "5", "7", "9", "11"],
      scoreToWinRadioGroupStateName: "scoreToWin",
      numCardsInHandRadioGroupStateName: "numCardsInHand",
    };
  },
  components: {
    CustomRadioButton,
  },
  computed: {
    ...mapState("General", ["room"]),
    ...mapState("RoomLobby", [
      "scoreToWin",
      "numCardsInHand",
      "roomLobbyStatus",
    ]),
    seedModel: {
      get() {
        // this syntax is needed to reuse this component in other areas
        return this.$store.state["RoomLobby"]["seed"];
      },
      set(value) {
        this.$socket.client.emit("changeRoomConfig", {
          room: this.room,
          setting: "seed",
          value: value,
        });
      },
    },
  },
};
</script>

<style>
</style>