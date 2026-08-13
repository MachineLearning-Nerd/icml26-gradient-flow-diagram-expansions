# Claim C4 — mean-field init-variance scaling (Sec. 4)

**Finite contract status: PASS. Paper-level status: not independently verified.**

## Exact claim (source-quoted)
> Mean-field (feature-evolving) regimes require sigma^2 ~ 1/H (symmetric case, edge B-E) or
> sigma^2 ~ 1/H^{2/nu} (asymmetric case, edge C-D). (Sec. 4; for nu=2 these coincide.)
(source SHA `6c470ad469118a8bd3b61f82b3456d95169c0581bce9284a0d68b13b8e37ca9b`; App. `sec:hyperparameter_polygon_detailed`.)

## Method — derived from the Pareto-front dominance conditions
- SYM B-E dominance `p^{nu-2} H^2 sigma^{2nu} ~ 1`  =>  sigma^2 ~ H^{-2/nu} p^{-(nu-2)/nu};
  at nu=2 this is **sigma^2 ~ 1/H**.
- ASYM C-D dominance `H sigma^nu ~ 1`  =>  **sigma^2 ~ H^{-2/nu}**.

| regime | dominance | sigma^2 | H-exponent |
|---|---|---|---|
| SYM nu=2 (edge B-E) | p^{nu-2} H^2 sigma^{2nu} ~ 1 | 1/H | -1 |
| SYM nu=4 (edge B-E) | p^{nu-2} H^2 sigma^{2nu} ~ 1 | 1/(sqrt(H)*sqrt(p)) | (-log(H) - log(p))/(2*log(H)) |
| SYM nu=6 (edge B-E) | p^{nu-2} H^2 sigma^{2nu} ~ 1 | 1/(H**(1/3)*p**(2/3)) | (-log(H) - 2*log(p))/(3*log(H)) |
| ASYM nu=2 (edge C-D) | H sigma^nu ~ 1 | 1/H | -1 |
| ASYM nu=3 (edge C-D) | H sigma^nu ~ 1 | H**(-2/3) | -2/3 |
| ASYM nu=4 (edge C-D) | H sigma^nu ~ 1 | 1/sqrt(H) | -1/2 |

## Verdict
**FINITE CONTRACT PASS** — SYM nu=2 gives sigma^2 ~ 1/H; ASYM gives sigma^2 ~ 1/H^{2/nu} for nu=2,3,4.
Command `uv run python repro/src/run_publication_gate.py`; uv, Python 3.12, numpy 2.5, scipy 1.18, sympy 1.14, matplotlib 3.11 (pyproject.toml + uv.lock pinned).
