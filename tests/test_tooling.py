"""Tooling-map seam tests — the 12-primitive benchmark map is a CLAIM, so it is gated.

Never mutate tracked files: the write-path tests copy data/ into a tempdir first
(a read-only --check would hide a write-path bug).
"""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build  # noqa: E402
import validate  # noqa: E402

TOOLING = yaml.safe_load((ROOT / "data" / "tooling.yml").read_text())


class TestToolingData(unittest.TestCase):
    def test_primitives_unique(self):
        names = [t["primitive"] for t in TOOLING]
        self.assertEqual(len(names), len(set(names)), f"duplicate primitive in {names}")

    def test_every_category_renders(self):
        """A category present in data but absent from build.TOOLING_CATS renders nowhere."""
        declared = {k for k, _ in build.TOOLING_CATS}
        used = {t["category"] for t in TOOLING}
        self.assertTrue(used <= declared, f"unrendered categories: {used - declared}")

    def test_benchmark_urls_wellformed(self):
        """Catches the `url https://…` typo class — YAML silently splits on the scheme colon."""
        for t in TOOLING:
            for b in t.get("benchmarks") or []:
                self.assertTrue(
                    b["url"].startswith("https://"),
                    f"{t['primitive']}/{b['name']}: url must be https:// — got {b['url']!r}")
                self.assertNotIn(" ", b["url"].strip(),
                                 f"{t['primitive']}/{b['name']}: whitespace in url")

    def test_no_claim_without_evidence(self):
        """coverage 'none' ⟺ zero benchmarks. The repo's core rule, machine-checked."""
        for t in TOOLING:
            benches = t.get("benchmarks") or []
            if t["coverage"] == "none":
                self.assertEqual(benches, [], f"{t['primitive']}: 'none' but has benchmarks")
            else:
                self.assertTrue(benches, f"{t['primitive']}: claims {t['coverage']} with no benchmark")

    def test_every_primitive_states_its_gap(self):
        """Recording the null is mandatory — an empty gap is an unanswered question."""
        for t in TOOLING:
            self.assertGreater(len(t["gap"].strip()), 20,
                               f"{t['primitive']}: gap must say what is NOT measured")

    def test_secondary_evidence_is_declared_not_dressed_up(self):
        """A 'strong' claim on secondary-only evidence must name the unread primary in its gap."""
        for t in TOOLING:
            if t["evidence"] == "secondary" and t["coverage"] == "strong":
                self.assertRegex(
                    t["gap"], r"(?i)not\s+read|NOT\s+read|primary",
                    f"{t['primitive']}: strong+secondary must flag the unread primary")

    def test_all_primitives_reach_the_readme(self):
        readme = (ROOT / "README.md").read_text()
        for t in TOOLING:
            self.assertIn(f"`{t['primitive']}`", readme,
                          f"{t['primitive']} missing from generated README")


class TestGateActuallyFails(unittest.TestCase):
    """Maker≠checker: prove the gate can FAIL, or it is decoration."""

    def _validate_with(self, mutate):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            shutil.copytree(ROOT / "data", data)
            entries = yaml.safe_load((data / "tooling.yml").read_text())
            mutate(entries)
            (data / "tooling.yml").write_text(yaml.safe_dump(entries))
            original = validate.DATA
            try:
                validate.DATA = data
                return validate.main()
            finally:
                validate.DATA = original

    def test_baseline_copy_is_green(self):
        self.assertEqual(self._validate_with(lambda e: None), [])

    def test_catches_coverage_claimed_without_benchmarks(self):
        def strip(entries):
            for t in entries:
                if t["coverage"] != "none":
                    t["benchmarks"] = []
                    return
        errs = self._validate_with(strip)
        self.assertTrue(any("zero benchmarks" in e for e in errs), errs)

    def test_catches_none_coverage_with_benchmarks(self):
        def stuff(entries):
            for t in entries:
                if t["coverage"] == "none":
                    t["benchmarks"] = [{"name": "x", "url": "https://x", "note": "y"}]
                    return
        errs = self._validate_with(stuff)
        self.assertTrue(any("benchmark(s) listed" in e for e in errs), errs)

    def test_catches_bad_enum(self):
        errs = self._validate_with(lambda e: e[0].__setitem__("cost_metric", "probably-fine"))
        self.assertTrue(any("bad cost_metric" in x for x in errs), errs)

    def test_catches_missing_benchmarks_key(self):
        errs = self._validate_with(lambda e: e[0].pop("benchmarks"))
        self.assertTrue(any("record the null" in x for x in errs), errs)


if __name__ == "__main__":
    unittest.main()
