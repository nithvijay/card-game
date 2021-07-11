<template>
  <div class="flex flex-col bg-blue-900 text-gray-100 p-3 rounded-md shadow-lg">
    <individual-user-status
      v-for="member in roomLobbyStatus['members']"
      :key="member.pid"
      :name="member.username"
      :isReady="member.isReady"
    />
  </div>
</template>

<script>
import { mapState } from "vuex";
import IndividualUserStatus from "../components/IndividualUserStatus.vue";

export default {
  name: "UserStatusTile",
  components: {
    IndividualUserStatus,
  },
  computed: {
    ...mapState("RoomLobby", ["roomLobbyStatus"]),
  },
};
</script>

<style>
</style>