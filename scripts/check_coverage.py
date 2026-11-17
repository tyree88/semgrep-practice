"""Fail unless every rule fires on app/vulnerable.py and nothing fires on app/fixed.py.

Usage: semgrep scan --config rules/ app/ --json --metrics=off | python3 scripts/check_coverage.py
"""
import json
import pathlib
import sys

rule_ids = {p.stem for p in pathlib.Path("rules").glob("*.yaml")}
results = json.load(sys.stdin)["results"]
hit = {r["check_id"].rsplit(".", 1)[-1] for r in results if r["path"].endswith("app/vulnerable.py")}
fixed = [f'{r["path"]}:{r["start"]["line"]} {r["check_id"]}' for r in results if r["path"].endswith("app/fixed.py")]

missing = sorted(rule_ids - hit)
if missing:
    print("Rules with no finding in app/vulnerable.py:", ", ".join(missing))
if fixed:
    print("False positives in app/fixed.py:", *fixed, sep="\n  ")
if missing or fixed:
    sys.exit(1)
print(f"OK: all {len(rule_ids)} rules fire on vulnerable.py, 0 findings on fixed.py")
