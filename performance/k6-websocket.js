import ws from "k6/ws";
import { check } from "k6";

export const options = {
  scenarios: {
    fanout: { executor: "per-vu-iterations", vus: 5, iterations: 1, maxDuration: "10s" },
  },
  thresholds: { checks: ["rate==1"] },
};

const baseUrl = __ENV.WS_URL || "ws://host.docker.internal:8000";

export default function () {
  const response = ws.connect(`${baseUrl}/api/v1/events/ws?role=analyst`, {}, (socket) => {
    socket.on("message", (message) => {
      const payload = JSON.parse(message);
      check(payload, { "snapshot received": (item) => item.type === "queue.snapshot.v1" });
      socket.close();
    });
    socket.setTimeout(() => socket.close(), 5_000);
  });
  check(response, { "websocket upgraded": (item) => item && item.status === 101 });
}
