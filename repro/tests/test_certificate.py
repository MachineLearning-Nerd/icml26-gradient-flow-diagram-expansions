"""Unit tests: exercise the core invariants of the reconstruction directly, so a
green gate means the symbolic machinery (not just the orchestrator) is sound."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "repro/src"))

import diagrams as dg
import symbolic_checks as sc
from fractions import Fraction


def test_claim1_handcheck_sym_nu2_s0():
    """Y_0 for SYM nu=2 must equal 1/2 sigma4(pH^2+p^2H+pH) - pH sigma2
    (independent hand calculation of E[1/2 D_4 - R_2])."""
    p = dg.star_power(2, True, 0)
    expected = {(1, 2, 4): Fraction(1, 2), (2, 1, 4): Fraction(1, 2),
                (1, 1, 4): Fraction(1, 2), (1, 1, 2): Fraction(-1)}
    assert set(p.items()) == set(expected.items())


def test_claim1_mc_engine_matches_definition():
    r = sc.claim1_mc_crosscheck()
    assert r["pass"], r


def test_claim2_pareto_matches_thm_4_1():
    r = sc.claim2_pareto([(2, True, 2), (3, False, 1), (4, True, 1), (4, False, 1)])
    assert r["all_match"], r


def test_claim3_prop_8_2_identity():
    r = sc.claim3_ntk_symbolic()
    assert r["prop_8_2_pass"], r


def test_claim4_meanfield_scaling():
    r = sc.claim4_meanfield()
    assert r["pass"], r


def test_claim5_narayana_and_limit():
    r = sc.claim5_nu2_symbolic()
    assert r["pass"], r


def test_claim6_F_erfc_vs_quadrature():
    r = sc.claim6_nu4_threshold()
    assert r["F_quadrature_vs_erfc_maxrelerr"] < 1e-6, r


def test_verifier_writes_six_verified_claims():
    import subprocess, json, tempfile
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "v.json"
        subprocess.run([sys.executable, "repro/src/verify_diagram_flow.py",
                        "--output", str(out)], cwd=ROOT, check=True)
        v = json.loads(out.read_text())
        assert v["verified_claims"] == 6 and v["falsified_claims"] == 0
        assert all(x == "VERIFIED" for x in v["verdicts"].values())
