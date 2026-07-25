"""Numerical gradient-flow experiments corroborating claims 3 (NTK staticity),
5 (SYM nu=2 closed form, eq:loss-narayana) and 6 (SYM nu=4 ascent threshold,
eq:nu4-threshold) of arXiv:2602.04548.

These reproduce the paper's own experimental figures (Figs. nu2-sym-gen and
nu4-ascent) by direct simulation of the model gradient flow, and compare against
the closed forms validated symbolically in ``symbolic_checks.py``.  They are
corroborating evidence; the rigorous claim verdicts rest on the independent
symbolic reconstruction.

Heavy work: intended to run on a multi-core CPU flavour (see orx-compute skill).
"""

from __future__ import annotations
import math
import os
from typing import Tuple

import numpy as np


# ---------------------------------------------------------------------------
# SYM nu=2 closed-form loss (eq:loss-narayana / eq:PhiABEfinal1)
# ---------------------------------------------------------------------------
def _narayana(n, k):
    if not (1 <= k <= n):
        return 0
    return math.comb(n, k) * math.comb(n, k - 1) // n


# Precompute series coefficients of h(z,y) = sum_m c_m(y) z^m up to order M,
# where c_m(y) = sum_{n=1}^{m+1} N(m+1, n) y^n.  Used to stabilise h, h_z near
# z=0 where the closed form suffers catastrophic cancellation.
_MSER = 9
_SER_C = [[_narayana(m + 1, n) for n in range(1, m + 2)] for m in range(_MSER + 1)]


def _h_series(z, y, deriv=0):
    """Series approx of h (deriv=0) or dh/dz (deriv=1) at small |z|."""
    out = 0.0
    if deriv == 0:
        for m in range(_MSER + 1):
            term = sum(c * y ** n for n, c in enumerate(_SER_C[m], start=1))
            out += term * z ** m
    else:
        for m in range(1, _MSER + 1):
            term = sum(c * y ** n for n, c in enumerate(_SER_C[m], start=1))
            out += m * term * z ** (m - 1)
    return out


def _h(z, y):
    z = np.asarray(z, dtype=float)
    closed = (1 - z * (y + 1) - np.sqrt(1 - 2 * z * (y + 1) + z ** 2 * (y - 1) ** 2)) / (2 * z ** 2 + 1e-300)
    out = np.where(np.abs(z) < 0.2, _h_series(z, y, 0), closed)
    return out


def _h_z(z, y):
    z = np.asarray(z, dtype=float)
    s = np.sqrt(1 - 2 * z * (y + 1) + z ** 2 * (y - 1) ** 2)
    sp = (-(y + 1) + z * (y - 1) ** 2) / s
    num = (-(y + 1) - sp) * 2 * z ** 2 - (1 - z * (y + 1) - s) * 4 * z
    closed = num / (4 * z ** 4)
    out = np.where(np.abs(z) < 0.2, _h_series(z, y, 1), closed)
    return out


def psi_nu2(x, y, z):
    """Psi(x,y,z) = (z e^{-8x}/2) h_1(z(1-e^{-4x}),y) - e^{-4x} h(z(1-e^{-4x}),y)."""
    e4 = np.exp(-4 * x)
    arg = z * (1 - e4)
    return (z * np.exp(-8 * x) / 2.0) * _h_z(arg, y) - e4 * _h(arg, y)


def theory_loss_nu2(t, p, H, T, sigma2):
    """E[L(t)] ~ p/2 + p^2 sigma^2 Psi(-t/T, H/p, p sigma^2)."""
    x = -np.asarray(t, dtype=float) / T
    return p / 2.0 + p ** 2 * sigma2 * psi_nu2(x, H / p, p * sigma2)


# ---------------------------------------------------------------------------
# SYM nu=2 gradient flow:  du/dt = -(2/T) U (U^T U - I)
# ---------------------------------------------------------------------------
def sym_nu2_run(p: int, H: int, sigma2: float, T: float, t_max: float,
                n_steps: int, seed: int) -> Tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    U = rng.normal(0.0, math.sqrt(sigma2), size=(H, p))
    I = np.eye(p)
    dt = t_max / n_steps
    t_arr = np.linspace(0.0, t_max, n_steps + 1)
    L = np.empty(n_steps + 1)
    M = U.T @ U - I
    L[0] = 0.5 * float(np.sum(M * M))

    def grad(U):
        return (2.0 / T) * (U @ (U.T @ U - I))

    for i in range(1, n_steps + 1):
        # RK4
        k1 = -grad(U)
        k2 = -grad(U + 0.5 * dt * k1)
        k3 = -grad(U + 0.5 * dt * k2)
        k4 = -grad(U + dt * k3)
        U = U + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        M = U.T @ U - I
        L[i] = 0.5 * float(np.sum(M * M))
    return t_arr, L


def ntk_sym_nu2(U: np.ndarray, p: int, eps: float = 1e-4) -> np.ndarray:
    """Full NTK Theta_{ij;i'j'} for SYM nu=2 by finite differences of f=U^T U."""
    H = U.shape[0]
    Th = np.zeros((p, p, p, p))
    base = U.T @ U
    for k in range(H):
        for a in range(p):
            Up = U.copy(); Up[k, a] += eps
            Um = U.copy(); Um[k, a] -= eps
            d = ((Up.T @ Up) - (Um.T @ Um)) / (2 * eps)
            Th += np.einsum("ij,kl->ijkl", d, d)
    return Th


# ---------------------------------------------------------------------------
# SYM nu=4 gradient ascent:  du/dtau = +(1/T) dL/du  with
#   L = 1/2 sum_{kk'} G_{kk'}^4 - sum_{ki} u_{ki}^4 + p/2,  G = U U^T
#   dL/du = 4 (G^{\circ 3}) U - 4 U^{\circ 3}
# ---------------------------------------------------------------------------
def sym_nu4_ascent(p: int, H: int, sigma2: float, T: float, tau_max: float,
                    n_steps: int, seed: int, track_every: int = 5):
    rng = np.random.default_rng(seed)
    U = rng.normal(0.0, math.sqrt(sigma2), size=(H, p))
    dtau = tau_max / n_steps

    def Lnorm(U):
        G = U @ U.T
        return 0.5 * float(np.sum(G ** 4)) - float(np.sum(U ** 4)) + 0.5 * p

    def grad(U):
        G = U @ U.T
        return 4.0 * (G ** 3) @ U - 4.0 * (U ** 3)

    taus = [0.0]; vals = [Lnorm(U)]; unorm = [float(np.sum(U ** 2))]
    blown = False
    for i in range(1, n_steps + 1):
        # ascent: + grad (increase L); clip if exploding
        g = grad(U)
        U = U + dtau * g / T
        if not np.all(np.isfinite(U)) or float(np.max(np.abs(U))) > 1e8:
            blown = True
            taus.append(i * dtau); vals.append(float("inf")); unorm.append(float("inf"))
            break
        if i % track_every == 0:
            taus.append(i * dtau); vals.append(Lnorm(U)); unorm.append(float(np.sum(U ** 2)))
    return np.array(taus), np.array(vals), np.array(unorm), blown


def claim5_numerical(outdir: str) -> dict:
    """SYM nu=2: compare simulated E[L(t)] to the closed form (Fig. nu2-sym-gen).
    Setup matches the paper: p=512, sigma^2=1e-2/p, H in {1024,512,256}, T=1."""
    os.makedirs(outdir, exist_ok=True)
    p = 512
    sigma2 = 1e-2 / p
    T = 1.0
    t_max = 3.0
    n_steps = 300
    seeds = list(range(3))
    rows = []
    curves = {}
    for H in (1024, 512, 256):
        Ls = np.zeros(n_steps + 1)
        for sd in seeds:
            t_arr, L = sym_nu2_run(p, H, sigma2, T, t_max, n_steps, sd)
            Ls += L
        Ls /= len(seeds)
        th = theory_loss_nu2(t_arr, p, H, T, sigma2)
        curves[H] = (t_arr, Ls, th)
        rel = np.abs(Ls - th) / (np.abs(th) + 1e-9)
        rows.append({"H": H, "p": p, "sigma2": sigma2,
                     "mean_relerr": float(np.mean(rel)),
                     "max_relerr": float(np.max(rel[1:])),   # drop t=0 singular
                     "final_obs": float(Ls[-1]), "final_theory": float(th[-1])})
    # save CSV
    import csv
    with open(os.path.join(outdir, "claim5_nu2_curves.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t", "H", "observed_EL", "theory_EL"])
        for H in (1024, 512, 256):
            t, Ls, th = curves[H]
            for tt, oo, ee in zip(t, Ls, th):
                w.writerow([tt, H, oo, ee])
    # figure
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 4))
        for H in (1024, 512, 256):
            t, Ls, th = curves[H]
            ax.plot(t, Ls / (p / 2), "-", label=f"GF p={p}, H={H}")
            ax.plot(t, th / (p / 2), "k--", alpha=0.5)
        ax.set_xlabel("t"); ax.set_ylabel("E[L(t)] / (p/2)")
        ax.set_title("SYM nu=2: GF simulation vs closed form (dashed=theory)")
        ax.legend(); ax.grid(alpha=0.3)
        fig.tight_layout(); fig.savefig(os.path.join(outdir, "claim5_nu2.png"), dpi=110)
        plt.close(fig)
    except Exception as e:
        rows.append({"figure_error": str(e)})
    maxerr = max(r.get("max_relerr", 0) for r in rows)
    return {"rows": rows, "max_relerr": maxerr,
            "pass": maxerr < 0.12,
            "note": "Reduced-seed (3) GF vs eq:loss-narayana; agreement corroborates claim 5."}


def claim3b_numerical(outdir: str) -> dict:
    """SYM nu=2 NTK evolution: during learning the kernel is NOT static
    (Prop 8.2 => static Theta would force a static model).  We run GF and
    measure ||Theta(t_end)-Theta(0)|| / ||Theta(0)|| on a small p where the full
    NTK is affordable, showing it is large whenever the model learns."""
    os.makedirs(outdir, exist_ok=True)
    p = 8
    H = 16
    sigma2 = 1.0 / H              # mean-field scaling sigma^2 ~ 1/H (claim 4)
    T = 1.0
    t_max = 2.0
    n_steps = 200
    seed = 0
    rng = np.random.default_rng(seed)
    U0 = rng.normal(0.0, math.sqrt(sigma2), size=(H, p))
    Th0 = ntk_sym_nu2(U0, p)
    # integrate GF
    U = U0.copy()
    dt = t_max / n_steps

    def grad(U):
        return (2.0 / T) * (U @ (U.T @ U - np.eye(p)))

    for i in range(n_steps):
        k1 = -grad(U); k2 = -grad(U + 0.5 * dt * k1)
        k3 = -grad(U + 0.5 * dt * k2); k4 = -grad(U + dt * k3)
        U = U + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    Th1 = ntk_sym_nu2(U, p)
    f0 = U0.T @ U0; f1 = U.T @ U
    dmodel = float(np.linalg.norm(f1 - f0)) / (float(np.linalg.norm(f0)) + 1e-12)
    dntk = float(np.linalg.norm(Th1 - Th0)) / (float(np.linalg.norm(Th0)) + 1e-12)
    L0 = 0.5 * float(np.sum((f0 - np.eye(p)) ** 2))
    L1 = 0.5 * float(np.sum((f1 - np.eye(p)) ** 2))
    return {"p": p, "H": H, "sigma2": sigma2,
            "rel_drift_model_f": dmodel, "rel_drift_NTK": dntk,
            "L0": L0, "L1": L1, "learned": L1 < L0,
            "interpretation": "Model learned (f drifted) AND NTK drifted by a "
                              "comparable fraction -- consistent with Prop 8.2: a "
                              "static NTK would force f static.  SYM has no NTK limit.",
            "pass": dmodel > 0.05 and dntk > 0.05 and L1 < L0}


def claim6_numerical(outdir: str) -> dict:
    """SYM nu=4 gradient ascent divergence boundary (Fig. nu4-ascent).
    For theta=1+3H/p^2 and rho=p^3 sigma^4, theory (eq:nu4-threshold) predicts
    convergence below rho* = 1/(-16 theta int_0^{-inf} F^3) and divergence above.
    We run ascent at several rho straddling rho* and report which blow up."""
    import csv
    import symbolic_checks as sc
    os.makedirs(outdir, exist_ok=True)
    val, _ = None, None
    from scipy.integrate import quad
    integ, _ = quad(lambda u: sc.F_erfc(u) ** 3, -np.inf, 0, limit=400)
    integ = -integ  # int_0^{-inf} F^3
    p = 32
    H = int(round(p ** 2 / 3))      # => theta = 1 + 3H/p^2 = 1 + 1 = 2
    theta = 1 + 3 * H / p ** 2
    rho_star = 1.0 / (-16.0 * theta * integ)
    T = 1.0
    tau_max = 0.5
    n_steps = 400
    seeds = [0, 1]
    rho_factors = [0.3, 0.6, 0.9, 1.0, 1.1, 1.4, 2.0]
    rows = []
    for rf in rho_factors:
        rho = rf * rho_star
        sigma2 = (rho / (p ** 3)) ** 0.5     # rho = p^3 sigma^4 => sigma2 = sqrt(rho/p^3)
        blown_any = False
        for sd in seeds:
            _, _, _, blown = sym_nu4_ascent(p, H, sigma2, T, tau_max, n_steps, sd)
            blown_any = blown_any or blown
        rows.append({"rho_factor": rf, "rho": rho, "sigma2": sigma2,
                     "theta": theta, "diverged": bool(blown_any),
                     "prediction": "high-noise (diverge)" if rf > 1.0
                     else "low-noise (converge)"})
    with open(os.path.join(outdir, "claim6_nu4_ascent.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["rho_factor", "rho", "sigma2", "theta", "diverged"])
        for r in rows:
            w.writerow([r["rho_factor"], r["rho"], r["sigma2"], r["theta"], int(r["diverged"])])
    # the boundary: diverged iff rho > rho* (allow the exactly-1 point to be ambiguous)
    classified = [(r["rho_factor"] > 1.0) == r["diverged"] for r in rows if abs(r["rho_factor"] - 1.0) > 1e-9]
    boundary_ok = all(classified)
    return {"p": p, "H": H, "theta": theta, "rho_star": rho_star,
            "rows": rows, "boundary_separates_converge_diverge": boundary_ok,
            "note": "Reduced-scale (p=32) ascent; corroborates eq:nu4-threshold.",
            "pass": boundary_ok}


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "outputs/gf"
    print("claim5:", claim5_numerical(out + "/c5")["pass"])
    print("claim3b:", claim3b_numerical(out + "/c3")["pass"])
    print("claim6:", claim6_numerical(out + "/c6")["pass"])
