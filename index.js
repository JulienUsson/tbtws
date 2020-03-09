require("dotenv").config();
const spawn = require("child_process").spawn;
const WebSocket = require("ws");

const wss = new WebSocket.Server({ port: process.env.PORT || 9000 });

trainingBikeListener = spawn("python3", [
  "training_bike_listener.py",
  "-i",
  process.env.INPUT_DEVICE || "0"
]);
trainingBikeListener.stdout.on("data", function(data) {
  const { speed } = JSON.parse(data);
  console.log({ speed });
  wss.clients.forEach(ws => {
    ws.send({ speed });
  });
});

wss.on("connection", ws => {
  console.log("Connected");

  ws.on("close", () => {
    console.log("Disconnected");
  });
});

console.log("Started on port 9000");
