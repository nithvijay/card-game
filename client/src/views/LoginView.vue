<template>
  <div class="flex flex-col max-w-lg mx-auto">
    <div class="text-center mt-5">
      <p class="text-xl">Welcome to The Inspector Game!</p>
    </div>

    <div class="container mx-auto max-w-sm p-5">
      <form class="flex flex-col">
        <label class="font-bold text-gray-500"> Username </label>
        <input
          class="
            bg-gray-100
            appearance-none
            border-2
            rounded
            py-2
            px-4
            text-gray-700
            focus:outline-none
            transition
            duration-300
            focus:bg-white
          "
          :class="{
            'border-gray-100 focus:border-blue-800': isUsernameValid,
            'border-red-500 focus:border-red-500': !isUsernameValid,
          }"
          type="text"
          v-model="usernameModel"
        />

        <transition name="fade" mode="out-in">
          <div class="text-red-700" v-if="!isUsernameValid" key="1">
            <i class="fas fa-exclamation-circle" />
            {{ usernameValidMessage }}
          </div>
          <div v-else key="2">&nbsp;</div>
        </transition>

        <label class="font-bold text-gray-500"> Room </label>
        <input
          class="
            bg-gray-100
            appearance-none
            border-2
            rounded
            py-2
            px-4
            text-gray-700
            focus:outline-none
            transition
            duration-300
            focus:bg-white
          "
          :class="{
            'border-gray-100 focus:border-blue-800': isRoomValid,
            'border-red-500 focus:border-red-500': !isRoomValid,
          }"
          type="text"
          v-model="roomModel"
        />

        <transition name="fade" mode="out-in">
          <div class="text-red-700" v-if="!isRoomValid" key="1">
            <i class="fas fa-exclamation-circle" />
            {{ roomValidMessage }}
          </div>
          <div v-else key="2">&nbsp;</div>
        </transition>
        <button
          class="
            shadow
            transition
            hover:ease-in-out
            duration-100
            bg-blue-800
            hover:bg-blue-700
            focus:outline-none
            active:bg-blue-300
            text-white
            font-bold
            py-2
            px-4
            rounded
          "
          @click.prevent="submitLoginInfo"
          type="submit"
        >
          Submit
        </button>
      </form>
    </div>
    <div class="border-blue-800 border-2 rounded-md bg-white flex max-w-lg">
      <a
        target="_blank"
        href="https://github.com/nithvijay/card-game/blob/main/Instructions.md"
        class="
          text-lg text-center
          flex-1
          no-underline
          hover:underline
          border-2
          rounded-md
          p-2
          hover:bg-blue-100
        "
      >
        Instructions
      </a>

      <a
        target="_blank"
        href="https://docs.google.com/forms/d/e/1FAIpQLSf0cF0S9Ms6Iqo1WFn7ayU-7D83Ce7ArGNkapf0-BpI-JK3fw/viewform?usp=sf_link"
        class="
          text-lg text-center
          flex-1
          no-underline
          hover:underline
          border-2
          rounded-md
          p-2
          hover:bg-blue-100
        "
      >
        Feedback
      </a>

      <a
        target="_blank"
        href="https://github.com/nithvijay/card-game"
        class="
          text-lg text-center
          flex-1
          no-underline
          hover:underline
          border-2
          p-2
          hover:bg-blue-100
        "
      >
        Source Code
      </a>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  data() {
    return {
      isUsernameValid: true,
      usernameValidMessage: "",
      isRoomValid: true,
      roomValidMessage: "",
    };
  },
  computed: {
    ...mapState("General", ["username", "room", "pid"]),
    usernameModel: {
      get() {
        return this.$store.state["General"].username;
      },
      set(value) {
        if (value.length > 14) {
          this.isUsernameValid = false;
          this.usernameValidMessage =
            "username must be fewer than 15 characters";
        } else {
          this.isUsernameValid = true;
        }
        return this.$store.commit("General/setUsername", value);
      },
    },
    roomModel: {
      get() {
        return this.$store.state["General"].room;
      },
      set(value) {
        if (value.length > 14) {
          this.isRoomValid = false;
          this.roomValidMessage = "room must be fewer than 15 characters";
        } else {
          this.isRoomValid = true;
        }
        return this.$store.commit("General/setRoom", value.toUpperCase());
      },
    },
  },
  sockets: {
    errorLoggingIn(data) {
      switch (data["type"]) {
        case "username":
          this.isUsernameValid = false;
          this.usernameValidMessage = data["errorMessage"];
          break;
        case "room":
          this.isRoomValid = false;
          this.roomValidMessage = data["errorMessage"];
          break;
      }
    },
  },
  methods: {
    submitLoginInfo() {
      localStorage.setItem("username", this.username);
      localStorage.setItem("room", this.room);
      if (
        (15 > this.username.length) &
        (this.username.length > 0) &
        (15 > this.room.length) &
        (this.room.length > 0)
      ) {
        this.$socket.client.emit("submitLoginInfo", {
          username: this.username,
          room: this.room,
          pid: this.pid,
        });
      } else if (this.room.length === 0) {
        this.isRoomValid = false;
        this.roomValidMessage = "Room code cannot be empty";
      } else if (this.username.length === 0) {
        this.isUsernameValid = false;
        this.usernameValidMessage = "Username cannot be empty";
      }
    },
  },
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.05s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>