#!/usr/bin/env python3
"""ainative.py — AI-native self-audit. Scores data/ainative.yml principles against
REAL in-repo evidence (a file exists / a regex matches). No evidence ⇒ the principle
fails. `--gate N` exits non-zero below N — a regression in HOW we operate fails CI.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def check(p) -> bool:
    target = ROOT / p["path"]
    if p["kind"] == "file":
        return target.exists()
    if p["kind"] == "grep":
        return target.exists() and re.search(p["pattern"], target.read_text(), re.M) is not None
    return False


if __name__ == "__main__":
    gate = int(sys.argv[sys.argv.index("--gate") + 1]) if "--gate" in sys.argv else 0
    principles = yaml.safe_load((ROOT / "data" / "ainative.yml").read_text())
    passed = 0
    for p in principles:
        ok = check(p["evidence"])
        passed += ok
        print(f"{'✅' if ok else '❌'} {p['id']}: {p['principle']}")
    score = round(100 * passed / len(principles))
    print(f"score: {score}/100 (gate {gate})")
    sys.exit(0 if score >= gate else 1)
