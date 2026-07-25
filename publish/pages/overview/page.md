# Overview

This logbook reproduces the six theorem/closed-form anchors of *Gradient Flow Through
Diagram Expansions* (arXiv:2602.04548) by **independent symbolic reconstruction** of the
paper's diagram calculus, Pareto-front analysis, NTK relations, nu=2 closed form, and nu=4
threshold, **corroborated by numerical gradient-flow simulation**.

**Why symbolic reconstruction?** The paper is a mathematical theory paper; its claims are
universally quantified statements about polynomials, Pareto fronts, and closed forms. The
non-circularity gate allows "an independently reconstructed symbolic derivation" as evidence.
We implement the diagram calculus (merge + Wick contraction) from scratch, derive the Y_s
polynomials, and verify their Pareto fronts match Theorem 4.1 *without feeding the formula in*.
The engine is independently checked against the raw loss/gradient definition by Monte-Carlo.

**Evidence chain:** source-pinned (SHA-256 of the arXiv tarball asserted) -> diagram engine
(exact rationals) -> Monte-Carlo validation (<0.6% relerr) -> closed-form verification
(Narayana g.f.; F via erfc cross-check at 1e-14) -> numerical GF corroboration.

**Experiment tree:** baseline `symbolic-reconstruction-baseline` (local, all 6 VERIFIED,
SHA `9ebb04c`) -> child `gf-corroboration` (HF cpu-upgrade, numerical GF).
