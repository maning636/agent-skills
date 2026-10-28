#!/usr/bin/env bash
# Absurd skill: connection / queue diagnostics (v2 — honest health)
#
# Reports real schema readiness, not just metadata presence.
# Returns status=ok only when ALL queues have t_* and e_* tables.
# Returns status=degraded if any queue is missing task/event tables.

set -e

DB_URL="postgresql://postgres:postgres@127.0.0.1:5432/absurd_db"

ABSURD_DATABASE_URL="$DB_URL" \
python << PYEOF
import json, sys
sys.path.insert(0, 'E:/Python/Lib/site-packages')
import psycopg
from absurd_sdk import Absurd

DB_URL = "postgresql://postgres:postgres@127.0.0.1:5432/absurd_db"

try:
    absurd = Absurd(conn_or_url=DB_URL)
    queues = absurd.list_queues()
except Exception as e:
    print(json.dumps({"status": "error", "error": f"connect failed: {e}"}, ensure_ascii=False, indent=2))
    sys.exit(1)

result = {
    "status": "ok",
    "database_url_set": bool("${ABSURD_DATABASE_URL:-}"),
    "queue_count": len(queues),
    "queues": [{"name": q} for q in queues],
    "task_table_ready": False,
    "event_table_ready": False,
    "task_tables_present": "0/0",
    "event_tables_present": "0/0",
}

task_ok = 0
event_ok = 0
try:
    conn = psycopg.connect(DB_URL)
    with conn.cursor() as cur:
        for q in queues:
            cur.execute("SELECT to_regclass(%s);", (f"absurd.t_{q}",))
            if cur.fetchone()[0] is not None:
                task_ok += 1
            cur.execute("SELECT to_regclass(%s);", (f"absurd.e_{q}",))
            if cur.fetchone()[0] is not None:
                event_ok += 1
    conn.close()
except Exception as e:
    result["status"] = "error"
    result["error"] = f"schema probe failed: {e}"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(1)

result["task_tables_present"] = f"{task_ok}/{len(queues)}"
result["event_tables_present"] = f"{event_ok}/{len(queues)}"
result["task_table_ready"] = (task_ok == len(queues))
result["event_table_ready"] = (event_ok == len(queues))

if not (result["task_table_ready"] and result["event_table_ready"]):
    result["status"] = "degraded"
    result["diagnosis"] = "some queues missing t_* or e_* tables; run absurd_create_queue on them"

absurd.close()
print(json.dumps(result, ensure_ascii=False, indent=2))
PYEOF