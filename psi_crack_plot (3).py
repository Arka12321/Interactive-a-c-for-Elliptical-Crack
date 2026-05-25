import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.special import ellipe


def elliptic_E_vec(ac_array):
    """
    Analytical complete elliptic integral of the second kind E(k^2):
      k^2 = 1 - (c/a)^2  for a >= c  (ac >= 1)
      k^2 = 1 - (a/c)^2  for a <  c  (ac <  1)
    scipy.special.ellipe takes the parameter m = k^2.
    """
    k2 = np.where(ac_array >= 1,
                  1 - (1 / ac_array)**2,
                  1 - ac_array**2)
    return ellipe(k2)


def psi_vec(ac_array, E_array, beta):
    """
    psi(a/c, beta) = sqrt(pi) * [cos^2(beta) + (c/a)^2 * sin^2(beta)]^(1/2) / E(a/c)
    """
    ca = 1 / ac_array
    inner = np.cos(beta)**2 + ca**2 * np.sin(beta)**2
    return np.sqrt(np.pi) * np.sqrt(inner) / E_array


# --- Compute analytically (no precompute needed, it's instant) ---
ac_values = np.linspace(0.05, 4.0, 600)
E_values  = elliptic_E_vec(ac_values)

beta_init  = 0.0
psi_values = psi_vec(ac_values, E_values, beta_init)

fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.22)

(line,) = ax.plot(ac_values, psi_values, color="#1a1a1a", linewidth=2.5)

# Reference lines matching Fig 2.9
ax.axhline(np.sqrt(np.pi),   color="gray", linestyle="--", linewidth=1.2)
ax.axhline(2/np.sqrt(np.pi), color="gray", linestyle="--", linewidth=1.2)
ax.axvline(1.0,               color="gray", linestyle="--", linewidth=1.0)
ax.text(4.05, np.sqrt(np.pi),   r"$\pi^{1/2}$",   va="center", fontsize=12)
ax.text(4.05, 2/np.sqrt(np.pi), r"$2/\pi^{1/2}$", va="center", fontsize=12)

ax.set_xlabel("Axial ratio, $a/c$", fontsize=13)
ax.set_ylabel(r"Modification factor, $\psi(a/c,\,\beta)$", fontsize=13)
ax.set_title(r"Geometry modification factor $\psi$ vs axial ratio $a/c$", fontsize=13)
ax.set_xlim(0, 4)
ax.set_ylim(0, 2.5)
ax.grid(True, linestyle="--", alpha=0.3)

beta_text = ax.text(0.65, 0.08, r"$\beta = 0$",
                    transform=ax.transAxes, fontsize=12, color="#1f77b4")

# --- Slider ---
ax_slider = plt.axes([0.15, 0.07, 0.7, 0.03])
slider = Slider(ax=ax_slider, label=r"$\beta$",
                valmin=0, valmax=np.pi, valinit=beta_init,
                valstep=0.01, color="#1f77b4")


def beta_label(b):
    frac = b / np.pi
    if abs(frac) < 0.005:        return r"$\beta = 0$"
    if abs(frac - 0.25) < 0.008: return r"$\beta = \pi/4$"
    if abs(frac - 0.5)  < 0.008: return r"$\beta = \pi/2$"
    if abs(frac - 0.75) < 0.008: return r"$\beta = 3\pi/4$"
    if abs(frac - 1.0)  < 0.008: return r"$\beta = \pi$"
    return rf"$\beta = {frac:.2f}\pi$"


def update(val):
    b = slider.val
    line.set_ydata(psi_vec(ac_values, E_values, b))
    beta_text.set_text(beta_label(b))
    fig.canvas.draw_idle()


slider.on_changed(update)
plt.show()
