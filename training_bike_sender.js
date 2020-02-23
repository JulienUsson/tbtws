const WebSocket = require("ws");
const redis = require("redis");

const subscriber = redis.createClient();
const publisher = redis.createClient();

const wss = new WebSocket.Server({ port: 9000 });

wss.on("connection", ws => {
  console.log("Sender: connection");
  ws.on("message", message => {
    if (message === "reset") {
      console.log("Sender: resetting...");
      publisher.publish("bike_reset", "true");
    }
  });
});

subscriber.on("message", (channel, message) => {
  if (channel === "bike_stat") {
    console.log(`Sender: sending ${message}`);
    wss.clients.forEach(ws => {
      ws.send(message);
    });
  }
});

subscriber.subscribe("bike_stat");

console.log("Sender: Started on port 9000");
