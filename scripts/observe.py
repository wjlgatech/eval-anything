#!/usr/bin/env python3
"""observe.py — the O of OEC: machine-readable observation of agent sessions.

Parses Claude Code session transcripts (~/.claude/projects/<slug>/*.jsonl — the
same ground truth patoles/agent-flow visualizes for humans) and emits observation
summaries an EVAL can consume. Composes, never absorbs: the human surface stays
`npx agent-flow-app` (Apache-2.0); this script is the AI-agent surface + the O→E
bridge. Vocabulary aligned with the OWASP Agent Observability Standard's spirit:
observe what happened, never infer what didn't.

Honesty rules (family non-negotiables):
- Only computed measures — a field that can't be derived is null, never guessed.
- Unparseable lines are COUNTED (skipped_lines), never silently dropped.

Usage:
  python3 scripts/observe.py                 # current project's sessions, human table
  python3 scripts/observe.py --json          # machine-readable (for agents / evals)
  python3 scripts/observe.py --eval          # OEC signals: observation → eval-ready
  python3 scripts/observe.py --path <file|dir>   # any transcript file or directory
  python3 scripts/observe.py --session <id-prefix>   # restrict to one session
"""
import json
import sys
from datetime import datetime
from pathlib import Path

MUTATING_TOOLS = {"Edit", "Write", "NotebookEdit"}


def project_transcript_dir(cwd: Path) -> Path:
    # Claude Code slugs a project path by replacing every non-alphanumeric char
    # (/, ., _) with "-" — verified against a real ~/.claude/projects entry.
    slug = "".join(c if c.isalnum() else "-" for c in str(cwd.resolve()))
    return Path.home() / ".claude" / "projects" / slug


def parse_ts(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        return None


def observe_file(path: Path) -> dict:
    o = {
        "session": path.stem,
        "file": str(path),
        "started_at": None, "ended_at": None, "duration_s": None,
        "user_prompts": 0, "assistant_messages": 0,
        "tool_calls": {}, "tool_errors": 0,
        "subagent_lines": 0, "subagents_spawned": 0,
        "files_mutated": set(), "models": set(), "git_branches": set(),
        "tokens_out": 0, "tokens_in": 0,
        "lines": 0, "skipped_lines": 0,
    }
    first_ts, last_ts = None, None
    for line in path.open(encoding="utf-8", errors="replace"):
        o["lines"] += 1
        try:
            d = json.loads(line)
        except (json.JSONDecodeError, UnicodeDecodeError):
            o["skipped_lines"] += 1
            continue
        ts = parse_ts(d.get("timestamp"))
        if ts:
            first_ts = min(first_ts, ts) if first_ts else ts
            last_ts = max(last_ts, ts) if last_ts else ts
        if d.get("gitBranch"):
            o["git_branches"].add(d["gitBranch"])
        if d.get("isSidechain"):
            o["subagent_lines"] += 1
        t = d.get("type")
        msg = d.get("message") or {}
        content = msg.get("content") if isinstance(msg, dict) else None
        if t == "user":
            if d.get("origin") == "user" or isinstance(content, str):
                o["user_prompts"] += 1
            if isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("is_error"):
                        o["tool_errors"] += 1
        elif t == "assistant":
            o["assistant_messages"] += 1
            if isinstance(msg, dict):
                if msg.get("model"):
                    o["models"].add(msg["model"])
                usage = msg.get("usage") or {}
                o["tokens_out"] += usage.get("output_tokens") or 0
                o["tokens_in"] += (usage.get("input_tokens") or 0) + (usage.get("cache_read_input_tokens") or 0)
            if isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "tool_use":
                        name = b.get("name", "?")
                        o["tool_calls"][name] = o["tool_calls"].get(name, 0) + 1
                        if name in ("Task", "Agent"):
                            o["subagents_spawned"] += 1
                        if name in MUTATING_TOOLS:
                            fp = (b.get("input") or {}).get("file_path")
                            if fp:
                                o["files_mutated"].add(fp)
    if first_ts and last_ts:
        o["started_at"] = first_ts.isoformat()
        o["ended_at"] = last_ts.isoformat()
        o["duration_s"] = round((last_ts - first_ts).total_seconds(), 1)
    o["files_mutated"] = sorted(o["files_mutated"])
    o["models"] = sorted(o["models"])
    o["git_branches"] = sorted(o["git_branches"])
    return o


def eval_signals(o: dict) -> dict:
    """The O→E bridge: eval-ready signals with honest nulls."""
    total_calls = sum(o["tool_calls"].values())
    return {
        "session": o["session"],
        "signals": {
            "tool_error_rate": round(o["tool_errors"] / total_calls, 4) if total_calls else None,
            "tool_calls_total": total_calls,
            "tool_calls_per_prompt": round(total_calls / o["user_prompts"], 2) if o["user_prompts"] else None,
            "subagents_spawned": o["subagents_spawned"],
            "files_mutated": len(o["files_mutated"]),
            "duration_s": o["duration_s"],
            "tokens_out": o["tokens_out"] or None,
        },
        "not_measured": [k for k, v in {
            "task_success": "needs a stated criterion — observation alone cannot judge",
            "cost_usd": "transcript carries tokens, not prices",
        }.items()],
        "note": "signals are OBSERVATIONS — pass them to a criterion (judge/gate) to make them an eval; "
                "no criterion ⇒ this is a scoreboard, not a loop",
    }


def human(observations: list) -> str:
    out = []
    for o in observations:
        top = sorted(o["tool_calls"].items(), key=lambda kv: -kv[1])[:5]
        out.append(f"session {o['session'][:8]}…  ({o['duration_s'] or '?'}s, {o['lines']} lines"
                   + (f", {o['skipped_lines']} unparseable" if o["skipped_lines"] else "") + ")")
        out.append(f"  prompts {o['user_prompts']} · assistant msgs {o['assistant_messages']} · "
                   f"tool calls {sum(o['tool_calls'].values())} ({o['tool_errors']} errors) · "
                   f"subagents {o['subagents_spawned']} · files mutated {len(o['files_mutated'])}")
        out.append(f"  top tools: " + (", ".join(f"{n}×{c}" for n, c in top) or "—"))
        out.append(f"  models: {', '.join(o['models']) or '—'}  tokens out {o['tokens_out']:,}")
    out.append("")
    out.append("👁️ human live view: `npx agent-flow-app` (patoles/agent-flow, Apache-2.0) — same ground truth, drawn")
    out.append("⚖️ eval-ready signals: re-run with --eval · machine-readable: --json")
    return "\n".join(out)


def main(argv):
    args = list(argv)
    path = Path(args[args.index("--path") + 1]) if "--path" in args else project_transcript_dir(Path.cwd())
    sess = args[args.index("--session") + 1] if "--session" in args else None
    files = [path] if path.is_file() else sorted(path.glob("*.jsonl")) if path.is_dir() else []
    if sess:
        files = [f for f in files if f.stem.startswith(sess)]
    if not files:
        print(f"none found — no transcripts at {path}", file=sys.stderr)
        return 1
    obs = [observe_file(f) for f in files]
    if "--eval" in args:
        print(json.dumps([eval_signals(o) for o in obs], indent=2))
    elif "--json" in args:
        print(json.dumps(obs, indent=2))
    else:
        print(human(obs))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
