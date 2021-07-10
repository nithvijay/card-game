<template>
  <div>
    <div class="flex flex-wrap items-start justify-center gap-1 p-2">
      <score-summary-stage-4 :summary="summary1" :name="name1" />
      <score-summary-stage-4 :summary="summary2" :name="name2" />
      <score-summary-stage-4 :summary="summary3" :name="name3" />
      <score-summary-stage-4 :summary="summary4" :name="name4" />
    </div>

    <div class="text-center">
      <button
        type="button"
        class="
          text-lg
          bg-blue-700
          hover:bg-blue-600
          transition
          duration:300
          rounded-xl
          text-gray-100
          py-2
          px-20
        "
      >
        Next
      </button>
    </div>
  </div>
</template>

<script>
import ScoreSummaryStage4 from "../components/ScoreSummaryStage4.vue";
export default {
  data: function () {
    return {
      name1: "novahoo",
      name2: "Chungus",
      name3: "op",
      name4: "mangos",
      name5: "sherlock",
      summary1: [
        {
          text: "Other",
          symbol: "+",
        },
        {
          text: "Something",
          symbol: "+",
        },
        {
          text: "Else",
          symbol: "-",
        },
      ],
      summary2: [
        {
          text: "Other",
          symbol: "+",
        },
        {
          text: "Something",
          symbol: "+",
        },
        {
          text: "Else",
          symbol: "-",
        },
        {
          text: "Something",
          symbol: "+",
        },
        {
          text: "Else",
          symbol: "-",
        },
      ],
      summary3: [
        {
          text: "Something",
          symbol: "+",
        },
        {
          text: "Else",
          symbol: "-",
        },
        {
          text: "Something",
          symbol: "+",
        },
        {
          text: "Else",
          symbol: "-",
        },
      ],
      summary4: [
        {
          text: "Other",
          symbol: "+",
        },
        {
          text: "Something",
          symbol: "+",
        },
        {
          text: "Else",
          symbol: "-",
        },
        {
          text: "Something",
          symbol: "+",
        },
        {
          text: "Else",
          symbol: "-",
        },
        {
          text: "Something",
          symbol: "+",
        },
        {
          text: "Else",
          symbol: "-",
        },
      ],
      summary5: [
        {
          text: "Something",
          symbol: "+",
        },
        {
          text: "Else",
          symbol: "-",
        },
      ],
    };
  },
  components: {
    ScoreSummaryStage4,
  },
};
</script>

<style>
</style>