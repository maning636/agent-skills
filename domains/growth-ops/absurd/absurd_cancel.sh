#!/usr/bin/env bash
# Absurd skill: cancel a task
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
a = Absurd()
a.cancel_task('${TASK_ID}', queue_name='${QUEUE}')
print('{\"cancelled\": \"${TASK_ID}\"}')
"