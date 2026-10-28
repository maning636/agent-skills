#!/usr/bin/env bash
# Absurd skill: list all queues
set -e

ABSURD_DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/absurd_db" \
python -c "
from absurd_sdk import Absurd
import json
a = Absurd()
print(json.dumps([{'name': q} for q in a.list_queues()], indent=2))
"
