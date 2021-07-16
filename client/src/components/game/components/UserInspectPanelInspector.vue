<template>
  <div
    class="
      flex flex-col
      p-2
      bg-green-600
      rounded-md
      shadow-md
      items-center
      w-3/4
      gap-1
    "
  >
    <div class="flex justify-between gap-1">
      <button
        @click="inspectBag('inspected')"
        class="
          px-2
          rounded-md
          shadow-md
          transition
          duration-100
          bg-green-200
          hover:bg-green-300
        "
      >
        Inspect
      </button>
      <button
        @click="inspectBag('let go')"
        class="
          px-2
          rounded-md
          shadow-md
          transition
          duration-100
          bg-green-200
          hover:bg-green-300
        "
      >
        Let Go
      </button>
    </div>

    <user-num-cards-stage-2 :name="name" :numCards="numCards" />
  </div>
</template>

<script>
import { mapState } from "vuex";
import UserNumCardsStage2 from "./UserNumCardsStage2.vue";
export default {
  props: {
    name: String,
    numCards: Number,
    cards: Array,
    pid: String,
  },
  methods: {
    inspectBag(option) {
      console.log("test");
      this.$socket.client.emit("stage3MakeDecision", {
        pid: this.pid,
        option: option,
        room: this.room,
      });
    },
  },
  computed: {
    ...mapState("General", ["room"]),
  },
  components: {
    UserNumCardsStage2,
  },
};
</script>


<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>