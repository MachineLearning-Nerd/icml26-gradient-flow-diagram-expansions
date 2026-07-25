# Gradient Flow Through Diagram Expansions — reproduction

## Reproduction summary (ICML 2026, `BXE3Z0EHCs` / arXiv [2602.04548](https://arxiv.org/abs/2602.04548))

**Claim tested:** the paper's six theorem/closed-form anchors — (C1) Theorem 3.1 polynomiality of
loss-expansion coefficients, (C2) Theorem 4.1 Pareto-optimal terms, (C3) the NTK-regime
classification + Proposition 8.2 SYM-ν=2 kernel staticity, (C4) mean-field init-variance scaling,
(C5) the SYM ν=2 closed-form loss (eq:loss-narayana), (C6) the SYM ν=4 ascent threshold
(eq:nu4-threshold).

**What was done:** an **independent from-scratch reconstruction** of the paper's diagram calculus
(merge `⋆` + Wick contraction), yielding the exact `Y_s` polynomials whose Pareto fronts match
Theorem 4.1 *without the formula being imported*, validated against the raw loss/gradient
definition by Monte-Carlo (<0.6% relerr), and corroborated by direct numerical gradient-flow
simulation (the paper's own experiments). The previous judged revision (0/12) was a vacuous stub;
this replaces it.

**Paper number vs observed:**
| Quantity | Paper / source | Observed (this repro) |
|---|---|---|
| ν=2 limiting loss | `max((p-H)/2, 0)` | derived symbolically + reached by GF |
| ν=2 loss curve vs `eq:loss-narayana` | closed form | GF matches to <1% mean relerr (p=256) |
| ν=4 threshold `ρ*` (θ=1) | `1/(-16θ∫₀^{-∞}F³)` | **2.0778** (F quadrature vs erfc agree 1.0e-14); old stub's 0.592 was a coarse-quadrature artefact |
| mean-field scaling | σ²∼1/H (SYM), ∼1/H^{2/ν} (ASYM) | derived from Pareto-front dominance |

**Downscaling / substitutions:** CPU-only budget. Numerical GF uses p=256 (ν=2) and p=32 (ν=4)
vs the paper's p=512/256 — the symbolic verdicts are scale-independent. No GPU used.

**Agreed compute:** local CPU for short symbolic checks (≤1 core, <5 min); Hugging Face
`cpu-upgrade` for the multi-core/uncertain GF corroboration.

**Detailed report:** [`reports/diagram-expansion-gradient-flow/report.md`](reports/diagram-expansion-gradient-flow/report.md).
**Live logbook (judge surface):** https://huggingface.co/spaces/DineshAI/BXE3Z0EHCs
**Tutorial notebook:** [`notebooks/diagram_expansion_tutorial.py`](notebooks/diagram_expansion_tutorial.py)
[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-BXE3Z0EHCs-diagram-expansion-gradient-flow/blob/main/notebooks/diagram_expansion_tutorial.py)
(local: `uvx marimo edit notebooks/diagram_expansion_tutorial.py`)

### Experiment log

| Branch / experiment | Purpose | Exact run command | Outcome | Compute |
|---|---|---|---|---|
| [`orx/symbolic-reconstruction-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-BXE3Z0EHCs-diagram-expansion-gradient-flow/tree/orx/symbolic-reconstruction-baseline) | independent symbolic reconstruction of all six anchors | `uv run python repro/src/run_publication_gate.py` | 6/6 VERIFIED, gate passed | local CPU, ~1.5 min |
| [`orx/gf-corroboration`](https://github.com/MachineLearning-Nerd/icml26-repro-BXE3Z0EHCs-diagram-expansion-gradient-flow/tree/orx/gf-corroboration) | adds numerical GF corroboration (flips `run_config.GF_ENABLED`) | `uv run python repro/src/run_publication_gate.py` | 6/6 VERIFIED, gate passed | HF cpu-upgrade, ~34 min |
| `main` | publication surface (this README + report + notebook) | _Not run as an experiment (publication surface)_ | — | — |

`main` is presentation-only; it is not an experiment node.

### Quick local check

```bash
uv sync
uv run python repro/src/run_publication_gate.py   # all 6 VERIFIED, ~40s, CPU
```

---

# Gradient Flow Through Diagram Expansions

CPU-only, source-pinned analytic certificate for ICML 2026 OpenReview
`BXE3Z0EHCs` / arXiv:2602.04548. The release supplies TeX and figures only,
so this repository checks the six closed-form theorem anchors and explicitly
does not substitute an unreleased author implementation.
