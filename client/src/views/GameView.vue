<template>
  <div class="flex flex-col max-w-3xl mx-auto gap-2 items-center">
    <turn-tile />
    <div>Stage: {{ this.generalGameData.stage }}</div>
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
import Stage5Tile from "../components/game/tiles/Stage5Tile.vue";

import { mapState } from "vuex";

export default {
  name: "GameView",
  components: {
    TurnTile,
    Stage1Tile,
    Stage2Tile,
    Stage3Tile,
    Stage4Tile,
    Stage5Tile,
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
.component-fade-enter-active {
  transition: opacity 0.3s ease;
}
.component-fade-leave-active {
  transition: opacity 0.3s ease;
  transition-delay: 0.3s;
}
.component-fade-enter,
.component-fade-leave-to {
  opacity: 0;
}
</style>