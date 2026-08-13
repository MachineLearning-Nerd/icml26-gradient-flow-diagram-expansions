# Publication gate

This repository is gate-ready as a finite symbolic and gradient-flow audit.

- Finite contracts: 6/6 pass.
- Paper-level claims independently verified: 0/6.
- Overall status: **INCONCLUSIVE**.
- Gate output: [publication_gate.json](publication_gate.json).
- Raw output: [outputs/verification.json](outputs/verification.json).

Fast symbolic check:

```bash
uv sync --frozen
uv run python repro/src/verify_diagram_flow.py --no-gf
```

Full gate:

```bash
uv run python repro/src/run_publication_gate.py
```

The gate checks finite source anchors, symbolic identities, selected numerical
comparisons, and optional reduced-scale GF corroboration. It does not establish
the paper’s universal or asymptotic claims.
