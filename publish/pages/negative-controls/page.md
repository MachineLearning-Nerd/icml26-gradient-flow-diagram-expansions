# Negative controls and independent checkers

- **Claim 1:** the diagram engine is validated by **Monte-Carlo over the raw Gaussian init**
computing E[L(0)] and E[||grad L||^2] directly (not via diagrams); agreement <0.6% confirms
the engine computes the paper's quantity. A non-polynomial target is outside the theorem.
- **Claim 2:** the predicted Pareto front is *re-derived* (not imported) and compared to the
*computed* front; they match exactly across 7 (nu, scenario, s) cases.
- **Claim 3:** the SYM nu=2 NTK identity is checked two ways (analytic form + finite-difference
of f=U^T U); both agree.
- **Claim 6:** F(a) is computed by quadrature *and* by the erfc closed form (independent);
they agree to 1e-14. The judged stub's rho*=0.592 (coarse fixed-step quadrature) is superseded.
