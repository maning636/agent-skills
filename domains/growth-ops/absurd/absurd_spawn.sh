#!/usr/bin/env bash
# Absurd skill: spawn a new task
set -e

TASK_NAME=""
PARAMS="{}"
QUEUE="agent-tasks"
MAX_ATTEMPTS=3

while [[ $# -gt 0 ]]; do
  case "$1" in
    --task-name) TASK_NAME="$2"; shift 2;;
    --params) PARAMS="$2"; shift 2;;
    --queue) QUEUE="$2"; shift 2;;
    --max-attempts) MAX_ATTEMPTS="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 1;;
  esac
done

if [[ -z "$TASK_NAME" ]]; then
  echo '{"error": "--task-name is required"}'
  exit 1
fi

ABSURD_DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/absurd_db" \
python -c "
from absurd_sdk import Absurd
import json, sys
a = Absurd(queue_name='${QUEUE}')
res = a.spawn('${TASK_NAME}', json.loads('''${PARAMS}'''), queue='${QUEUE}', max_attempts=${MAX_ATTEMPTS})
print(json.dumps({'task_id': str(res['task_id']), 'run_id': str(res['run_id']), 'attempt': res['attempt'], 'status': 'spawned'}))
"