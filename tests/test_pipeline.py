"""Seam tests — the definition of done. Never mutate tracked files."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build  # noqa: E402
import validate  # noqa: E402


class TestPipeline(unittest.TestCase):
    def test_build_deterministic(self):
        self.assertEqual(build.render(), build.render())

    def test_no_drift(self):
        self.assertEqual((ROOT / "README.md").read_text(), build.render(),
                         "README drifted — run `make build`")

    def test_validate_green(self):
        self.assertEqual(validate.main(), [])


if __name__ == "__main__":
    unittest.main()
