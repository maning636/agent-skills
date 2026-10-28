#!/usr/bin/env bash
# Absurd skill: emit event to wake suspended tasks
set -e

EVENT=""
PAYLOAD="{}"
QUEUE="agent-tasks"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --event) EVENT="$2"; shift 2;;
    --payload) PAYLOAD="$2"; shift 2;;
    --queue) QUEUE="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 1;;
  esac
done

if [[ -z "$EVENT" ]]; then
  echo '{"error": "--event is required"}'
  exit 1
fi

ABSURD_DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/absurd_db" \
python << PYEOF
from absurd_sdk import Absurd
import json
queue_name = "${QUEUE}"
event = "${EVENT}"
payload_text = '''${PAYLOAD}'''
a = Absurd()
a.emit_event(event, json.loads(payload_text), queue_name=queue_name)
print(json.dumps({"emitted": event, "payload": json.loads(payload_text)}))
PYEOF