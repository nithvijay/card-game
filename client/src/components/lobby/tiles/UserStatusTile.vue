<template>
  <div class="flex flex-col bg-blue-900 text-gray-100 p-3 rounded-md shadow-lg">
    <individual-user-status :name="name1" :isReady="isReady1" />
    <individual-user-status :name="name2" :isReady="isReady2" />
    <individual-user-status :name="name3" :isReady="isReady3" />
    <individual-user-status :name="name4" :isReady="isReady4" />
    <individual-user-status :name="name5" :isReady="isReady5" />
  </div>
</template>

<script>
import IndividualUserStatus from "../components/IndividualUserStatus.vue";

export default {
  name: "UserStatusTile",
  data: function () {
    return {
      name1: "novahoo",
      name2: "chungus",
      name3: "op",
      name4: "mangos",
      name5: "sherlock",
      isReady1: false,
      isReady2: true,
      isReady3: true,
      isReady4: false,
      isReady5: false,
    };
  },
  components: {
    IndividualUserStatus,
  },
};
</script>

<style>
</style>