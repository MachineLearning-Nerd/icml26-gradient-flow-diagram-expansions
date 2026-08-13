# Status

- Paper: [arXiv:2602.04548v2](https://arxiv.org/abs/2602.04548v2), “Gradient
  Flow Through Diagram Expansions: Learning Regimes and Explicit Solutions,” by
  Dmitry Yarotsky, Eugene Golikov, and Yaroslav Gusev.
- OpenReview: [BXE3Z0EHCs](https://openreview.net/forum?id=BXE3Z0EHCs).
- Source archive: `source/arxiv-2602.04548.tar`, SHA-256
  `6c470ad469118a8bd3b61f82b3456d95169c0581bce9284a0d68b13b8e37ca9b`.
- Finite audit: 6/6 source-pinned symbolic/numerical contracts pass.
- Paper-level audit: 0/6 claims independently verified.
- Consolidated status: **INCONCLUSIVE**.
- Producers: `repro/src/verify_diagram_flow.py`,
  `repro/src/symbolic_checks.py`, and optional
  `repro/src/gf_experiments.py`.
- Canonical branch: `main`; historical branch roles are recorded in
  [BRANCH_AUDIT.md](BRANCH_AUDIT.md).
- Maintainer identity: MachineLearning-Nerd.
- Evidence boundary: raw `VERIFIED` means finite contract pass; it
  does not prove universal diagram-expansion or gradient-flow theorems.

The repository is ready as a finite symbolic/GF audit, not as a formal proof
of the paper’s claims.
