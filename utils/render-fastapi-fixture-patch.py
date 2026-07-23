#!/usr/bin/env python3
import json
import sys
from pathlib import Path


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

LARGE_COLUMNAR = {
    "customers-clv-map",
    "orders-costs",
    "orders-daily",
    "sellers-performance",
    "sellers-review-sales",
    "sellers-shipping-times",
}


def head_and_tail(values):
    if len(values) <= 6:
        return values
    return values[:3] + values[-3:]


def compact_payload(name, payload):
    if name in FULL:
        return payload
    if name in LARGE_COLUMNAR:
        return {key: head_and_tail(value) for key, value in payload.items()}
    if name == "categories-weights":
        return {key: head_and_tail(value) for key, value in payload.items()}
    raise ValueError(f"No fixture strategy for {name}")


def emit_add(path, content):
    print(f"*** Add File: {path}")
    for line in content.splitlines():
        print(f"+{line}")


def main(capture_dir):
    root = Path(capture_dir)
    print("*** Begin Patch")
    for source_path in sorted(root.glob("*.json")):
        payload = json.loads(source_path.read_text(encoding="utf-8"))
        compact = compact_payload(source_path.stem, payload)
        rendered = json.dumps(compact, ensure_ascii=False, indent=2) + "\n"
        emit_add(f"src/test/resources/contracts/fastapi/{source_path.name}", rendered)
    print("*** End Patch")


if __name__ == "__main__":
    main(sys.argv[1])
