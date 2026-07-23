#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path


def scalar_kind(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def list_summary(values):
    kinds = sorted({scalar_kind(value) for value in values})
    result = {"length": len(values), "kinds": kinds, "nulls": sum(value is None for value in values)}
    if values and all(isinstance(value, list) for value in values):
        result["row_lengths"] = sorted({len(value) for value in values})
        result["row_kinds"] = sorted({kind for row in values for kind in {scalar_kind(value) for value in row}})
    if values and all(isinstance(value, str) or value is None for value in values):
        strings = [value for value in values if isinstance(value, str)]
        result["first"] = strings[:3]
        result["last"] = strings[-3:]
    if values and all((isinstance(value, (int, float)) and not isinstance(value, bool)) or value is None for value in values):
        numbers = [value for value in values if isinstance(value, (int, float)) and not isinstance(value, bool)]
        result["first"] = numbers[:3]
        result["last"] = numbers[-3:]
        if numbers:
            result["min"] = min(numbers)
            result["max"] = max(numbers)
    return result


def object_summary(payload):
    if not isinstance(payload, dict):
        return {"shape": scalar_kind(payload)}
    result = {"shape": "object", "keys": list(payload.keys()), "fields": {}}
    for key, value in payload.items():
        if isinstance(value, list):
            result["fields"][key] = list_summary(value)
        elif isinstance(value, dict):
            result["fields"][key] = {
                "shape": "object-map",
                "keys": list(value.keys()),
                "value_lengths": {nested_key: len(nested_value) if isinstance(nested_value, list) else None for nested_key, nested_value in value.items()},
            }
        else:
            result["fields"][key] = {"kind": scalar_kind(value), "value": value}
    return result


def main(capture_dir):
    root = Path(capture_dir)
    result = {}
    for response_path in sorted(root.glob("*.json")):
        raw = response_path.read_bytes()
        payload = json.loads(raw)
        info = object_summary(payload)
        info["bytes"] = len(raw)
        info["sha256"] = hashlib.sha256(raw).hexdigest()
        result[response_path.stem] = info
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1])
