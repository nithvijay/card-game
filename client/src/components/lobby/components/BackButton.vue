<template>
  <div class="flex">
    <button
      @click="returnToLogin"
      class="
        border-2 border-blue-800
        rounded-md
        shadow-md
        px-1
        transition
        duration-50
        hover:bg-gray-300
        active:bg-gray-400
      "
    >
      <i class="fas fa-chevron-left" /> Go Back
    </button>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState("General", ["pid", "room"]),
  },
  methods: {
    returnToLogin() {
      this.$socket.client.emit("returnToLogin", {
        pid: this.pid,
        room: this.room,
      });
    },
  },
};
</script>

<style>
</style>