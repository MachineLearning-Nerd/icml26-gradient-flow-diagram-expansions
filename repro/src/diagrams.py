"""Independent reconstruction of the diagram calculus of
"Gradient Flow Through Diagram Expansions" (arXiv:2602.04548), Sec. 3 + App. A.

A *diagram* is a multigraph with H-nodes (sum over the width index k=1..H) and
p-nodes (sum over the input index i=1..p), and coloured edges = weights
u_{k,i}^{(m)}.  For the identity target F_{i_1..i_nu}=delta_{i_1=...=i_nu}:

  D_{2nu}: 2 H-nodes, nu p-nodes; p-node m joined to both H-nodes, colour m.
           (= sum f^2 ; 2*nu edges)
  R_nu   : 1 H-node, 1 p-node, nu parallel edges of colours 1..nu (ASYM) or
           all colour 1 (SYM).  (= model . target ; nu edges)

merge(G,G')  realises  sum_u dG/du dG'/du  (delete an equal-colour edge from
each, identify their endpoints).  wick_average(G) = E[G](0) over u~N(0,sigma^2):
sum over pairings of equal-colour edges; each contributes p^q H^n sigma^{2l}.

By construction E[G] is a polynomial in (H,p,sigma^2) -- this IS the content of
Thm 3.1.  The loss-expansion coefficients are
    Y_s = E[ (1/2 D_{2nu} - R_nu)^{star (s+1)} ]
(+ pure-target constant p/2 for s=0).  This module enumerates Y_s exactly.
"""

from __future__ import annotations
from fractions import Fraction
from itertools import permutations
from typing import Dict, List, Tuple

Edge = Tuple[int, int, int]          # (h_node, p_node, colour)
Monomial = Tuple[int, int, int]      # (q, n, 2l)  ->  p^q H^n sigma^{2l}
Poly = Dict[Monomial, Fraction]      # monomial -> exact coefficient


def _refine(g: List[Edge], h_nodes: List[int], p_nodes: List[int]):
    """Weisfeiler-Lh refinement: return a partition (dict node->label) of H- and
    p-nodes that is isomorphism-invariant for these coloured bipartite multigraphs.
    Nodes are split by the sorted multiset of (edge-colour, neighbour-label) until
    stable.  Two nodes can only be swapped by an isomorphism if they share a label."""
    label = {n: (0,) for n in h_nodes}
    labelp = {n: (0,) for n in p_nodes}
    hset, pset = set(h_nodes), set(p_nodes)

    def neigh(node, is_h):
        col = []
        for (h, p, c) in g:
            if is_h and h == node:
                col.append((c, labelp[p]))
            if (not is_h) and p == node:
                col.append((c, label[h]))
        return tuple(sorted(col))

    for _ in range(len(g) + 4):
        newh = {n: (label[n], neigh(n, True)) for n in h_nodes}
        newp = {n: (labelp[n], neigh(n, False)) for n in p_nodes}
        # relabel by sorted order of new signatures (stable ids)
        sh = sorted(set(newh.values()))
        sp = sorted(set(newp.values()))
        mh = {v: i for i, v in enumerate(sh)}
        mp = {v: i for i, v in enumerate(sp)}
        nh = {n: mh[newh[n]] for n in h_nodes}
        np_ = {n: mp[newp[n]] for n in p_nodes}
        if nh == label and np_ == labelp:
            break
        label, labelp = nh, np_
    return label, labelp


def _canonicalize(g: List[Edge]) -> Tuple[Edge, ...]:
    """Exact canonical form: refine nodes by WL signature, then permute only
    within tied classes (few perms), taking the lexicographically smallest sorted
    edge tuple.  Isomorphic diagrams share a canonical form."""
    h_nodes = sorted({e[0] for e in g})
    p_nodes = sorted({e[1] for e in g})
    if len(h_nodes) > 9 or len(p_nodes) > 9:
        return tuple(sorted((e[2], e[0], e[1]) for e in g))
    lh, lp = _refine(g, h_nodes, p_nodes)
    # group nodes of same type by label
    hgroups: Dict[int, List[int]] = {}
    pgroups: Dict[int, List[int]] = {}
    for n in h_nodes:
        hgroups.setdefault(lh[n], []).append(n)
    for n in p_nodes:
        pgroups.setdefault(lp[n], []).append(n)
    best = None
    h_perm_groups = [sorted(v) for v in hgroups.values()]
    p_perm_groups = [sorted(v) for v in pgroups.values()]
    # iterate over permutations within each group (cartesian product)
    from itertools import product as iproduct
    h_base = []
    for grp in h_perm_groups:
        h_base.append(grp[0])  # representative ordering seed
    # build all H relabellings: within each group, all orderings
    def all_relabels(groups):
        opts = []
        for grp in groups:
            from itertools import permutations
            opts.append(list(permutations(grp)))
        for combo in iproduct(*opts):
            mp = {}
            newid = 0
            for ordering in combo:
                for old in ordering:
                    mp[old] = newid
                    newid += 1
            yield mp
    for hmap in all_relabels(h_perm_groups):
        for pmap in all_relabels(p_perm_groups):
            rep = tuple(sorted((hmap[e[0]], pmap[e[1]], e[2]) for e in g))
            if best is None or rep < best:
                best = rep
    return best  # type: ignore[return-value]


def _aggregate(front: List[Tuple[List[Edge], Fraction]]
               ) -> List[Tuple[List[Edge], Fraction]]:
    """Aggregate isomorphic diagrams (same canonical form) summing coefficients."""
    buckets: Dict[Tuple[Edge, ...], Tuple[List[Edge], Fraction]] = {}
    for (gd, cd) in front:
        key = _canonicalize(gd)
        if key in buckets:
            bg, bc = buckets[key]
            buckets[key] = (bg, bc + cd)
        else:
            buckets[key] = (gd, cd)
    return list(buckets.values())


def diagram_D(nu: int, symmetric: bool) -> List[Edge]:
    """D_{2nu}: 2 H-nodes, nu p-nodes; p-node m joined to both H-nodes. In SYM
    all edges share colour 0 (one weight u_{k,i}); in ASYM p-node m's edges
    carry colour m (the mode index)."""
    e: List[Edge] = []
    for m in range(nu):
        c = 0 if symmetric else m
        e.append((0, m, c))
        e.append((1, m, c))
    return e


def diagram_R(nu: int, symmetric: bool) -> List[Edge]:
    return [(0, 0, 0 if symmetric else m) for m in range(nu)]


def merge(g: List[Edge], gp: List[Edge]) -> List[List[Edge]]:
    """All diagrams G star G' (Sec. 3). g keeps its labels; g' is relabelled
    into a disjoint namespace with the chosen edge's endpoints identified to
    the chosen edge in g."""
    out: List[List[Edge]] = []
    max_h_g = max((e[0] for e in g), default=-1)
    max_p_g = max((e[1] for e in g), default=-1)
    oh = max_h_g + 1
    op = max_p_g + 1
    for i, (ha, pa, ca) in enumerate(g):
        base = [g[k] for k in range(len(g)) if k != i]
        for j, (hb, pb, cb) in enumerate(gp):
            if ca != cb:
                continue
            merged = list(base)
            for k, (h2, p2, c2) in enumerate(gp):
                if k == j:
                    continue
                nh = ha if h2 == hb else h2 + oh
                np_ = pa if p2 == pb else p2 + op
                merged.append((nh, np_, c2))
            out.append(merged)
    return out


def _matchings(idx: List[int], colours: List[int]) -> List[List[Tuple[int, int]]]:
    out: List[List[Tuple[int, int]]] = []
    acc: List[Tuple[int, int]] = []

    def rec(rest: List[int]) -> None:
        if not rest:
            out.append(list(acc))
            return
        first = rest[0]
        tail = rest[1:]
        for k, j in enumerate(tail):
            if colours[first] == colours[j]:
                acc.append((first, j))
                rec(tail[:k] + tail[k + 1:])
                acc.pop()

    rec(idx)
    return out


def wick_average(g: List[Edge]) -> Poly:
    """E[G](0) = sum over perfect matchings of equal-colour edges of
    p^(#p-nodes) H^(#H-nodes) sigma^(#edges)."""
    n = len(g)
    if n == 0:
        return {(0, 0, 0): Fraction(1)}
    if n % 2 == 1:
        return {}
    colours = [e[2] for e in g]
    poly: Poly = {}
    for m in _matchings(list(range(n)), colours):
        h_parent: Dict[int, int] = {}
        p_parent: Dict[int, int] = {}

        def find(d, x):
            d.setdefault(x, x)
            while d[x] != x:
                d[x] = d[d[x]]
                x = d[x]
            return x

        for a, b in m:
            ha, pa, _ = g[a]
            hb, pb, _ = g[b]
            ra, rb = find(h_parent, ha), find(h_parent, hb)
            h_parent[ra] = rb
            ra, rb = find(p_parent, pa), find(p_parent, pb)
            p_parent[ra] = rb
        nH = len({find(h_parent, k) for k in h_parent})
        nP = len({find(p_parent, k) for k in p_parent})
        mono = (nP, nH, n)
        poly[mono] = poly.get(mono, Fraction(0)) + Fraction(1)
    return poly


def star_power(nu: int, symmetric: bool, s: int) -> Poly:
    """Y_s = E[(1/2 D - R)^{star (s+1)}] as an exact polynomial."""
    D = diagram_D(nu, symmetric)
    R = diagram_R(nu, symmetric)
    factors = s + 1
    # current = list of (diagram, coeff); one factor (1/2 D - R)
    current: List[Tuple[List[Edge], Fraction]] = [(D, Fraction(1, 2)), (R, Fraction(-1))]
    current = _aggregate(current)
    for _ in range(factors - 1):
        nxt: List[Tuple[List[Edge], Fraction]] = []
        for (gd, cd) in current:
            for mds in merge(gd, D):
                nxt.append((mds, cd * Fraction(1, 2)))
            for mds in merge(gd, R):
                nxt.append((mds, cd * Fraction(-1)))
        current = _aggregate(nxt)
    poly: Poly = {}
    for (gd, cd) in current:
        for mono, cc in wick_average(gd).items():
            poly[mono] = poly.get(mono, Fraction(0)) + cd * cc
    return {m: c for m, c in poly.items() if c != 0}


def pareto_set(poly: Poly) -> List[Monomial]:
    """Pareto-optimal monomials (paper Sec. 4): among monomials sharing the same
    2l, keep those whose (q,n) is maximal in the Pareto sense (not dominated)."""
    by_l: Dict[int, List[Monomial]] = {}
    for mono in poly:
        by_l.setdefault(mono[2], []).append(mono)
    front: List[Monomial] = []
    for l, items in by_l.items():
        for mono in items:
            q, n, _ = mono
            dominated = False
            for mono2 in items:
                if mono2 == mono:
                    continue
                q2, n2, _ = mono2
                if q2 >= q and n2 >= n and (q2 > q or n2 > n):
                    dominated = True
                    break
            if not dominated:
                front.append(mono)
    return sorted(front)


def Q_formula(n: int, sD: int, nu: int, symmetric: bool) -> int:
    """Q(n, s_D) from Thm 4.1."""
    if symmetric:
        return 1 + (nu - 1) * sD - (nu // 2) * (n - 1)
    return 1 + (nu - 1) * (sD + 1 - n)


def predicted_pareto_terms(s: int, nu: int, symmetric: bool) -> List[Monomial]:
    """The (q, n, 2l) Pareto triples predicted by Thm 4.1 (identity target)."""
    triples: List[Monomial] = []
    for sD in range(0, s + 2):
        for n in range(1, sD + 2):
            two_l = nu * (sD + 1) + (nu - 2) * s
            q = Q_formula(n, sD, nu, symmetric)
            triples.append((q, n, two_l))
    if not symmetric:
        # ASYM exceptions (Thm 4.1): drop (a) odd s_R=s+1-s_D, (b) (n,sD)=(s+2,s+1)
        kept = []
        for (q, n, two_l) in triples:
            # recover sD from two_l = nu(sD+1)+(nu-2)s  ->  sD = (two_l-(nu-2)s)/nu -1
            sD = (two_l - (nu - 2) * s) // nu - 1
            sR = s + 1 - sD
            if sR % 2 == 1:
                continue            # a) odd s_R does not occur
            if n == s + 2 and sD == s + 1:
                continue            # b) exceptional vertex
            kept.append((q, n, two_l))
        triples = kept
    return sorted(set(triples))
