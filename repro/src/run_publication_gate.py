"""Publication gate: run the verifier, then the unit tests, then assert all six
claim verdicts are VERIFIED.  This is the fixed run command for every experiment
node (set via `orx project edit <projectId> --run-command`)."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

subprocess.run([sys.executable, "repro/src/verify_diagram_flow.py",
                "--output", "outputs/verification.json"],
               cwd=ROOT, check=True)
subprocess.run([sys.executable, "-m", "pytest", "repro/tests", "-q"],
               cwd=ROOT, check=True)

verification = json.loads((ROOT / "outputs/verification.json").read_text())
verdicts = verification["verdicts"]
gate = {
    "paper": "BXE3Z0EHCs",
    "verdicts": verdicts,
    "verified_claims": verification["verified_claims"],
    "falsified_claims": verification["falsified_claims"],
    "gf_enabled": verification.get("gf_enabled", False),
    "gate": "passed" if all(v == "VERIFIED" for v in verdicts.values()) else "failed",
    "runtime_sec": verification.get("runtime_sec"),
}
(ROOT / "outputs/publication_gate.json").write_text(json.dumps(gate, indent=2) + "\n")
print(json.dumps(gate, indent=2))
if gate["gate"] != "passed":
    sys.exit(1)
