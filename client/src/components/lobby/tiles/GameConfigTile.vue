<template>
  <div class="flex flex-col p-3 gap-2">
    <div>Points to Win</div>
    <div class="flex gap-1">
      <!-- scoreToWin Radio Group -->
      <custom-radio-button
        text="30"
        namespace="LobbyConfig"
        :vuexRadioGroupState="scoreToWinRadioGroupStateName"
        :vuexRadioGroupMutator="scoreToWinRadioGroupMutatorName"
      />
      <custom-radio-button
        text="50"
        namespace="LobbyConfig"
        :vuexRadioGroupState="scoreToWinRadioGroupStateName"
        :vuexRadioGroupMutator="scoreToWinRadioGroupMutatorName"
      />
      <custom-radio-button
        text="70"
        namespace="LobbyConfig"
        :vuexRadioGroupState="scoreToWinRadioGroupStateName"
        :vuexRadioGroupMutator="scoreToWinRadioGroupMutatorName"
      />
    </div>

    <!-- numCardsInHand Radio Group -->
    <div class="mt-5">Number of Cards in Hand</div>
    <div class="flex gap-1">
      <custom-radio-button
        text="3"
        namespace="LobbyConfig"
        :vuexRadioGroupState="numCardsInHandRadioGroupStateName"
        :vuexRadioGroupMutator="numCardsInHandRadioGroupMutatorName"
      />

      <custom-radio-button
        text="4"
        namespace="LobbyConfig"
        :vuexRadioGroupState="numCardsInHandRadioGroupStateName"
        :vuexRadioGroupMutator="numCardsInHandRadioGroupMutatorName"
      />

      <custom-radio-button
        text="5"
        namespace="LobbyConfig"
        :vuexRadioGroupState="numCardsInHandRadioGroupStateName"
        :vuexRadioGroupMutator="numCardsInHandRadioGroupMutatorName"
      />
      <custom-radio-button
        text="6"
        namespace="LobbyConfig"
        :vuexRadioGroupState="numCardsInHandRadioGroupStateName"
        :vuexRadioGroupMutator="numCardsInHandRadioGroupMutatorName"
      />
      <custom-radio-button
        text="7"
        namespace="LobbyConfig"
        :vuexRadioGroupState="numCardsInHandRadioGroupStateName"
        :vuexRadioGroupMutator="numCardsInHandRadioGroupMutatorName"
      />
    </div>
    {{ scoreToWinRadioGroup }}
    {{ numCardsInHandRadioGroup }}
  </div>
</template>

<script>
import { mapState } from "vuex";
import CustomRadioButton from "../components/CustomRadioButton.vue";

export default {
  data: function () {
    return {
      scoreToWinRadioGroupStateName: "scoreToWinRadioGroup",
      scoreToWinRadioGroupMutatorName: "setScoreToWinRadioGroup",
      numCardsInHandRadioGroupStateName: "numCardsInHandRadioGroup",
      numCardsInHandRadioGroupMutatorName: "setNumCardsInHandRadioGroup",
    };
  },
  components: {
    CustomRadioButton,
  },
  computed: mapState("LobbyConfig", [
    "scoreToWinRadioGroup",
    "numCardsInHandRadioGroup",
  ]),
};
</script>

<style>
</style>