---
title: "ICML 2026 — Gradient Flow Through Diagram Expansions"
emoji: "🌀"
colorFrom: blue
colorTo: purple
sdk: static
pinned: false
tags:
  - icml2026-repro
  - paper-BXE3Z0EHCs
  - source-pinned
  - finite-audit
---

# ICML 2026 — Gradient Flow Through Diagram Expansions

Independent, CPU-only, source-pinned finite audit for:

> Dmitry Yarotsky, Eugene Golikov, and Yaroslav Gusev. “Gradient Flow Through
> Diagram Expansions: Learning Regimes and Explicit Solutions.”
> [arXiv:2602.04548v2](https://arxiv.org/abs/2602.04548v2).
> OpenReview: [BXE3Z0EHCs](https://openreview.net/forum?id=BXE3Z0EHCs).

Repository name: `icml26-gradient-flow-diagram-expansions`

## Current status

**Overall: INCONCLUSIVE.** The canonical branch contains six independent,
source-pinned finite contracts. All six pass, but that does not independently
prove the paper’s universal diagram-expansion, scaling-regime, closed-form, or
gradient-flow claims.

| Layer | Result | Meaning |
| --- | --- | --- |
| Finite contract checks | 6/6 pass | Source anchors, symbolic reconstructions, finite comparisons, numerical corroboration, and declared checks pass. |
| Paper-level claims | 0/6 independently verified | Finite grids, Monte Carlo, and reduced-scale GF runs do not establish universal limits or theorem quantifiers. |
| Consolidated status | INCONCLUSIVE | This is reproducible finite evidence, not a formal proof certificate. |

The raw `outputs/verification.json` uses `VERIFIED` for finite
producer verdicts. The consolidated gate in `publication_gate.json`
renames those outcomes `FINITE_CONTRACT_PASS` and reports the
paper-level boundary separately.

The local source archive is pinned to SHA-256
`6c470ad469118a8bd3b61f82b3456d95169c0581bce9284a0d68b13b8e37ca9b`.
The public arXiv record is currently v2; the local archive remains identified
by its hash for exact reproducibility.

## What the paper does

The paper develops a diagram-expansion framework for gradient-flow dynamics in
large learning problems. It studies scaling regimes for tensor
Canonical Polyadic decomposition, including lazy/NTK and mean-field behavior,
and derives explicit solutions in selected symmetric settings. The repository
reconstructs selected diagram and formula checks and adds reduced-scale
gradient-flow corroboration.

## Claim ledger: producer → evidence → boundary

The main producer is `repro/src/verify_diagram_flow.py`. Its symbolic
subroutines live in `repro/src/diagrams.py` and
`repro/src/symbolic_checks.py`; optional numerical corroboration is
produced by `repro/src/gf_experiments.py`. The fixed runner is
`repro/src/run_publication_gate.py`.

| Claim | Paper object | Evidence producer and check | Boundary |
| --- | --- | --- | --- |
| C1 | Theorem 3.1 polynomiality | Diagram reconstruction plus exact polynomial checks and Monte Carlo comparison; maximum recorded relative error is about 0.0057. | Finite reconstruction and MC validation; not a universal proof. |
| C2 | Theorem 4.1 Pareto terms | Computed finite fronts are compared with the source formula across selected symmetric/asymmetric `nu` and order settings. | Finite front comparison; not the full theorem over all parameters. |
| C3 | NTK regime and Proposition 8.2 | Symbolic NTK/staticity checks, with optional GF drift corroboration. | Selected symbolic identities and trajectories; not a proof of all regime classifications. |
| C4 | Mean-field initialization scaling | Finite checks of `sigma^2 ~ 1/H` and `sigma^2 ~ 1/H^{2/nu}` for selected widths/orders. | Scaling examples; not a universal asymptotic derivation. |
| C5 | Symmetric `nu=2` closed form | Narayana/limit symbolic checks plus optional reduced-scale GF curve comparison. | Finite symbolic and numerical agreement; not an independent derivation of every limiting step. |
| C6 | Symmetric `nu=4` ascent threshold | Independent quadrature/erfc agreement at about `1.0e-14`, `rho*` near 2.0778 for `theta=1`, and reduced-scale `p=32` GF bracketing. | Reduced-scale corroboration; finite-size effects remain and the theorem is not independently proved. |

A contract passes when the pinned source anchors and declared finite checks pass.
The raw label `VERIFIED` should therefore be read as “finite contract
pass,” not “paper theorem verified.”

## Reproduce

Install the locked environment:

```bash
uv sync --frozen
```

Fast symbolic verification without the heavy gradient-flow campaign:

```bash
uv run python repro/src/verify_diagram_flow.py --no-gf
```

Full publication gate, including the configured GF corroboration:

```bash
uv run python repro/src/run_publication_gate.py
```

The GF run is CPU-intensive. Existing raw GF outputs are retained under
`outputs/gf/` and `publish/outputs/gf/`; no GPU result is
claimed.

## Limitations

- Universal diagram-expansion and asymptotic statements are not established by
  finite symbolic grids, Monte Carlo, or reduced-scale simulations.
- GF corroboration uses reduced sizes, including `p=256` for `nu=2`
  and `p=32` for `nu=4`, versus larger paper settings.
- The `nu=4` transition has a documented finite-size preemption near the
  threshold.
- Historical `VERIFIED` labels in raw Trackio/Hugging Face artifacts
  describe finite checks only.
- The source archive and outputs are preserved for reproducibility; changing the
  arXiv source requires a new hash and audit.

## Branches

`main` is the canonical publication branch. The substantive historical
branches have been integrated into it:

| Historical branch | Role |
| --- | --- |
| `orx/symbolic-reconstruction-baseline` | Added the independent diagram calculus, symbolic checks, and six finite anchors. |
| `orx/gf-corroboration` | Added GF experiments, reduced-scale outputs, and the corrected ν=4 quadrature/threshold implementation. |

The branch cleanup retains the integrated code and deletes the historical remote
branches. See [BRANCH_AUDIT.md](BRANCH_AUDIT.md) for live verification.

## Repository map

- `repro/src/diagrams.py`: diagram operations and symbolic reconstruction.
- `repro/src/symbolic_checks.py`: six claim-level finite checks.
- `repro/src/gf_experiments.py`: optional numerical GF corroboration.
- `repro/src/verify_diagram_flow.py`: source-pinned verifier.
- `repro/src/run_publication_gate.py`: full gate runner.
- `outputs/`: raw verification and GF outputs.
- `publish/`: publication bundle and preserved historical pages.
- `reports/`: detailed finite audit report.
- `notebooks/`: explanatory tutorial.
- `source/`: pinned paper archive.
- `STATUS.md`, `GATE_READY.md`, and
  `BRANCH_AUDIT.md`: status, gate, and lineage.

## Citation

```bibtex
@article{yarotsky2026gradient,
  title   = {Gradient Flow Through Diagram Expansions: Learning Regimes and Explicit Solutions},
  author  = {Yarotsky, Dmitry and Golikov, Eugene and Gusev, Yaroslav},
  journal = {arXiv preprint arXiv:2602.04548},
  year    = {2026},
  url     = {https://arxiv.org/abs/2602.04548v2}
}
```

## Thank you and attribution

Thank you to Dmitry Yarotsky, Eugene Golikov, and Yaroslav Gusev for making this
mathematical work available for careful study and reproducibility analysis. This
repository is an independent finite audit, not an official implementation or
endorsement by the authors.

Maintained by [MachineLearning-Nerd](https://github.com/MachineLearning-Nerd).
