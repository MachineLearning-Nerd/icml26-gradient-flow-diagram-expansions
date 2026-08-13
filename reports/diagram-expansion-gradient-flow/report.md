# Gradient Flow Through Diagram Expansions — finite audit report

Paper: Dmitry Yarotsky, Eugene Golikov, and Yaroslav Gusev, “Gradient Flow
Through Diagram Expansions: Learning Regimes and Explicit Solutions,”
[arXiv:2602.04548v2](https://arxiv.org/abs/2602.04548v2),
OpenReview [BXE3Z0EHCs](https://openreview.net/forum?id=BXE3Z0EHCs).

## Consolidated result

- Finite contracts: **6/6 pass**.
- Paper-level claims independently verified: **0/6**.
- Overall: **INCONCLUSIVE**.

The raw verifier calls its finite producer results `VERIFIED`. Here that
means that the declared symbolic/numerical contract passed; it does not mean
that a universal theorem, large-size limit, or gradient-flow convergence claim
has been formally proved.

The source archive is pinned to
`6c470ad469118a8bd3b61f82b3456d95169c0581bce9284a0d68b13b8e37ca9b`.

## What is run

The canonical producer is `repro/src/verify_diagram_flow.py`. It:

1. verifies the source hash and selected theorem/equation anchors;
2. reconstructs and checks finite diagram/polynomial identities through
   `repro/src/diagrams.py` and `repro/src/symbolic_checks.py`;
3. compares selected symbolic expressions and finite Pareto fronts;
4. performs the declared NTK, scaling, `nu=2`, and `nu=4` checks; and
5. optionally runs reduced-scale gradient-flow corroboration from
   `repro/src/gf_experiments.py`.

The publication runner invokes the verifier and tests. The consolidated gate
separates finite contract status from paper-level status.

## Claim-by-claim ledger

| Claim | Paper object | Finite evidence producer | Result and boundary |
| --- | --- | --- | --- |
| C1 | Theorem 3.1 polynomiality | Reconstructed diagram/polynomial checks and Monte Carlo comparison; maximum recorded relative error about 0.0057. | Finite contract pass; not a universal polynomiality proof. |
| C2 | Theorem 4.1 Pareto terms | Computed fronts compared with the source formula over selected symmetric/asymmetric `nu` and order settings. | Finite contract pass; not the full theorem over all parameters. |
| C3 | NTK regime and Proposition 8.2 | Symbolic NTK/staticity identities plus optional GF drift corroboration. | Finite contract pass; not a complete regime-classification proof. |
| C4 | Mean-field scaling | Selected finite checks of `sigma^2 ~ 1/H` and `sigma^2 ~ 1/H^{2/nu}`. | Finite contract pass; not a universal asymptotic derivation. |
| C5 | Symmetric `nu=2` closed form | Narayana/limit symbolic checks and optional reduced-scale GF curve comparison. | Finite contract pass; not an independent proof of the limiting solution. |
| C6 | Symmetric `nu=4` threshold | Quadrature/erfc agreement about `1.0e-14`, `rho*` about 2.0778 for `theta=1`, and reduced-scale `p=32` GF bracketing. | Finite contract pass; finite-size effects and theorem limits remain. |

## Key finite observations

- The `nu=2` limiting-loss check evaluates
  `max((p-H)/2, 0)` on selected cells.
- The `nu=4` quadrature and closed form agree to approximately
  `1.027e-14` relative error at the recorded checks.
- The GF campaign is reduced-scale and corroborative. It is not a replacement
  for the paper’s mathematical proof.

## Reproduce

Fast symbolic path:

```bash
uv sync --frozen
uv run python repro/src/verify_diagram_flow.py --no-gf
```

Full configured gate:

```bash
uv run python repro/src/run_publication_gate.py
```

## Limitations

- Finite symbolic grids, Monte Carlo checks, and reduced-scale simulations do
  not establish universal or asymptotic statements.
- GF uses reduced sizes, including `p=256` for `nu=2` and `p=32`
  for `nu=4`; the paper studies larger settings.
- The `nu=4` transition has a documented finite-size preemption.
- The source archive contains paper materials but no author executable release;
  this repository is an independent audit.
- Raw Trackio/Hugging Face pages preserve historical `VERIFIED` wording
  as provenance; the canonical gate is the conservative result above.
