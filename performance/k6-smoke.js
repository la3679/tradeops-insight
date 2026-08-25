import http from "k6/http";
import { check } from "k6";
import { sleep } from "k6";

export const options = {
  scenarios: {
    representative: {
      executor: "constant-vus",
      vus: 1,
      duration: "30s",
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<500"],
  },
};

const baseUrl = __ENV.BASE_URL || "http://host.docker.internal:8000";

export default function () {
  const responses = http.batch([
    ["GET", `${baseUrl}/api/v1/health/ready`],
    ["GET", `${baseUrl}/api/v1/exceptions`, null, { headers: { "X-Demo-Role": "analyst" } }],
    [
      "GET",
      `${baseUrl}/api/v1/trades?cursor=0&limit=25`,
      null,
      { headers: { "X-Demo-Role": "analyst" } },
    ],
    ["GET", `${baseUrl}/api/v1/dashboard/summary`, null, { headers: { "X-Demo-Role": "analyst" } }],
  ]);
  check(responses, {
    "all representative requests succeeded": (items) => items.every((item) => item.status === 200),
  });
  sleep(2.2);
}
