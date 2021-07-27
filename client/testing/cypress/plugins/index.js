/// <reference types="cypress" />

// Socket.io client to allow Cypress itself
// to communicate with a central "checkpoint" server
// https://socket.io/docs/v4/client-initialization/
const io = require("socket.io-client");

module.exports = (on, config) => {
  // this socket will be used to sync Cypress instance
  // to another Cypress instance. We can create it right away
  const cySocket = io("http://localhost:9090");

  // receiving the checkpoint name reached by any test runner
  let checkpointName;
  cySocket.on("checkpoint", (name) => {
    console.log("current checkpoint %s", name);
    checkpointName = name;
  });

  on("task", {
    // tasks for syncing multiple Cypress instances together
    checkpoint(name) {
      console.log('emitting checkpoint name "%s"', name);
      cySocket.emit("checkpoint", name);

      return null;
    },

    waitForCheckpoint(name) {
      console.log('waiting for checkpoint "%s"', name);

      // TODO: set maximum waiting time
      return new Promise((resolve) => {
        const i = setInterval(() => {
          console.log('checking, current checkpoint "%s"', checkpointName);
          if (checkpointName === name) {
            console.log('reached checkpoint "%s"', name);
            clearInterval(i);
            resolve(name);
          }
        }, 1000);
      });
    },
  });
};
