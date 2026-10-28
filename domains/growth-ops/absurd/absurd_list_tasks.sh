#!/usr/bin/env bash
# Absurd skill: list pending/running tasks
set -e

QUEUE="default"
LIMIT=10

while [[ $# -gt 0 ]]; do
  case "$1" in
    --queue) QUEUE="$2"; shift 2;;
    --limit) LIMIT="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 1;;
  esac
done

ABSURD_DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/absurd_db" \
python << PYEOF
from absurd_sdk import Absurd
import json
import psycopg
conn = psycopg.connect("postgresql://postgres:postgres@127.0.0.1:5432/absurd_db", autocommit=True)
queue_name = "${QUEUE}"
limit = ${LIMIT}
with conn.cursor() as cur:
    cur.execute(
        'SELECT task_id, task_name, state, attempts, max_attempts, params, enqueue_at FROM absurd."t_' + queue_name + '" ORDER BY enqueue_at DESC LIMIT %s',
        (limit,),
    )
    rows = cur.fetchall()
print(json.dumps([{
    "task_id": str(r[0]), "task_name": r[1], "state": r[2],
    "attempts": r[3], "max_attempts": r[4], "params": r[5], "enqueued_at": r[6].isoformat()
} for r in rows], indent=2, default=str))
PYEOF

