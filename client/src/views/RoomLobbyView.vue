<template>
  <div class="container mx-auto max-w-sm p-5 flex flex-col gap-2">
    <user-status-tile />
    <game-config-tile />
    <ready-button-tile />
  </div>
</template>

<script>
import UserStatusTile from "../components/lobby/tiles/UserStatusTile.vue";
import GameConfigTile from "../components/lobby/tiles/GameConfigTile.vue";
import ReadyButtonTile from "../components/lobby/tiles/ReadyButtonTile.vue";

export default {
  components: {
    UserStatusTile,
    GameConfigTile,
    ReadyButtonTile,
  },
};
</script>

<style>
</style>