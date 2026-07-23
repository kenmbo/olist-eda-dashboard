#!/usr/bin/env bash
set -u
capture_dir=$(mktemp -d /tmp/olist-fastapi-debug.XXXXXX)
cd /home/kebo/python/olist-migration/olist-eda-dashboard || exit 1
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m uvicorn src.main:app --host 127.0.0.1 --port 8002 --log-level info > "$capture_dir/server.log" 2>&1 &
server_pid=$!
sleep 3
printf 'capture=%s\npid=%s\n' "$capture_dir" "$server_pid"
ps -o pid,ppid,stat,cmd -p "$server_pid"
curl --verbose --max-time 3 http://127.0.0.1:8002/openapi.json > "$capture_dir/openapi.json"
curl_exit=$?
printf 'curl_exit=%s\n' "$curl_exit"
sed -n '1,160p' "$capture_dir/server.log"
kill "$server_pid" 2>/dev/null
wait "$server_pid" 2>/dev/null
exit "$curl_exit"

