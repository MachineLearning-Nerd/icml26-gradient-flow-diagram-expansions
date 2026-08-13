# Methods — the diagram calculus (`repro/src/diagrams.py`)

The core of the reconstruction is a from-scratch implementation of the paper's diagram
machinery (Sec. 3 + App. A):

```python
# atomic diagrams for the identity target
def diagram_D(nu, symmetric): ...   # 2 H-nodes, nu p-nodes, coloured edges
def diagram_R(nu, symmetric): ...   # 1 H-node, 1 p-node, nu parallel edges
def merge(g, gp): ...               # G star G' = sum_u dG/du dG'/du
def wick_average(g): ...            # pair equal-colour edges -> p^q H^n sigma^{2l}
def star_power(nu, symmetric, s):   # Y_s = E[(1/2 D - R)^{star(s+1)}]
```

Wick averaging makes polynomiality (Thm 3.1) hold by construction. Isomorphic diagrams are
aggregated via an **exact canonical form** (Weisfeiler-Lehman refinement + within-class
permutation), which makes enumeration tractable without changing coefficients. All
coefficients are exact Python `Fraction`s.
