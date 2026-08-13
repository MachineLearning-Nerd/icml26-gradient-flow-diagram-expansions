# Conclusion

All six finite contracts pass by independent symbolic checks and optional
reduced-scale gradient-flow corroboration. The paper-level result is **0/6
independently verified; overall INCONCLUSIVE**.

| Claim | Verdict | Confidence |
|---|---|---|
| claim_1 | FINITE CONTRACT PASS | finite evidence |
| claim_2 | FINITE CONTRACT PASS | finite evidence |
| claim_3 | FINITE CONTRACT PASS | finite evidence |
| claim_4 | FINITE CONTRACT PASS | finite evidence |
| claim_5 | FINITE CONTRACT PASS | finite evidence |
| claim_6 | FINITE CONTRACT PASS | finite evidence |

**Limitations (honest):** the numerical GF corroboration is at reduced scale (p=256 for nu=2,
p=32 for nu=4) vs the paper (p=512/256) due to the CPU-only budget; the symbolic verdicts do
not depend on scale. The nu=4 ascent transition brackets rho* with a small finite-size
preemption. The closed-form nu=2 theory is the large-p formal limit (matches GF to ~1% where
the loss is non-negligible). These are documented per claim.

The historical judged score was 0/12. No forecast or new judge score is claimed.
