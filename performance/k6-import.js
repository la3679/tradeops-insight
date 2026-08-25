import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 1,
  iterations: 10,
  thresholds: { http_req_failed: ["rate<0.01"], http_req_duration: ["p(95)<500"] },
};

const baseUrl = __ENV.BASE_URL || "http://host.docker.internal:8000";

export default function () {
  const response = http.post(`${baseUrl}/api/v1/imports/synthetic`, null, {
    headers: {
      "X-Demo-Role": "administrator",
      "Idempotency-Key": `k6-import-${__VU}-${__ITER}`,
    },
  });
  check(response, { "import accepted": (item) => item.status === 202 });
  sleep(0.6);
}
