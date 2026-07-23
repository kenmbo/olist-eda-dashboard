#!/usr/bin/env bash
set -u -o pipefail

source_root="/home/kebo/python/olist-migration/olist-eda-dashboard"
capture_dir="${1:-$(mktemp -d /tmp/olist-fastapi-baseline.XXXXXX)}"
base_url="http://127.0.0.1:8000"

mkdir -p "$capture_dir"
printf 'endpoint\tpath\thttp_status\tcontent_type\tbody_bytes\tcurl_result\n' > "$capture_dir/requests.tsv"

cd "$source_root"

PYTHONDONTWRITEBYTECODE=1 "$source_root/.venv/bin/python" -B -m uvicorn src.main:app \
  --host 127.0.0.1 --port 8000 --log-level warning > "$capture_dir/server.log" 2>&1 &
server_pid=$!

cleanup() {
  kill "$server_pid" 2>/dev/null || true
  wait "$server_pid" 2>/dev/null || true
}
trap cleanup EXIT

ready=0
for attempt in $(seq 1 120); do
  if curl --silent --show-error --fail --max-time 2 "$base_url/openapi.json" > /dev/null; then
    ready=1
    break
  fi
  sleep 0.25
done

if [ "$ready" -ne 1 ]; then
  printf 'FastAPI did not become ready; inspect %s/server.log\n' "$capture_dir" >&2
  exit 1
fi

endpoints=(
  'orders-daily:/api/orders/daily'
  'orders-costs:/api/orders/costs'
  'categories-sales:/api/categories/sales'
  'sellers-performance:/api/sellers/performance'
  'sellers-distribution:/api/sellers/distribution'
  'shipping-stages-by-city:/api/shipping/stages-by-city'
  'customers-clv-map:/api/customers/clv-map'
  'sellers-review-sales:/api/sellers/review-sales'
  'leads-conversion:/api/leads/conversion'
  'leads-origin:/api/leads/origin'
  'reviews-distribution:/api/reviews/distribution'
  'delivery-stages:/api/delivery/stages'
  'orders-hourly:/api/orders/hourly'
  'sales-monthly:/api/sales/monthly'
  'categories-monthly-sales:/api/categories/monthly-sales'
  'sellers-shipping-times:/api/sellers/shipping-times'
  'categories-weights:/api/categories/weights'
)

for endpoint in "${endpoints[@]}"; do
  name="${endpoint%%:*}"
  path="${endpoint#*:}"
  headers="$capture_dir/$name.headers"
  body="$capture_dir/$name.json"
  curl_result=ok
  if ! status=$(curl --silent --show-error --max-time 180 --dump-header "$headers" --output "$body" --write-out '%{http_code}' "$base_url$path"); then
    curl_result=curl-error
  fi
  content_type=$(awk 'BEGIN { IGNORECASE = 1 } /^content-type:/ { sub(/^[^:]*:[[:space:]]*/, ""); sub(/[\r\n].*$/, ""); print; exit }' "$headers")
  body_bytes=$(wc -c < "$body")
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$path" "$status" "$content_type" "$body_bytes" "$curl_result" >> "$capture_dir/requests.tsv"
done

printf '%s\n' "$capture_dir"
