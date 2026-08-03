#!/usr/bin/env python3
"""sync.py — the meta-repo heartbeat. Refreshes data/registry.yml (stars, last push)
for every tracked upstream repo via the OPEN GitHub API, then regenerates the README.

Honest-by-construction: on any failure (rate limit, network, 404) it records
last_sync_error and moves on — "none found", never fabricated. Runs weekly in CI
(human-gated PR) or locally via `make sync`. NOT part of `make check` (no network
in the finish line).
"""
import json
import subprocess
import sys
import urllib.request
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "registry.yml"


def fetch(repo: str) -> dict:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}",
        headers={"User-Agent": "meta-repo-sync", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


if __name__ == "__main__":
    entries = yaml.safe_load(REG.read_text()) or []
    moved = []
    for e in entries:
        try:
            data = fetch(e["repo"])
            old = e.get("stars")
            e["stars"] = data.get("stargazers_count")
            e["pushed_at"] = data.get("pushed_at")
            e["last_sync"] = str(date.today())
            e.pop("last_sync_error", None)
            if old is not None and e["stars"] != old:
                moved.append(f"{e['repo']}: ⭐ {old} → {e['stars']}")
        except Exception as ex:  # record the null, never fabricate
            e["last_sync_error"] = f"{type(ex).__name__} — none found"
    REG.write_text(yaml.safe_dump(entries, sort_keys=False, allow_unicode=True))
    # Regenerate EVERY derived artifact, not just the README. Missing build_brief.py here left
    # `make check` red after every sync (brief-drift), which would have failed the weekly
    # automation's own PR — caught 2026-08-03 while replaying a stale sync branch.
    for gen in ("build.py", "build_brief.py"):
        subprocess.run([sys.executable, str(ROOT / "scripts" / gen)], check=True)
    print("what moved:" if moved else "what moved: (nothing this week)")
    for m in moved:
        print(f"  {m}")
