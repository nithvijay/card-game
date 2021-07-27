<template>
  <div class="flex flex-wrap justify-center gap-1 mt-2">
    <user-label
      v-for="(username, index) in usernames"
      :key="index"
      :isInspector="index === inspectorIndex"
      :name="username"
      :state="isReady[index]"
      :score="scores[index]"
    />
  </div>
</template>

<script>
import UserLabel from "../components/UserLabel.vue";
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState("GeneralGame", ["generalGameData", "isReady"]),
    usernames() {
      return this.generalGameData.usernames;
    },
    inspectorIndex() {
      return this.generalGameData.inspectorIndex;
    },
    scores() {
      return this.generalGameData.scores;
    },
  },
  components: {
    UserLabel,
  },
};
</script>

<style>
</style>