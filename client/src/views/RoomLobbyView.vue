<template>
  <div class="container mx-auto max-w-sm p-5 flex flex-col gap-2">
    <back-button />
    <user-status-tile />
    <game-config-tile />
    <ready-button-tile />
  </div>
</template>

<script>
import UserStatusTile from "../components/lobby/tiles/UserStatusTile.vue";
import GameConfigTile from "../components/lobby/tiles/GameConfigTile.vue";
import ReadyButtonTile from "../components/lobby/tiles/ReadyButtonTile.vue";
import BackButton from "../components/lobby/components/BackButton.vue";

export default {
  components: {
    UserStatusTile,
    GameConfigTile,
    ReadyButtonTile,
    BackButton,
  },
};
</script>

<style>
</style>