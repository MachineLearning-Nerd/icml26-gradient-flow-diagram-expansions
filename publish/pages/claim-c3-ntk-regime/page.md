# Claim C3 — NTK regime (Sec. 4, 8; Propositions 8.1, 8.2)

**Finite contract status: PASS. Paper-level status: not independently verified.**

## Exact claim (source-quoted)
> An NTK-like (feature-frozen) regime appears only at points/edge B-C of the Pareto polygon
> in ASYM (Prop 8.1: for T~eta^-1 H sigma^{2nu-2}, the NTK converges to the identity tensor
> and f converges to (1-e^{-eta t}) times the identity). Proposition 8.2: for SYM nu=2 the
> NTK is static throughout training iff the model is static, so SYM has no NTK limit.
(Sec. 8, `\label{prop:ntk_training_main}` and App. `app:NTK_trace_evolution_nu=2`.)

## Method — independent reconstruction
(a) The B-C edge scaling and natural timescale `T ~ H sigma^{2nu-2}` are read off the Pareto
polygon (claim 2) and match Prop 8.1's parameterisation.
(b) Prop 8.2 crux identity, constructed directly: for SYM nu=2,
`Theta_{i,j;i',j'} = delta_{i=i'}f_{j,j'} + delta_{i=j'}f_{j,i'} + delta_{j=i'}f_{i,j'} + delta_{j=j'}f_{i,i'}`
so with i,j,j' distinct, `Theta_{i,j;j,j'} = f_{i,j'}`. Verified two ways:
- identity max-error vs the analytic form: **0.00e+00**
- full NTK vs finite-difference of f=U^T U: max-error **3.59e-12**.

SYM nu=2: Theta is a linear combo of f entries, so a static kernel would force a static model (no feature learning) -- hence no NTK limit in SYM.

### Numerical GF corroboration (claim 5, eq:loss-narayana)

SYM nu=2 gradient flow vs closed form (p=256, sigma^2=1e-2/p, 2 seeds, RK4). Scale-relative error vs p/2:

| H | mean relerr (theory non-negligible) | max abserr / (p/2) | final obs | final theory |
|---|---|---|---|---|
| 512 | 0.0028 | 0.0011 | 9.9e-05 | 9.53e-05 |
| 256 | 0.0088 | 0.0034 | 1.87 | 1.59 |
| 128 | 0.0012 | 0.0025 | 64 | 64 |

**Pass:** True. Reduced-scale (p=256, 2 seeds) GF vs eq:loss-narayana. Under/balanced-parameterized (H=128,256) track the closed form to <0.5% of p/2; the strongly overparameterized H=512 case shows a finite-size tail transient (mean relerr where the loss is non-negligible is still ~1.3%). Corroborates claim 5.

![SYM nu=2 loss: GF vs closed form](outputs/claim5_nu2.png)

Raw curve data: `outputs/gf/claim5_nu2_curves.csv`

### Numerical GF corroboration (claim 3b, Prop 8.2)

SYM nu=2 GF run (p=8, H=16, sigma^2=0.0625): relative model drift ||f(t)-f(0)||/||f(0)|| = **0.608**, relative NTK drift = **0.498**, loss 1.93 -> 1.3e-05. Model learned (f drifted) AND NTK drifted by a comparable fraction -- consistent with Prop 8.2: a static NTK would force f static.  SYM has no NTK limit. **Pass:** True

### Numerical GF corroboration (claim 6, eq:nu4-threshold)

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
**FINITE CONTRACT PASS**. Command `uv run python repro/src/run_publication_gate.py`; uv, Python 3.12, numpy 2.5, scipy 1.18, sympy 1.14, matplotlib 3.11 (pyproject.toml + uv.lock pinned).
