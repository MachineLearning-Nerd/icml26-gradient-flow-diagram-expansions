<!-- Historical rejected baseline (judged 0/12). Superseded by the current claim pages. -->
# Tests and gate


---
<!-- trackio-cell
{"type": "code", "id": "cell_ded161db2b7c", "created_at": "2026-07-22T13:03:00+00:00", "title": "Run publication gate", "command": [".venv/bin/python", "repro/src/run_publication_gate.py"], "exit_code": 0, "duration_s": 3.74}
-->
````bash
$ .venv/bin/python repro/src/run_publication_gate.py
````

exit 0 · 3.7s


````python title=run_publication_gate.py
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
subprocess.run([sys.executable, 'repro/src/verify_diagram_flow.py', '--output', 'outputs/verification.json'], cwd=ROOT, check=True)
subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'repro/tests', '-v'], cwd=ROOT, check=True)
verification = json.loads((ROOT / 'outputs/verification.json').read_text())
assert verification['verified_claims'] == 6 and verification['falsified_claims'] == 0
gate = {'paper': 'BXE3Z0EHCs', 'gate': 'passed', 'tests_passed': True, 'publication_gate_passed': True, 'verified_claims': 6, 'scope': verification['scope']}
(ROOT / 'outputs/publication_gate.json').write_text(json.dumps(gate, indent=2) + '\n')
print(json.dumps(gate, indent=2))

````


````output
{
  "paper": "BXE3Z0EHCs",
  "source_sha256": "6c470ad469118a8bd3b61f82b3456d95169c0581bce9284a0d68b13b8e37ca9b",
  "scope": "Source-pinned finite analytic certificate for polynomial/Pareto and explicit gradient-flow formulas; not a replacement for universal proofs.",
  "claims": {
    "C1": {
      "status": "verified",
      "polynomial_cells": 18
    },
    "C2": {
      "status": "verified",
      "pareto_cells": 60
    },
    "C3": {
      "status": "verified",
      "ntk_scaling_cells": 3
    },
    "C4": {
      "status": "verified",
      "mean_field_scaling_cells": 6
    },
    "C5": {
      "status": "verified",
      "nu2_limit_cells": 5
    },
    "C6": {
      "status": "verified",
      "nu4_rho_star": 0.5920560161706298
    }
  },
  "verified_claims": 6,
  "falsified_claims": 0
}
test_six_claims (test_certificate.TestCertificate.test_six_claims) ... {
  "paper": "BXE3Z0EHCs",
  "source_sha256": "6c470ad469118a8bd3b61f82b3456d95169c0581bce9284a0d68b13b8e37ca9b",
  "scope": "Source-pinned finite analytic certificate for polynomial/Pareto and explicit gradient-flow formulas; not a replacement for universal proofs.",
  "claims": {
    "C1": {
      "status": "verified",
      "polynomial_cells": 18
    },
    "C2": {
      "status": "verified",
      "pareto_cells": 60
    },
    "C3": {
      "status": "verified",
      "ntk_scaling_cells": 3
    },
    "C4": {
      "status": "verified",
      "mean_field_scaling_cells": 6
    },
    "C5": {
      "status": "verified",
      "nu2_limit_cells": 5
    },
    "C6": {
      "status": "verified",
      "nu4_rho_star": 0.5920560161706298
    }
  },
  "verified_claims": 6,
  "falsified_claims": 0
}
ok

----------------------------------------------------------------------
Ran 1 test in 1.834s

OK
{
  "paper": "BXE3Z0EHCs",
  "gate": "passed",
  "tests_passed": true,
  "publication_gate_passed": true,
  "verified_claims": 6,
  "scope": "Source-pinned finite analytic certificate for polynomial/Pareto and explicit gradient-flow formulas; not a replacement for universal proofs."
}

````
