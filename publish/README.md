# Gradient Flow Through Diagram Expansions — finite audit logbook

**Paper:** Dmitry Yarotsky, Eugene Golikov, and Yaroslav Gusev, “Gradient Flow
Through Diagram Expansions: Learning Regimes and Explicit Solutions”
([arXiv:2602.04548v2](https://arxiv.org/abs/2602.04548v2),
OpenReview `BXE3Z0EHCs`).

## Honest status

**6/6 finite contracts pass; 0/6 paper-level claims independently verified;
overall INCONCLUSIVE.**

The claim pages document symbolic reconstructions and reduced-scale gradient-flow
corroboration. Their raw `VERIFIED` labels
mean finite contract pass, not formal proof of the paper’s universal or
asymptotic statements. Historical judged pages remain under
[historical](pages/historical/index.md).

## Per-claim finite contracts

| Claim | Finite producer | Result |
|---|---|---|
| [C1 polynomial coefficients](pages/claim-c1-polynomial-coefficients/page.md) | Diagram reconstruction, exact polynomial checks, and MC comparison | FINITE CONTRACT PASS |
| [C2 Pareto terms](pages/claim-c2-pareto-terms/page.md) | Computed finite fronts vs source formula | FINITE CONTRACT PASS |
| [C3 NTK regime](pages/claim-c3-ntk-regime/page.md) | Symbolic NTK/staticity checks and optional GF drift | FINITE CONTRACT PASS |
| [C4 mean-field scaling](pages/claim-c4-mean-field-scaling/page.md) | Selected scaling relations from finite front checks | FINITE CONTRACT PASS |
| [C5 `nu=2` solution](pages/claim-c5-nu-2-solution/page.md) | Narayana/limit checks and optional reduced GF curve | FINITE CONTRACT PASS |
| [C6 `nu=4` threshold](pages/claim-c6-nu-4-threshold/page.md) | Quadrature/erfc check and reduced GF bracket | FINITE CONTRACT PASS |

## Reproduce

```bash
uv sync --frozen
uv run python repro/src/verify_diagram_flow.py --no-gf
```

The configured full gate additionally runs the CPU-intensive GF corroboration:

```bash
uv run python repro/src/run_publication_gate.py
```

Source SHA-256:
`6c470ad469118a8bd3b61f82b3456d95169c0581bce9284a0d68b13b8e37ca9b`.
