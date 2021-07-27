<template>
  <div class="flex flex-col bg-blue-900 text-gray-100 p-3 rounded-md shadow-lg">
    <individual-user-status
      v-for="member in roomLobbyStatus['members']"
      :key="member.pid"
      :name="member.username"
      :isReady="member.isReady"
    />
    <div v-if="numUsersNeeded > 0" class="flex justify-center pt-2">
      <div class="border-2 border-gray-100 text-center rounded-md px-2">
        {{ numUsersNeeded }} more {{ userSingular }} needed
      </div>
    </div>
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
    numUsersNeeded() {
      const numberLeft = 3 - parseInt(this.roomLobbyStatus.members.length);
      return numberLeft < 0 ? 0 : numberLeft;
    },
    userSingular() {
      return this.numUsersNeeded > 1 ? "users" : "user";
    },
  },
};
</script>

<style>
</style>