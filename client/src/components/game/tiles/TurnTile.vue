<template>
  <div class="flex flex-wrap justify-center gap-1">
    <user-label :isSherriff="isSherriff1" :name="name1" />
    <user-label :isSherriff="isSherriff2" :name="name2" />
    <user-label :isSherriff="isSherriff3" :name="name3" />
    <user-label :isSherriff="isSherriff4" :name="name4" />
    <user-label :isSherriff="isSherriff5" :name="name5" />
  </div>
</template>

<script>
import UserLabel from "../components/UserLabel.vue";

export default {
  data: function () {
    return {
      name1: "novahoo",
      name2: "Chungus",
      name3: "op",
      name4: "mangos",
      name5: "sherlock",
      isSherriff1: false,
      isSherriff2: false,
      isSherriff3: true,
      isSherriff4: false,
      isSherriff5: false,
    };
  },
  components: {
    UserLabel,
  },
};
</script>

<style>
</style>