#!/usr/bin/env bash
# Absurd skill: retry a failed task
set -e

TASK_ID=""
QUEUE="agent-tasks"
SPAWN_NEW="False"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --task-id) TASK_ID="$2"; shift 2;;
    --queue) QUEUE="$2"; shift 2;;
    --spawn-new) SPAWN_NEW="True"; shift;;
    *) echo "unknown arg: $1" >&2; exit 1;;
  esac
done

if [[ -z "$TASK_ID" ]]; then
  echo '{"error": "--task-id is required"}'
  exit 1
fi

ABSURD_DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/absurd_db" \
python << PYEOF
from absurd_sdk import Absurd
import json
queue_name = "${QUEUE}"
task_id = "${TASK_ID}"
spawn_new = ${SPAWN_NEW}
a = Absurd()
res = a.retry_task(task_id, spawn_new=spawn_new, queue_name=queue_name)
print(json.dumps({"retried": task_id, "result": str(res)}, indent=2))
PYEOF