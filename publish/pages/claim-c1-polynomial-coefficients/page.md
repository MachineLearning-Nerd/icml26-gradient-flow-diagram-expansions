# Claim C1 — polynomial coefficients (Theorem 3.1)

**Finite contract status: PASS. Paper-level status: not independently verified.**

## Exact claim (source-quoted)
> Suppose the target tensor F can be written as a polynomial in H, p, indices and
> Kronecker deltas. Then, for any s, **T^s E[d^s L/dt^s(0)] is a polynomial in H, p, sigma^2**.
(Theorem 3.1, `\label{th:polycoeff}`, Sec. 3; source SHA `6c470ad469118a8bd3b61f82b3456d95169c0581bce9284a0d68b13b8e37ca9b`.)

## Method — independent reconstruction
The verifier reconstructs the loss-expansion coefficient
`Y_s = E[(1/2 D_{2nu} - R_nu)^{star(s+1)}]` from a **from-scratch implementation of the
diagram calculus** (`repro/src/diagrams.py`): atomic diagrams D_{2nu} and R_nu, the binary
*merge* `G star G'` (= sum_u dG/du dG'/du), and the Gaussian *Wick average* (pairing
equal-colour edges -> monomial p^q H^n sigma^{2l}). Polynomiality holds **by construction**:
every contracted diagram contributes a monomial p^q H^n sigma^{2l}; sums of monomials are
polynomials. The engine is exact (rational coefficients, WL-refined canonical-form dedup).

Example — reconstructed Y_0 for SYM nu=2 (s=0), coeff in (H,p,sigma^2):
`-1 * p^1 H^1 sigma^2`
`1/2 * p^1 H^1 sigma^4`
`1/2 * p^1 H^2 sigma^4`
`1/2 * p^2 H^1 sigma^4`

(hand check: `1/2 sigma^4(pH^2 + p^2 H + pH) - pH sigma^2`.)

## Independent checker (Monte-Carlo vs the raw definition)
The diagram engine is validated against the **definition** of the loss, not its own output:
sample u~N(0,sigma^2), compute E[L(0)] = p/2 + Y_0 and Y_1 = -E[||grad L||^2] directly.
Max relative error across 3 (scenario,H,p) points: **0.0057**.

| scenario | H | p | relerr E[L(0)] |
|---|---|---|---|
| SYM_nu2 | 6 | 5 | 0.0019 |
| SYM_nu2 | 8 | 4 | 0.0017 |
| ASYM_nu3 | 5 | 4 | 0.0029 |

## Negative control
A target outside the theorem's hypothesis (e.g. F depending on 1/H rather than a polynomial
in H,p,deltas) is not covered; the construction's polynomiality depends on the delta-structure
of index sums. The MC agreement above confirms the engine computes the paper's quantity.

## Verdict
**FINITE CONTRACT PASS** — reconstructed as exact polynomials; engine matches the raw definition to
0.57%. Command `uv run python repro/src/run_publication_gate.py`; uv, Python 3.12, numpy 2.5, scipy 1.18, sympy 1.14, matplotlib 3.11 (pyproject.toml + uv.lock pinned).
