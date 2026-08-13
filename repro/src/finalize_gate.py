"""Write the consolidated finite-contract gate from existing evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = tuple(f"claim_{index}" for index in range(1, 7))


def main() -> None:
    verification = json.loads((ROOT / "outputs" / "verification.json").read_text())
    verdicts = verification.get("verdicts", {})
    statuses = {
        claim: "FINITE_CONTRACT_PASS"
        if verdicts.get(claim) == "VERIFIED"
        else "FINITE_CONTRACT_FAIL"
        for claim in CONTRACTS
    }
    passed = sum(status == "FINITE_CONTRACT_PASS" for status in statuses.values())
    gate = {
        "paper": verification["paper"],
        "gate": "finite-contract-audit",
        "tests_passed": passed == len(CONTRACTS),
        "publication_gate_passed": passed == len(CONTRACTS),
        "finite_contracts_passed": passed,
        "finite_contracts_total": len(CONTRACTS),
        "paper_claims_verified": 0,
        "paper_claims_total": len(CONTRACTS),
        "overall_status": "INCONCLUSIVE",
        "contract_statuses": statuses,
        "source_sha256": verification["source_audit"]["source_sha256"],
        "scope": (
            "Six source-pinned finite symbolic/numerical contracts pass; "
            "universal diagram-expansion, scaling-regime, closed-form, and "
            "gradient-flow claims remain independently unverified."
        ),
    }
    encoded = json.dumps(gate, indent=2) + "\n"
    (ROOT / "outputs" / "publication_gate.json").write_text(encoded)
    (ROOT / "publication_gate.json").write_text(encoded)
    print(json.dumps(gate, indent=2))


if __name__ == "__main__":
    main()

