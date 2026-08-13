import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium", app_title="Gradient Flow Through Diagram Expansions")


@app.cell
def _():
    import marimo as marimo
    return (marimo,)


@app.cell
def _(marimo):
    marimo.md(
        """
        # Gradient Flow Through Diagram Expansions — the central claim

        Reproduction of Yarotsky, Golikov & Gusev (arXiv [2602.04548](https://arxiv.org/abs/2602.04548),
        OpenReview `BXE3Z0EHCs`).

        **Finite audit result.** For the symmetric rank-$H$ CP-decomposition of the
        identity matrix, the expected gradient-flow loss has the closed form
        $\\mathbb{E}[L(t)] \\sim p/2 + p^2\\sigma^2\\,\\Psi(-t/T, H/p, p\\sigma^2)$ (paper, Sec. 9),
        and it converges to $\\max((p-H)/2,\\,0)$. The figure below is the headline evidence from the
        reproduction: direct reduced-scale gradient-flow simulation (solid) vs the independently
        evaluated closed form (dashed), agreeing to <1% on the recorded cells. This is finite
        corroboration, not an independent proof of the limiting formula.
        """
    )
    return


@app.cell
def _(marimo):
    # The already-produced headline figure, fetched from the public HF Space
    # (no expensive re-run needed to see the result).
    marimo.image(
        src="https://huggingface.co/spaces/DineshAI/BXE3Z0EHCs/resolve/main/outputs/claim5_nu2.png",
        width=600,
    )
    return


@app.cell
def _(marimo):
    marimo.md(
        """
        ## Why the loss is a polynomial (Theorem 3.1)

        The loss-expansion coefficient $Y_s = T^s\\,\\mathbb{E}[d^sL/dt^s(0)]$ is a sum of
        **diagrams**: bipartite graphs ($H$-nodes, $p$-nodes, coloured edges = weights) paired by
        Wick's theorem. Each Wick-contracted diagram contributes a monomial $p^q H^n \\sigma^{2l}$,
        so $Y_s$ is a polynomial in $(H,p,\\sigma^2)$ by construction. Below we build the smallest
        example, $Y_0$ for SYM $\\nu=2$, by hand and check it against the paper's structure.
        """
    )
    return


@app.cell
def _():
    # Y_0 for SYM nu=2 = E[1/2 D_4 - R_2] = 1/2 sigma^4 (pH^2 + p^2 H + pH) - pH sigma^2
    # (reconstructed exactly by the from-scratch diagram engine in repro/src/diagrams.py).
    from fractions import Fraction

    Y0_sym_nu2_s0 = {
        (1, 2, 4): Fraction(1, 2),   # 1/2 p H^2 sigma^4
        (2, 1, 4): Fraction(1, 2),   # 1/2 p^2 H sigma^4
        (1, 1, 4): Fraction(1, 2),   # 1/2 p H sigma^4
        (1, 1, 2): Fraction(-1),     # - p H sigma^2
    }
    for (q, n, twol), c in sorted(Y0_sym_nu2_s0.items()):
        print(f"{str(c):>5} * p^{q} H^{n} sigma^{twol}")
    print("\nAll monomials are p^q H^n sigma^{2l} -> Y_0 is a polynomial in (H,p,sigma^2).",
          "This is Theorem 3.1, holding by construction of the Wick contraction.")
    return


@app.cell
def _(marimo):
    marimo.md(
        """
        ## The Narayana generating function (Sec. 9)

        The closed form uses $h(z,y)=\\frac{1-z(y+1)-\\sqrt{1-2z(y+1)+z^2(y-1)^2}}{2z^2}$, whose
        Taylor coefficients are the **Narayana numbers** $N(m{+}1,n)=\\frac{1}{m+1}\\binom{m+1}{n}\\binom{m+1}{n-1}$.
        """
    )
    return


@app.cell
def _():
    from math import comb


    def narayana(n, k):
        return comb(n, k) * comb(n, k - 1) // n


    # limit of E[L(t)] as t->inf: max((p-H)/2, 0)  -- the optimal rank-H approx of the identity
    for p, H in [(256, 128), (256, 256), (256, 512)]:
        print(f"p={p}, H={H}:  lim E[L] = max((p-H)/2,0) = {max((p-H)/2,0)}")
    return


@app.cell
def _(marimo):
    marimo.md(
        """
        ---
        **Verdict (finite audit):** all six source-pinned finite contracts pass. The consolidated
        paper-level status is **INCONCLUSIVE**: 0/6 claims are independently verified as theorems.
        Details:
        [report](https://github.com/MachineLearning-Nerd/icml26-repro-BXE3Z0EHCs-diagram-expansion-gradient-flow/blob/main/reports/diagram-expansion-gradient-flow/report.md)
        · [HF logbook](https://huggingface.co/spaces/DineshAI/BXE3Z0EHCs).
        Run locally: `uv run python repro/src/run_publication_gate.py`.
        """
    )
    return


if __name__ == "__main__":
    app.run()
