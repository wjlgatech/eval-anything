"""observe.py — the O of OEC. Tests run against a synthetic transcript in a tempdir
(family rule: tests never touch tracked files or the user's real ~/.claude)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "observe.py"


def make_transcript(dirpath: Path) -> Path:
    lines = [
        {"type": "user", "origin": "user", "timestamp": "2026-07-22T10:00:00Z",
         "gitBranch": "main", "message": {"role": "user", "content": "do the thing"}},
        {"type": "assistant", "timestamp": "2026-07-22T10:00:10Z",
         "message": {"model": "claude-fable-5", "usage": {"output_tokens": 100, "input_tokens": 50},
                     "content": [{"type": "tool_use", "name": "Bash", "input": {}},
                                 {"type": "tool_use", "name": "Edit",
                                  "input": {"file_path": "/tmp/x.py"}},
                                 {"type": "tool_use", "name": "Task", "input": {}}]}},
        {"type": "user", "timestamp": "2026-07-22T10:00:20Z",
         "message": {"role": "user", "content": [
             {"type": "tool_result", "is_error": True, "content": "boom"}]}},
        {"type": "system", "timestamp": "2026-07-22T10:01:00Z"},
    ]
    f = dirpath / "sess-1234.jsonl"
    f.write_text("\n".join(json.dumps(l) for l in lines) + "\nnot json\n")
    return f


class TestObserve(unittest.TestCase):
    def run_observe(self, *args):
        r = subprocess.run([sys.executable, str(SCRIPT), *args],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def test_json_counts(self):
        with tempfile.TemporaryDirectory() as td:
            make_transcript(Path(td))
            (o,) = json.loads(self.run_observe("--path", td, "--json"))
            self.assertEqual(o["user_prompts"], 1)
            self.assertEqual(o["tool_calls"], {"Bash": 1, "Edit": 1, "Task": 1})
            self.assertEqual(o["tool_errors"], 1)
            self.assertEqual(o["subagents_spawned"], 1)
            self.assertEqual(o["files_mutated"], ["/tmp/x.py"])
            self.assertEqual(o["duration_s"], 60.0)
            self.assertEqual(o["skipped_lines"], 1)  # honest count, never silent
            self.assertEqual(o["tokens_out"], 100)

    def test_eval_signals_honest_nulls(self):
        with tempfile.TemporaryDirectory() as td:
            make_transcript(Path(td))
            (e,) = json.loads(self.run_observe("--path", td, "--eval"))
            self.assertAlmostEqual(e["signals"]["tool_error_rate"], 1 / 3, places=3)
            self.assertIn("task_success", e["not_measured"])  # no criterion ⇒ not measured
            self.assertIn("scoreboard", e["note"])

    def test_missing_dir_is_honest_null(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "--path", "/nonexistent-xyz"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("none found", r.stderr)


if __name__ == "__main__":
    unittest.main()
