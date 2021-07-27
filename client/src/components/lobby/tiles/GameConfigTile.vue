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
        :vuexRadioGroupAction="scoreToWinRadioGroupActionName"
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
        :vuexRadioGroupAction="numCardsInHandRadioGroupActionName"
      />
    </div>
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
      scoreToWinRadioGroupActionName: "setScoreToWin",
      numCardsInHandRadioGroupStateName: "numCardsInHand",
      numCardsInHandRadioGroupActionName: "setNumCardsInHand",
    };
  },
  components: {
    CustomRadioButton,
  },
  computed: mapState("RoomLobby", ["scoreToWin", "numCardsInHand"]),
};
</script>

<style>
</style>