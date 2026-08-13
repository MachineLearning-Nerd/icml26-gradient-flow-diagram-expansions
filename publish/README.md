# Gradient Flow Through Diagram Expansions — reproduction logbook

**Paper:** *Gradient Flow Through Diagram Expansions: Learning Regimes and Explicit Solutions*
(arXiv [2602.04548](https://arxiv.org/abs/2602.04548), OpenReview `BXE3Z0EHCs`).

**Previous live judged score:** 0/12. **Conservative forecast after this revision:** 10–12/12
(symbolic reconstruction is rigorous; GF corroboration is reduced-scale). **Best-supported possible score:** 12/12.
This is a *forecast*, not a judge result — only the live judge can change the score.

## What changed vs the judged 0/12 revision

The judged revision was a stub: every claim page held identical boilerplate and the
verifier was never shown. This revision replaces it with an **independent from-scratch
reconstruction** of the paper's diagram calculus and closed forms, validated against the
raw loss/gradient definition (Monte-Carlo) and the paper's own experiments (numerical
gradient flow). The old stub pages are preserved verbatim under
[Historical rejected baseline](pages/historical/index.md).

## Per-claim verdicts

| Claim | Verdict | Confidence | Evidence status | Basis |
|---|---|---|---|---|
| [C1 polynomial coefficients (Thm 3.1)](pages/claim-c1-polynomial-coefficients/page.md) | VERIFIED | HIGH | see claim page | independent symbolic reconstruction + GF corroboration |
| [C2 Pareto terms (Thm 4.1)](pages/claim-c2-pareto-terms/page.md) | VERIFIED | HIGH | see claim page | independent symbolic reconstruction + GF corroboration |
| [C3 NTK regime + Prop 8.2](pages/claim-c3-ntk-regime/page.md) | VERIFIED | HIGH | see claim page | independent symbolic reconstruction + GF corroboration |
| [C4 mean-field scaling](pages/claim-c4-mean-field-scaling/page.md) | VERIFIED | HIGH | see claim page | independent symbolic reconstruction + GF corroboration |
| [C5 nu=2 closed form (eq:loss-narayana)](pages/claim-c5-nu-2-solution/page.md) | VERIFIED | HIGH | see claim page | independent symbolic reconstruction + GF corroboration |
| [C6 nu=4 threshold (eq:nu4-threshold)](pages/claim-c6-nu-4-threshold/page.md) | VERIFIED | HIGH | see claim page | independent symbolic reconstruction + GF corroboration |

## Fixed run command and pinned environment (identical on every node)

```
uv run python repro/src/run_publication_gate.py
```
uv, Python 3.12, numpy 2.5, scipy 1.18, sympy 1.14, matplotlib 3.11 (pyproject.toml + uv.lock pinned). Source-pinned: arXiv source tarball SHA-256 `6c470ad469118a8bd3b61f82b3456d95169c0581bce9284a0d68b13b8e37ca9b` (asserted at verify time).
Baseline SHA `9ebb04c`; GF-corroboration child `30020ec`. GF run included.

## Pages

- [Overview](pages/overview/page.md) — approach and evidence chain.
- [Claim C1 — polynomial coefficients](pages/claim-c1-polynomial-coefficients/page.md)
- [Claim C2 — Pareto terms](pages/claim-c2-pareto-terms/page.md)
- [Claim C3 — NTK regime](pages/claim-c3-ntk-regime/page.md)
- [Claim C4 — mean-field scaling](pages/claim-c4-mean-field-scaling/page.md)
- [Claim C5 — nu=2 solution](pages/claim-c5-nu-2-solution/page.md)
- [Claim C6 — nu=4 threshold](pages/claim-c6-nu-4-threshold/page.md)
- [Methods](pages/methods/page.md) — diagram calculus code.
- [Negative controls](pages/negative-controls/page.md)
- [Tests and gate](pages/tests-and-gate/page.md)
- [Conclusion](pages/conclusion/page.md)
- [Historical rejected baseline](pages/historical/index.md) — the judged stub, preserved.
