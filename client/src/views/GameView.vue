<template>
  <div class="container max-w-sm mx-auto flex flex-col gap-2">
    <div class="h-4 bg-blue-400"></div>
    <turn-tile />
    <!-- <button @click.prevent="changeStage">
      Change Stage. Current Stage: {{ stage }}
    </button> -->
    <transition name="component-fade" mode="out-in">
      <component :is="view" />
    </transition>
  </div>
</template>

<script>
import TurnTile from "../components/game/tiles/TurnTile.vue";
import Stage1Tile from "../components/game/tiles/Stage1Tile.vue";
import Stage2Tile from "../components/game/tiles/Stage2Tile.vue";
import Stage3Tile from "../components/game/tiles/Stage3Tile.vue";
import Stage4Tile from "../components/game/tiles/Stage4Tile.vue";

import { mapState } from "vuex";

export default {
  name: "GameView",
  data: function () {
    return {
      // stage: 1,
      // view: "stage-1-tile",
    };
  },
  components: {
    TurnTile,
    Stage1Tile,
    Stage2Tile,
    Stage3Tile,
    Stage4Tile,
  },
  methods: {
    changeStage() {
      // this.stage = (this.stage % 4) + 1;
      // this.view = `stage-${this.stage}-tile`;
    },
  },
  computed: {
    ...mapState("GeneralGame", ["generalGameData"]),
    view() {
      if (this.generalGameData.stage) {
        return `stage-${this.generalGameData.stage}-tile`;
      } else {
        return "stage-1-tile";
      }
    },
  },
};
</script>

<style scoped>
.component-fade-enter-active,
.component-fade-leave-active {
  transition: opacity 0.3s ease;
}
.component-fade-enter, .component-fade-leave-to
/* .component-fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>