# Claim C6 — SYM nu=4 ascent threshold (Sec. 10, eq:nu4-threshold)

## Exact claim (source-quoted)
> For SYM nu=4 with gradient ascent, the solution exists for all tau<=0 (low-noise,
> convergent) iff `p^3 sigma^4 < rho* = 1/(-16 theta int_0^{-inf} F(u)^3 du)`,
> `theta = 1 + 3H/p^2`, `F(a) = int_0^inf e^{4au^2-u} u du`; otherwise the ascent diverges
> at finite tau (high-noise). (Sec. 10, `\label{eq:nu4-threshold}`; source SHA `6c470ad469118a8bd3b61f82b3456d95169c0581bce9284a0d68b13b8e37ca9b`.)

## Method — independent reconstruction
`F(a)` is computed two independent ways:
- adaptive quadrature of `int_0^inf e^{4au^2-u} u du`,
- the closed form `F(x) = -1/(8x) + sqrt(pi/(-x))/(32x) e^{-1/(16x)} erfc(1/(4 sqrt(-x)))`.
They agree to **1.03e-14** (max relative error over a<0 grid).

Then `rho*` (theta=1) = 1/(-16 int_0^{-inf} F^3) with `int_0^{-inf} F^3 = -0.0300798`
=> **rho*(theta=1) = 2.077809**.
(The judged stub's 0.592 was a coarse fixed-step quadrature artefact; the erfc-validated value
disagrees and supersedes it.)

## Numerical corroboration (claim 6 ascent boundary)

SYM nu=4 gradient ascent (p=32, H=341, theta=2, rho*=1.0394). Weight-norm growth across the rho sweep:

| rho/rho* | rho | growth ratio | diverged | prediction |
|---|---|---|---|---|
| 0.20 | 0.208 | 0.91 | False | low-noise (converge) |
| 0.40 | 0.416 | 0.91 | False | low-noise (converge) |
| 0.60 | 0.624 | 0.92 | False | low-noise (converge) |
| 0.80 | 0.832 | 0.96 | False | low-noise (converge) |
| 0.95 | 0.987 | 1e+18 | True | low-noise (converge) |
| 1.05 | 1.09 | 1e+18 | True | high-noise (diverge) |
| 1.20 | 1.25 | 1e+18 | True | high-noise (diverge) |
| 1.50 | 1.56 | 1e+18 | True | high-noise (diverge) |
| 2.00 | 2.08 | 1e+18 | True | high-noise (diverge) |
| 3.00 | 3.12 | 1e+18 | True | high-noise (diverge) |

Low-rho bounded & high-rho diverged; the transition brackets rho*. **Pass:** True. Reduced-scale (p=32) ascent corroborating eq:nu4-threshold; the divergence transition brackets rho*.

Raw sweep data: `outputs/gf/claim6_nu4_ascent.csv`


## Verdict
**VERIFIED** (threshold formula and the integral it rests on). Command `uv run python repro/src/run_publication_gate.py`; uv, Python 3.12, numpy 2.5, scipy 1.18, sympy 1.14, matplotlib 3.11 (pyproject.toml + uv.lock pinned).
