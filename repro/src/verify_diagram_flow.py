"""Source-pinned verifier for arXiv:2602.04548 (OpenReview BXE3Z0EHCs).

Runs the six claim checks (independent symbolic reconstruction of the diagram
calculus, Pareto front, NTK relations, nu=2 closed form, nu=4 threshold) and,
when GF_ENABLED is set in repro/src/run_config.py, the numerical gradient-flow
corroboration.  Writes outputs/verification.json and exits nonzero on failure.

Source pin: the arXiv source tarball is hashed and key theorem/section anchors
are asserted present, so the check is tied to the exact paper revision.
"""

from __future__ import annotations
import argparse
import hashlib
import json
import sys
import tarfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

ARC = ROOT / "source/arxiv-2602.04548.tar"
SHA = "6c470ad469118a8bd3b61f82b3456d95169c0581bce9284a0d68b13b8e37ca9b"
# anchors that must appear in the paper source (theorem/eq labels & section refs)
ANCHORS = [
    "\\label{th:polycoeff}",     # Theorem 3.1
    "\\label{th:pareto_front}",  # Theorem 4.1
    "Point C and Point B",       # NTK discussion (Sec. 5/8)
    "\\label{eq:loss-narayana}", # nu=2 closed form (Sec. 9)
    "\\label{eq:nu4-threshold}", # nu=4 threshold (Sec. 10)
    "\\label{prop:ntk_training_main}",  # Prop 8.1 (ASYM NTK)
]


def source_audit() -> dict:
    got = hashlib.sha256(ARC.read_bytes()).hexdigest()
    assert got == SHA, f"source SHA mismatch: {got} != {SHA}"
    with tarfile.open(ARC) as z:
        tex = z.extractfile("camera_ready.tex").read().decode()
    for tok in ANCHORS:
        assert tok in tex, f"missing source anchor: {tok}"
    return {"source_sha256": got, "anchors_present": ANCHORS,
            "tex_bytes": len(tex)}


def main():
    import symbolic_checks as sc
    import diagrams as dg
    from run_config import GF_ENABLED
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, default=ROOT / "outputs/verification.json")
    args = p.parse_args()

    t0 = time.time()
    audit = source_audit()

    results = {"paper": "BXE3Z0EHCs", "source_audit": audit, "gf_enabled": GF_ENABLED}

    # ---- Claim 1: Theorem 3.1 polynomiality + MC cross-check of the engine ----
    c1_poly = [sc.claim1_polynomial(nu, sym, s)
               for (nu, sym, s) in [(2, True, 0), (2, True, 1), (3, False, 0), (4, True, 0)]]
    c1_mc = sc.claim1_mc_crosscheck()
    results["claim_1"] = {
        "statement": "For polynomial/Kronecker-delta targets, T^s E[d^sL/dt^s(0)] is a "
                     "polynomial in (H,p,sigma^2) (Thm 3.1).",
        "reconstructed_polynomials": c1_poly,
        "mc_engine_validation": c1_mc,
        "verdict": "VERIFIED" if c1_mc["pass"] else "FALSIFIED",
    }

    # ---- Claim 2: Theorem 4.1 Pareto-optimal terms ----
    c2 = sc.claim2_pareto([(2, True, 1), (2, True, 2), (4, True, 1),
                           (3, False, 1), (3, False, 2), (4, False, 1), (2, False, 2)])
    results["claim_2"] = {
        "statement": "Pareto-optimal terms of Y_s are p^{Q(n,sD)} H^n sigma^{...} (Thm 4.1).",
        "check": c2,
        "verdict": "VERIFIED" if c2["all_match"] else "FALSIFIED",
    }

    # ---- Claim 3: NTK regime on B-C (ASYM) + Prop 8.2 SYM nu=2 staticity ----
    c3 = sc.claim3_ntk_symbolic()
    results["claim_3"] = {
        "statement": "NTK regime appears on B-C (ASYM); Prop 8.2: SYM nu=2 NTK is "
                     "static iff the model is static (no NTK limit in SYM).",
        "symbolic_check": c3,
        "verdict": "VERIFIED" if c3["prop_8_2_pass"] else "FALSIFIED",
    }

    # ---- Claim 4: mean-field scaling sigma^2 ~ 1/H (SYM) , ~ 1/H^{2/nu} (ASYM) ----
    c4 = sc.claim4_meanfield()
    results["claim_4"] = {
        "statement": "Mean-field init variance: sigma^2 ~ 1/H (SYM) , ~ 1/H^{2/nu} (ASYM).",
        "check": c4,
        "verdict": "VERIFIED" if c4["pass"] else "FALSIFIED",
    }

    # ---- Claim 5: SYM nu=2 closed form (eq:loss-narayana) ----
    c5 = sc.claim5_nu2_symbolic()
    results["claim_5"] = {
        "statement": "SYM nu=2 closed-form E[L(t)] (eq:loss-narayana), all scalings.",
        "symbolic_check": c5,
        "verdict": "VERIFIED" if c5["pass"] else "FALSIFIED",
    }

    # ---- Claim 6: SYM nu=4 ascent threshold (eq:nu4-threshold) ----
    c6 = sc.claim6_nu4_threshold()
    results["claim_6"] = {
        "statement": "SYM nu=4 ascent converges iff p^3 sigma^4 < rho* (eq:nu4-threshold).",
        "symbolic_check": c6,
        "verdict": "VERIFIED" if c6["pass"] else "FALSIFIED",
    }

    # ---- Optional numerical GF corroboration (claims 3b, 5, 6) ----
    if GF_ENABLED:
        import gf_experiments as gf
        results["gf_claim_5"] = gf.claim5_numerical(str(ROOT / "outputs/gf"))
        results["gf_claim_3b"] = gf.claim3b_numerical(str(ROOT / "outputs/gf"))
        results["gf_claim_6"] = gf.claim6_numerical(str(ROOT / "outputs/gf"))

    verdicts = {k: results[k]["verdict"] for k in
                ("claim_1", "claim_2", "claim_3", "claim_4", "claim_5", "claim_6")}
    results["verdicts"] = verdicts
    results["verified_claims"] = sum(1 for v in verdicts.values() if v == "VERIFIED")
    results["falsified_claims"] = sum(1 for v in verdicts.values() if v == "FALSIFIED")
    results["runtime_sec"] = round(time.time() - t0, 2)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, default=str) + "\n")
    print(json.dumps({"verdicts": verdicts,
                      "verified": results["verified_claims"],
                      "falsified": results["falsified_claims"],
                      "runtime_sec": results["runtime_sec"]}, indent=2))
    # fail-closed: any non-VERIFIED core claim is a nonzero exit
    if any(v != "VERIFIED" for v in verdicts.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
