<template>
  <div class="container mx-auto max-w-sm p-5">
    <form class="flex flex-col">
      <label class="font-bold text-gray-500"> Username </label>
      <input
        class="
          bg-gray-100
          appearance-none
          border-2 border-gray-100
          rounded
          mb-4
          py-2
          px-4
          text-gray-700
          focus:outline-none
          transition
          duration-300
          focus:bg-white
          focus:border-blue-800
        "
        type="text"
        placeholder="Ex: Jane Doe"
      />
      <label class="font-bold text-gray-500"> Room </label>
      <input
        class="
          bg-gray-100
          appearance-none
          border-2 border-gray-100
          rounded
          mb-4
          py-2
          px-4
          text-gray-700
          focus:outline-none
          transition
          duration-300
          focus:bg-white
          focus:border-blue-800
        "
        type="text"
        placeholder="Ex: ASDF"
      />
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
        type="button"
      >
        Enter Room
      </button>
    </form>
  </div>
</template>

<script>
export default {
  sockets: {
    connect() {
      console.log("socket connected");
    },
    customEmit(val) {
      console.log(val);
    },
  },
};
</script>

<style>
</style>