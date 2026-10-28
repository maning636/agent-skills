#!/usr/bin/env bash
# Absurd skill: fetch final task result
set -e

TASK_ID=""
QUEUE="agent-tasks"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --task-id) TASK_ID="$2"; shift 2;;
    --queue) QUEUE="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 1;;
  esac
done

if [[ -z "$TASK_ID" ]]; then
  echo '{"error": "--task-id is required"}'
  exit 1
fi

ABSURD_DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/absurd_db" \
python -c "
from absurd_sdk import Absurd
import json
a = Absurd()
snap = a.fetch_task_result('${TASK_ID}', queue_name='${QUEUE}')
if snap is None:
    print(json.dumps({'state': 'not_found'}))
else:
    print(json.dumps({
        'state': snap.state,
        'output': getattr(snap, 'output', None),
        'error': getattr(snap, 'error', None),
        'attempt': getattr(snap, 'attempt', None),
    }, indent=2, default=str))
"