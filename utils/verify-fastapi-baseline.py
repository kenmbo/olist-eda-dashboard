#!/usr/bin/env python3
import csv
import hashlib
import json
from pathlib import Path


CAPTURE = Path("/tmp/olist-fastapi-baseline.SjAhAW")
REPEAT = Path("/tmp/olist-fastapi-baseline.XAqbY2")
FIXTURES = Path("src/test/resources/contracts/fastapi")

FULL = {
    "categories-monthly-sales",
    "categories-sales",
    "delivery-stages",
    "leads-conversion",
    "leads-origin",
    "orders-hourly",
    "reviews-distribution",
    "sales-monthly",
    "sellers-distribution",
    "shipping-stages-by-city",
}


def no_null_or_nonfinite(value):
    if value is None:
        return False
    if isinstance(value, float):
        return value == value and value not in (float("inf"), float("-inf"))
    if isinstance(value, list):
        return all(no_null_or_nonfinite(item) for item in value)
    if isinstance(value, dict):
        return all(no_null_or_nonfinite(item) for item in value.values())
    return True


def compact(values):
    return values if len(values) <= 6 else values[:3] + values[-3:]


with (CAPTURE / "requests.tsv").open(newline="") as source:
    requests = list(csv.DictReader(source, delimiter="\t"))

assert len(requests) == 17
assert all(row["http_status"] == "200" for row in requests)
assert all(row["content_type"] == "application/json" for row in requests)
assert all(row["curl_result"] == "ok" for row in requests)

names = {row["endpoint"] for row in requests}
fixture_paths = sorted(FIXTURES.glob("*.json"))
assert {path.stem for path in fixture_paths} == names

for row in requests:
    name = row["endpoint"]
    source_path = CAPTURE / f"{name}.json"
    repeat_path = REPEAT / f"{name}.json"
    source_bytes = source_path.read_bytes()
    assert source_bytes == repeat_path.read_bytes(), name
    source_payload = json.loads(source_bytes)
    fixture_payload = json.loads((FIXTURES / f"{name}.json").read_text(encoding="utf-8"))
    assert no_null_or_nonfinite(source_payload), name
    assert list(fixture_payload) == list(source_payload), name
    if name in FULL:
        assert fixture_payload == source_payload, name
    else:
        assert all(fixture_payload[key] == compact(value) for key, value in source_payload.items()), name
    assert int(row["body_bytes"]) == len(source_bytes), name
    assert hashlib.sha256(source_bytes).hexdigest(), name

hourly = json.loads((CAPTURE / "orders-hourly.json").read_text())
assert hourly["index"] == ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
assert hourly["columns"] == [str(hour) for hour in range(24)]
assert len(hourly["data"]) == 7 and all(len(row) == 24 for row in hourly["data"])

monthly = json.loads((CAPTURE / "sales-monthly.json").read_text())
assert monthly["year_month"][0] == "2017-01-01T00:00:00"
assert monthly["year_month"][-1] == "2018-08-01T00:00:00"

category_monthly = json.loads((CAPTURE / "categories-monthly-sales.json").read_text())
assert category_monthly["columns"] == ["beleza_saude", "cama_mesa_banho", "esporte_lazer", "informatica_acessorios", "relogios_presentes"]
assert len(category_monthly["index"]) == 22
assert len(category_monthly["data"]) == 22 and all(len(row) == 5 for row in category_monthly["data"])

weights = json.loads((CAPTURE / "categories-weights.json").read_text())
assert list(weights) == ["cama_mesa_banho", "beleza_saude", "esporte_lazer", "moveis_decoracao", "informatica_acessorios"]
assert [len(values) for values in weights.values()] == [9919, 9221, 7889, 7319, 7121]

shipping = json.loads((CAPTURE / "sellers-shipping-times.json").read_text())
groups = []
for bucket in shipping["bucket"]:
    if not groups or groups[-1][0] != bucket:
        groups.append([bucket, 0])
    groups[-1][1] += 1
assert groups == [["10-99 orders", 33571], ["100-999 orders", 47697], ["1000+ orders", 18193], ["1-9 orders", 5111]]

docs = Path("docs/api-contracts.md").read_text(encoding="utf-8")
for required in [
    "Sunday as `0`",
    "2017-01-01T00:00:00",
    "cama_mesa_banho` (9,919)",
    "Deferred endpoints: excluded from main-migration parity",
    "`bucket`** (singular)",
]:
    assert required in docs, required

print("verified 17 live FastAPI captures, repeatability, full-response invariants, and compact fixtures")
