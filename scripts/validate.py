#!/usr/bin/env python3
"""validate.py — schema gate. No evidence ⇒ No: any miss fails loudly."""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


REQUIRED_META = ["name", "emoji", "title", "tagline", "description", "audience", "github"]

# curated-collection schemas: file → (required keys per entry, allowed categories)
COLLECTIONS = {
    "registry.yml": (["repo", "why", "category"],
                     {"observe", "control", "harness", "agent", "vlm", "vla", "judge", "live", "security"}),
    "papers.yml": (["category", "title", "cite", "url", "why"],
                   {"benchmarks", "judge", "agentic", "vlm", "vla", "meta"}),
    "labs.yml": (["category", "name", "url", "what", "why", "flagship"],
                 {"independent", "government", "academic", "industry"}),
    "blogs.yml": (["category", "author", "title", "url", "year", "why"],
                  {"practitioner", "org"}),
    "people.yml": (["category", "name", "affiliation", "known_for", "why", "link"],
                   {"architects", "arena", "builders", "science", "safety", "vla"}),
    "security.yml": (["category", "name", "url", "what", "why"],
                     {"standards", "papers", "tools", "agentsec", "labs", "people"}),
    "oec.yml": (["pillar", "horizon", "name", "origin", "url", "what", "why"],
                None),  # no `category` key — pillar/horizon checked below
    "examples.yml": (["feature", "tagline", "examples"], None),
}
OEC_PILLARS = {"observe", "evaluate", "control"}
OEC_HORIZONS = {"300y", "30y", "now"}


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
    for fname, (required, cats) in COLLECTIONS.items():
        f = DATA / fname
        if not f.exists():
            errs.append(f"{fname}: missing (curated collection)")
            continue
        try:
            entries = yaml.safe_load(f.read_text()) or []
        except yaml.YAMLError:
            continue  # parse error already reported above
        for i, e in enumerate(entries):
            for k in required:
                if not e.get(k):
                    errs.append(f"{fname}[{i}]: missing {k} ({e.get('name') or e.get('repo') or e.get('title') or '?'})")
            if cats is not None and e.get("category") not in cats:
                errs.append(f"{fname}[{i}]: unknown category {e.get('category')!r}")
            if fname == "oec.yml":
                if e.get("pillar") not in OEC_PILLARS:
                    errs.append(f"oec.yml[{i}]: unknown pillar {e.get('pillar')!r}")
                if e.get("horizon") not in OEC_HORIZONS:
                    errs.append(f"oec.yml[{i}]: unknown horizon {e.get('horizon')!r}")
            if fname == "examples.yml":
                for j, ex in enumerate(e.get("examples") or []):
                    if not ex.get("say") or not ex.get("get"):
                        errs.append(f"examples.yml[{i}].examples[{j}]: needs both say and get")
                if not 1 <= len(e.get("examples") or []) <= 3:
                    errs.append(f"examples.yml[{i}]: needs 1-3 examples ({e.get('feature')})")
    return errs


if __name__ == "__main__":
    errors = main()
    for e in errors:
        print(f"❌ {e}")
    if errors:
        sys.exit(1)
    print("✅ validate green")
