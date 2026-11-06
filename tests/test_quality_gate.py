"""Run the action's Bash step against a stand-in scanner to verify its contract."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


ACTION = yaml.safe_load((Path(__file__).resolve().parents[1] / "action.yml").read_text())
SCAN_STEP = next(step for step in ACTION["runs"]["steps"] if step["name"] == "Trigger CodeAnt analysis")


class QualityGateInputTests(unittest.TestCase):
    def run_action(self, value=None, scanner_exit=0):
        if value is None:
            value = ACTION["inputs"]["quality_gate"]["default"]
        self.assertEqual(SCAN_STEP["env"]["QUALITY_GATE"], "${{ inputs.quality_gate }}")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "start_scan.sh").write_text(
                '#!/bin/bash\nprintf "%s\\0" "$@" > arguments.bin\nexit "$SCANNER_EXIT"\n'
            )
            env = {
                **os.environ,
                "ACCESS_TOKEN": "test-token",
                "REPO_NAME": "example/repository",
                "COMMIT_ID": "abc123",
                "BRANCH": "main",
                "INCLUDE_PATHS": "src/path with spaces/**",
                "EXCLUDE_PATHS": "",
                "SCAN_TIMEOUT": "600",
                "SCANNERS": "sast,sca",
                "QUALITY_GATE": str(value),
                "SCANNER_EXIT": str(scanner_exit),
            }
            result = subprocess.run(
                ["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", SCAN_STEP["run"]],
                cwd=root, env=env, capture_output=True, text=True,
            )
            arguments = root / "arguments.bin"
            argv = arguments.read_bytes().decode().split("\0")[:-1] if arguments.exists() else None
            return result, argv

    def test_default_preserves_scan_only_behavior(self):
        result, argv = self.run_action()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("--quality-gate", argv)
        self.assertIn("src/path with spaces/**", argv)
        self.assertEqual(argv[argv.index("-e") + 1], "")

    def test_true_requests_native_enforcement(self):
        result, argv = self.run_action("true")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(argv.count("--quality-gate"), 1)

    def test_false_does_not_request_enforcement(self):
        result, argv = self.run_action("false")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("--quality-gate", argv)

    def test_scanner_failure_is_not_swallowed(self):
        for value in ("true", "false"):
            with self.subTest(quality_gate=value):
                result, _ = self.run_action(value, scanner_exit=7)
                self.assertEqual(result.returncode, 7)

    def test_invalid_input_does_not_start_a_scan(self):
        for value in ("", "tru", "yes", "true; echo unexpected"):
            with self.subTest(quality_gate=value):
                result, argv = self.run_action(value)
                self.assertEqual(result.returncode, 1)
                self.assertIsNone(argv)
                self.assertIn("quality_gate must be", result.stdout)


if __name__ == "__main__":
    unittest.main()
