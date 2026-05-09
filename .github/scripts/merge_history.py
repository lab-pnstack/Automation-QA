#!/usr/bin/env python3
import json
import os
from pathlib import Path

history_dir = Path("reports/history")
all_runs = []
seen_run_ids = set()

# Collect all individual run files
for json_file in sorted(history_dir.glob("*.json")):
    if json_file.name == "index.json":
        continue

    try:
        with open(json_file, 'r') as f:
            run_data = json.load(f)
            run_id = run_data.get('run_id')

            if run_id and run_id not in seen_run_ids:
                seen_run_ids.add(run_id)

                # Create summary entry
                summary = {
                    "run_id": run_id,
                    "date": run_data.get('date'),
                    "total": run_data.get('total', 0),
                    "passed": run_data.get('passed', 0),
                    "failed": run_data.get('failed', 0),
                    "warning": run_data.get('warning', 0),
                    "error": run_data.get('error', 0),
                    "skipped": run_data.get('skipped', 0),
                    "duration": run_data.get('duration', 0),
                    "pass_rate": run_data.get('pass_rate', 0),
                    "file": f"reports/history/{run_id}.json"
                }
                all_runs.append(summary)
    except Exception as e:
        print(f"Error processing {json_file}: {e}")

# Sort by date (newest first)
all_runs.sort(key=lambda x: x.get('date', ''), reverse=True)

# Write merged index
os.makedirs('_site/api', exist_ok=True)
with open('_site/api/runs.json', 'w') as f:
    json.dump(all_runs, f, indent=2)

print(f"Merged {len(all_runs)} test runs")
