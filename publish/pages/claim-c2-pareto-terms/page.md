# Claim C2 — Pareto-optimal terms (Theorem 4.1)

**Finite contract status: PASS. Paper-level status: not independently verified.**

## Exact claim (source-quoted)
> Up to nonzero numerical coefficients, the Pareto-optimal terms in Y_s are
> `p^{Q(n,sD)} H^n sigma^{nu(sD+1)+(nu-2)s}`, `0<=sD<=s+1`, `1<=n<=sD+1`, with
> `Q(n,sD)=1+(nu-1)sD - (nu/2)(n-1)` (SYM, even nu) or `1+(nu-1)(sD+1-n)` (ASYM);
> ASYM additionally omits odd-s_R terms and the (n,sD)=(s+2,s+1) term.
(Theorem 4.1, `\label{th:pareto_front}`, Sec. 4; source SHA `6c470ad469118a8bd3b61f82b3456d95169c0581bce9284a0d68b13b8e37ca9b`.)

## Method — independent reconstruction
From the **computed** Y_s polynomials (claim 1 engine) the verifier extracts every monomial,
takes the Pareto-optimal subset (max (q,n) at fixed sigma-power, Sec. 4 definition) and
compares it to the theorem's formula — *no theorem formula is fed in*: the formula is
re-derived as `predicted_pareto_terms` and checked against the independently *computed* front.

## Result
| nu | scenario | s | computed front size | predicted size | exact match |
|---|---|---|---|---|---|
| 2 | SYM | 1 | 6 | 6 | True |
| 2 | SYM | 2 | 10 | 10 | True |
| 4 | SYM | 1 | 6 | 6 | True |
| 3 | ASYM | 1 | 3 | 3 | True |
| 3 | ASYM | 2 | 5 | 5 | True |
| 4 | ASYM | 1 | 3 | 3 | True |
| 2 | ASYM | 2 | 5 | 5 | True |

**All 7 cases match exactly** (`all_match: True`).

## Verdict
**FINITE CONTRACT PASS**. Command `uv run python repro/src/run_publication_gate.py`; uv, Python 3.12, numpy 2.5, scipy 1.18, sympy 1.14, matplotlib 3.11 (pyproject.toml + uv.lock pinned).
