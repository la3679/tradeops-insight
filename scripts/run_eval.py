"""Run the replayable, zero-cost mock evaluation baseline."""

import json
from dataclasses import asdict

from tradeops.evaluation import run_mock_baseline

result = run_mock_baseline()
print(json.dumps(asdict(result), sort_keys=True))
if result.failed:
    raise SystemExit(1)
