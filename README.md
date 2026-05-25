# Interactive ψ(a/c, β) — Elliptical Crack Geometry Factor

An interactive Python plot of the **geometry modification factor ψ** for an elliptical crack, as defined in fracture mechanics (equation 2.21e). A slider lets you explore how the factor changes with the loading angle β from 0 to π.

---

## Physical background

In linear elastic fracture mechanics (LEFM), the **stress intensity factor K** at the front of an embedded elliptical crack depends not only on the applied stress and crack size, but also on the *shape* of the crack and the *angle* at which the stress is applied relative to the crack plane. This shape dependence is captured by the geometry modification factor **ψ(a/c, β)**.

### The elliptical crack

An embedded elliptical crack is characterised by two semi-axes:

- **a** — the semi-axis in the direction of crack depth
- **c** — the semi-axis in the direction of crack width

The ratio **a/c** (the axial ratio) describes the *ellipticity* of the crack:

| a/c | Crack shape |
|-----|-------------|
| a/c → 0 | Very flat, penny-shaped crack |
| a/c = 1 | Circular (penny-shaped) crack |
| a/c > 1 | Elongated, tunnel-like crack |

### The geometry factor ψ

The modification factor is defined as:

$$\psi(a/c,\, \beta) = \frac{\sqrt{\pi} \left[\cos^2\beta + \left(\dfrac{c}{a}\right)^2 \sin^2\beta\right]^{1/2}}{E(a/c)}$$

where:

- **β** is the angle between the applied stress direction and the crack plane normal (ranges from 0 to π)
- **E(a/c)** is the complete elliptic integral of the second kind:

$$E(a/c) = \int_0^{\pi/2} \left[1 - \left(1 - \frac{c^2}{a^2}\right)\sin^2\Phi\right]^{1/2} d\Phi$$

### Physical meaning of β

- **β = 0**: stress acts perpendicular to the crack plane (pure Mode I, opening mode) — maximum driving force for crack growth
- **β = π/2**: stress acts parallel to the crack plane — the elliptic correction is strongest and ψ is most sensitive to the axial ratio
- Intermediate β: mixed-mode loading

### Key limiting values (at β = 0)

| Condition | ψ value | Meaning |
|-----------|---------|---------|
| a/c = 1 (circle) | 2/√π ≈ 1.128 | Penny-shaped crack reference |
| a/c → ∞ | √π ≈ 1.772 | Long tunnel crack upper bound |

These are visible as dashed reference lines in the plot, matching Figure 2.9 of the source textbook.

---

## The elliptic integral — analytical evaluation

The integral E(a/c) is a **complete elliptic integral of the second kind**, one of the classical special functions of mathematics. It does not have a simple closed form in elementary functions, but it is tabulated and implemented analytically in scientific libraries.

In this code it is evaluated using:

```python
from scipy.special import ellipe
E = ellipe(k2)   # k² = 1 - (c/a)²  for a ≥ c
                 # k² = 1 - (a/c)²  for a < c
```

`scipy.special.ellipe` uses precomputed Chebyshev polynomial approximations — accurate to machine precision and orders of magnitude faster than numerical quadrature.

> **Note on the modulus:** For a/c < 1 (i.e. c is the major axis), the roles of the two semi-axes swap. The modulus k² must always be computed with respect to the *major* axis to remain in [0, 1).

---

## Usage

### Requirements

```
pip install numpy matplotlib scipy
```

### Run

```
python psi_crack_plot.py
```

The script precomputes E(a/c) analytically for 600 values of a/c ∈ [0.05, 4.0], then opens a matplotlib window with a live β slider.

---

## Reference

Lawn, B. R. (1993). *Fracture of Brittle Solids* (2nd ed.). Cambridge University Press. Equation 2.21e and Figure 2.9.
