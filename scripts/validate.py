#!/usr/bin/env python3
"""validate.py — schema gate. No evidence ⇒ No: any miss fails loudly."""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


REQUIRED_META = ["name", "emoji", "title", "tagline", "description", "audience", "github"]

def main():
    errs = []
    files = sorted(DATA.glob("*.yml"))
    if not files:
        errs.append("data/ holds no .yml files")
    for f in files:
        try:
            yaml.safe_load(f.read_text())
        except yaml.YAMLError as e:
            errs.append(f"{f.name}: parse error: {e}")
    meta = yaml.safe_load((DATA / "meta.yml").read_text()) if (DATA / "meta.yml").exists() else {}
    for k in REQUIRED_META:
        if not meta.get(k):
            errs.append(f"meta.yml missing: {k}")
    return errs


if __name__ == "__main__":
    errors = main()
    for e in errors:
        print(f"❌ {e}")
    if errors:
        sys.exit(1)
    print("✅ validate green")
