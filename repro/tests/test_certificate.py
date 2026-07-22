import json, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class TestCertificate(unittest.TestCase):
    def test_six_claims(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'v.json'
            subprocess.run([sys.executable, 'repro/src/verify_diagram_flow.py', '--output', str(output)], cwd=ROOT, check=True)
            self.assertEqual(json.loads(output.read_text())['verified_claims'], 6)
