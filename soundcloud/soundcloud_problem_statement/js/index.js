const net = require("net");
const readline = require("readline");

const EVENT_PORT = 9090;
const CLIENT_PORT = 9099;

const clientPool = {};
const followRegistry = {};

let lastSeqNo = 0;

net
  .createServer(socket => {
    const seqNoToMessage = {};
    const readInterface = readline.createInterface({ input: socket });
    readInterface.on("line", payload => {
      console.log(`Message received: ${payload}`);

      const payloadParts = payload.split("|");
      seqNoToMessage[parseInt(payloadParts[0])] = payloadParts;

      while (seqNoToMessage[lastSeqNo + 1]) {
        const nextMessage = seqNoToMessage[lastSeqNo + 1];
        const nextPayload = nextMessage.join("|");

        const seqNo = parseInt(nextMessage[0]);
        const kind = nextMessage[1];

        switch (kind) {
          case "F":
            {
              const fromUserId = parseInt(nextMessage[2]);
              const toUserId = parseInt(nextMessage[3]);

              const followers = followRegistry[toUserId] || new Set([]);
              followers.add(fromUserId);
              followRegistry[toUserId] = followers;

              const socket = clientPool[toUserId];
              if (socket) {
                socket.write(nextPayload + "\n");
              }
            }
            break;

          case "U":
            {
              const fromUserId = parseInt(nextMessage[2]);
              const toUserId = parseInt(nextMessage[3]);

              const followers = followRegistry[toUserId] || new Set([]);
              followers.delete(fromUserId);
              followRegistry[toUserId] = followers;
            }
            break;

          case "P":
            {
              const toUserId = parseInt(nextMessage[3]);

              const socket = clientPool[toUserId];
              if (socket) {
                socket.write(nextPayload + "\n");
              }
            }
            break;

          case "B":
            {
              for (let toUserId in clientPool) {
                const socket = clientPool[toUserId];
                if (socket) {
                  socket.write(nextPayload + "\n");
                }
              }
            }
            break;

          case "S":
            {
              const fromUserId = parseInt(nextMessage[2]);

              const followers = followRegistry[fromUserId] || new Set([]);

              followers.forEach(follower => {
                const socket = clientPool[follower];
                if (socket) {
                  socket.write(nextPayload + "\n");
                }
              });
            }
            break;
        }

        lastSeqNo = seqNo;
      }
    });
  })
  .listen(EVENT_PORT, "127.0.0.1", err => {
    if (err) {
      throw err;
    }
    console.log(`Listening for events on ${EVENT_PORT}`);
  });

net
  .createServer(clientSocket => {
    const readInterface = readline.createInterface({ input: clientSocket });
    readInterface.on("line", userIdString => {
      if (userIdString != null) {
        clientPool[parseInt(userIdString)] = clientSocket;

        console.log(
          `User connected: ${userIdString} (${clientPool.length} total)`
        );
      }
    });
  })
  .listen(CLIENT_PORT, "127.0.0.1", err => {
    if (err) {
      throw err;
    }
    console.log(`Listening for client requests on ${CLIENT_PORT}`);
  });
