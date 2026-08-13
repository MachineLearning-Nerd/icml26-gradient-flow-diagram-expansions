# Tests and gate

`repro/src/run_publication_gate.py` runs the verifier then `pytest repro/tests`. The verifier
**exits nonzero** if any claim is not VERIFIED (fail-closed). Tests directly exercise the core
invariants (the SYM nu=2 s=0 hand-calc, the MC engine match, the Pareto-front match, the Prop
8.2 identity, the Narayana coefficients, the F erfc agreement).

Baseline run (local): 8 tests passed, gate passed, all 6 VERIFIED, ~38 s.
