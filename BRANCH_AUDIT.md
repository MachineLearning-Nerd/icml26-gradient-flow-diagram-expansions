# Branch audit

## Canonical surface

`main` is the canonical publication branch. The substantive evidence
from the historical branches was integrated into `main` before cleanup.

| Historical branch | Integrated role |
| --- | --- |
| `orx/symbolic-reconstruction-baseline` | Independent diagram calculus, symbolic checks, and six finite anchors. |
| `orx/gf-corroboration` | Numerical gradient-flow corroboration and corrected ν=4 threshold integration. |

These branches are development lineage, not separate scientific results. Their
raw `VERIFIED` labels are finite producer labels only.

## Publication-time checks

Checked on 2026-08-13:

- Repository target: `icml26-gradient-flow-diagram-expansions`.
- Default and only remote branch after cleanup: `main`.
- Maintainer identity: MachineLearning-Nerd.
- Paper record: arXiv:2602.04548v2, OpenReview: BXE3Z0EHCs.
- Consolidated result: 6/6 finite contracts pass; 0/6 paper claims independently
  verified; overall INCONCLUSIVE.

## Live verification

Verified on 2026-08-13 after integration, repository rename, and branch cleanup:

- Repository name: `icml26-gradient-flow-diagram-expansions`.
- Default and only remote branch: `main`.
- Repository homepage: https://arxiv.org/abs/2602.04548v2.
- Reachable history: all retained commits use MachineLearning-Nerd with the
  requested no-reply address.
- Local branch state: `main` tracks `origin/main`; both
  historical `orx/*` branches are removed from the remote.
