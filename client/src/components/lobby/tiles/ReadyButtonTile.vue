<template>
  <div class="text-center">
    <button
      type="button"
      v-if="isUserReady"
      @click.prevent="clickedReady"
      class="
        text-lg
        w-32
        bg-green-100
        hover:bg-green-200
        transition
        duration:300
        text-green-900
        rounded-xl
        p-2
      "
    >
      Ready <i class="fas fa-check text-green-500" />
    </button>
    <button
      type="button"
      v-else
      @click.prevent="clickedReady"
      class="
        text-lg
        w-32
        bg-red-100
        hover:bg-red-200
        transition
        duration:300
        rounded-xl
        p-2
        text-red-900
      "
    >
      Not Ready <i class="fas fa-times text-red-500" />
    </button>
  </div>
</template>

<script>
import { mapState, mapGetters } from "vuex";

export default {
  methods: {
    clickedReady() {
      this.$socket.client.emit("changeReadyStatusRoomLobby", {
        pid: this.pid,
        room: this.room,
        isReady: !this.isUserReady,
      });
    },
  },
  computed: {
    ...mapState("General", ["pid", "room"]),
    ...mapState("RoomLobby", ["roomLobbyStatus"]),
    ...mapGetters("RoomLobby", ["someGetter"]),
    isUserReady() {
      if (this.someGetter) {
        // this should not be necessary
        return this.someGetter.filter((member) => member.pid === this.pid)[0]
          .isReady;
      } else {
        return false;
      }
    },
  },
};
</script>

<style>
</style>