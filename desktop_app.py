"""
Interactive Educational Model on Heat Transfer
Sensible heat, latent heat, gas behavior, First Law of Thermodynamics,
Kinetic Theory of Gases and Gas Laws.

Requires: Python 3.8+, numpy, matplotlib   (tkinter comes with Python)
Install:  pip install numpy matplotlib
Run:      python heat_transfer_model.py
"""
import math
import random
import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------- Constants ----------
R = 8.314            # J/(mol*K)
K_B = 1.380649e-23   # J/K
N_A = 6.022e23
C_ICE, C_WATER, C_STEAM = 2.09, 4.18, 2.01   # kJ/(kg*K)
L_FUS, L_VAP = 334.0, 2260.0                  # kJ/kg
T_TOP = 150.0                                 # top of the heating curve (deg C)
M_N2 = 0.028                                  # kg/mol (nitrogen gas)


def make_slider(parent, label, lo, hi, init, fmt, command):
    """Labeled slider. Returns the DoubleVar holding the value."""
    var = tk.DoubleVar(value=init)
    row = ttk.Frame(parent)
    row.pack(fill="x", pady=4)
    value_lbl = ttk.Label(row, text=fmt.format(init), width=12, anchor="e")
    ttk.Label(row, text=label).pack(side="left")
    value_lbl.pack(side="right")

    def on_move(_=None):
        value_lbl.config(text=fmt.format(var.get()))
        command()

    ttk.Scale(parent, from_=lo, to=hi, variable=var, command=on_move).pack(fill="x")
    return var


# ======================================================================
# TAB 1: Sensible + Latent heat (heating curve of water)
# ======================================================================
class HeatingCurveTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=8)
        ctrl = ttk.Frame(self, width=260)
        ctrl.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(ctrl, text="Heating Curve of Water",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(ctrl, text="Q = mcΔT (sensible)   Q = mL (latent)",
                  foreground="#555").pack(anchor="w", pady=(0, 8))

        self.m = make_slider(ctrl, "Mass (kg)", 0.1, 5.0, 1.0, "{:.2f}", self.update)
        self.t0 = make_slider(ctrl, "Start temp (°C)", -50, -1, -20, "{:.0f}", self.update)
        self.q = make_slider(ctrl, "Heat added (kJ)", 0, 15000, 1000, "{:.0f}", self.update)

        self.readout = tk.Label(ctrl, justify="left", anchor="nw", font=("Consolas", 10),
                                bg="#f4f6f8", padx=8, pady=8)
        self.readout.pack(fill="x", pady=10)

        fig = Figure(figsize=(6, 4.2), dpi=100)
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True)
        self.update()

    def stages(self):
        m, t0 = self.m.get(), self.t0.get()
        q1 = m * C_ICE * (0 - t0)
        q2 = m * L_FUS
        q3 = m * C_WATER * 100
        q4 = m * L_VAP
        q5 = m * C_STEAM * (T_TOP - 100)
        edges = np.cumsum([0, q1, q2, q3, q4, q5])
        temps = [t0, 0, 0, 100, 100, T_TOP]
        names = ["Ice warming (sensible)", "Melting (latent)", "Water warming (sensible)",
                 "Boiling (latent)", "Steam warming (sensible)"]
        return edges, temps, names

    def update(self):
        edges, temps, names = self.stages()
        q = self.q.get()
        # find current temperature and stage
        if q >= edges[-1]:
            idx, temp = 4, T_TOP
        else:
            idx = int(np.searchsorted(edges, q, side="right") - 1)
            idx = min(max(idx, 0), 4)
            span = edges[idx + 1] - edges[idx]
            frac = (q - edges[idx]) / span if span else 0
            temp = temps[idx] + (temps[idx + 1] - temps[idx]) * frac

        ax = self.ax
        ax.clear()
        colors = ["#4aa3df", "#2e7d32", "#1e88e5", "#2e7d32", "#e57373"]
        for i in range(5):
            ax.plot(edges[i:i + 2], temps[i:i + 2], color=colors[i], lw=3)
        ax.plot([q], [temp], "o", color="#d32f2f", ms=11, zorder=5)
        ax.axhline(0, color="#999", lw=0.6, ls="--")
        ax.axhline(100, color="#999", lw=0.6, ls="--")
        ax.set_xlabel("Heat added Q (kJ)")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Flat sections = latent heat (phase change)")
        ax.grid(alpha=0.25)
        self.canvas.figure.tight_layout()
        self.canvas.draw_idle()

        extra = ""
        if idx == 1:
            extra = f"\nMelted: {(q - edges[1]) / (edges[2] - edges[1]) * 100:.0f}%"
        elif idx == 3:
            extra = f"\nVaporized: {(q - edges[3]) / (edges[4] - edges[3]) * 100:.0f}%"
        self.readout.config(text=(
            f"Stage: {names[idx]}\n"
            f"Temperature: {temp:.1f} °C\n"
            f"Heat added: {q:.0f} kJ\n"
            f"Total to reach {T_TOP:.0f} °C: {edges[-1]:.0f} kJ{extra}"))


# ======================================================================
# TAB 2: Gas laws + kinetic theory (particle animation)
# ======================================================================
class GasTab(ttk.Frame):
    W, H = 460, 340

    def __init__(self, parent):
        super().__init__(parent, padding=8)
        ctrl = ttk.Frame(self, width=260)
        ctrl.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(ctrl, text="Ideal Gas & Kinetic Theory",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(ctrl, text="PV = nRT   KE = (3/2)kT", foreground="#555").pack(anchor="w", pady=(0, 8))

        self.n = make_slider(ctrl, "Amount n (mol)", 0.5, 5.0, 2.0, "{:.2f}", self.update)
        self.t = make_slider(ctrl, "Temperature (K)", 100, 1000, 300, "{:.0f}", self.update)
        self.v = make_slider(ctrl, "Volume (L)", 5, 50, 25, "{:.1f}", self.update)

        self.readout = tk.Label(ctrl, justify="left", anchor="nw", font=("Consolas", 10),
                                bg="#f4f6f8", padx=8, pady=8)
        self.readout.pack(fill="x", pady=10)
        ttk.Label(ctrl, text="Try: raise T → particles speed up.\nShrink V → pressure rises.",
                  foreground="#555").pack(anchor="w")

        self.canvas = tk.Canvas(self, width=self.W, height=self.H, bg="white",
                                highlightthickness=1, highlightbackground="#bbb")
        self.canvas.pack(side="right", padx=4)
        self.particles = []
        self.update()
        self.animate()

    def box_width(self):
        return 120 + (self.v.get() - 5) / 45 * (self.W - 130)

    def update(self):
        n, t, v = self.n.get(), self.t.get(), self.v.get()
        pressure_kpa = n * R * t / (v / 1000) / 1000
        ke = 1.5 * K_B * t
        vrms = math.sqrt(3 * R * t / M_N2)
        self.readout.config(text=(
            f"Pressure: {pressure_kpa:.1f} kPa\n"
            f"Avg KE:   {ke:.2e} J\n"
            f"v_rms:    {vrms:.0f} m/s (N2)\n"
            f"Molecules: {n * N_A:.2e}"))
        target = int(n * 20)
        while len(self.particles) < target:
            self.particles.append([random.uniform(10, 100), random.uniform(10, self.H - 10),
                                   random.uniform(-1, 1), random.uniform(-1, 1)])
        del self.particles[target:]

    def animate(self):
        c = self.canvas
        c.delete("all")
        bw = self.box_width()
        speed = math.sqrt(self.t.get() / 300) * 4
        c.create_rectangle(2, 2, bw, self.H - 2, outline="#1565c0", width=3)
        for p in self.particles:
            norm = math.hypot(p[2], p[3]) or 1
            p[0] += p[2] / norm * speed
            p[1] += p[3] / norm * speed
            if p[0] < 6 or p[0] > bw - 6:
                p[2] *= -1
                p[0] = min(max(p[0], 6), bw - 6)
            if p[1] < 6 or p[1] > self.H - 6:
                p[3] *= -1
                p[1] = min(max(p[1], 6), self.H - 6)
            # redder = faster / hotter
            heat = min(1, (self.t.get() - 100) / 900)
            color = f"#{int(40 + 215 * heat):02x}50{int(220 - 180 * heat):02x}"
            c.create_oval(p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4, fill=color, outline="")
        self.after(30, self.animate)


# ======================================================================
# TAB 3: First Law of Thermodynamics
# ======================================================================
class FirstLawTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=8)
        ctrl = ttk.Frame(self, width=260)
        ctrl.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(ctrl, text="First Law of Thermodynamics",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(ctrl, text="ΔU = Q − W", foreground="#555").pack(anchor="w", pady=(0, 8))

        self.q = make_slider(ctrl, "Heat in Q (kJ)", -50, 50, 30, "{:.1f}", self.update)
        self.w = make_slider(ctrl, "Work by gas W (kJ)", -50, 50, 10, "{:.1f}", self.update)
        self.n = make_slider(ctrl, "Gas amount n (mol)", 0.5, 5.0, 2.0, "{:.2f}", self.update)

        self.readout = tk.Label(ctrl, justify="left", anchor="nw", font=("Consolas", 10),
                                bg="#f4f6f8", padx=8, pady=8)
        self.readout.pack(fill="x", pady=10)

        fig = Figure(figsize=(6, 4.2), dpi=100)
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True)
        self.update()

    def update(self):
        q, w, n = self.q.get(), self.w.get(), self.n.get()
        du = q - w
        dT = du * 1000 / (1.5 * n * R)   # monatomic ideal gas: U = (3/2) nRT
        ax = self.ax
        ax.clear()
        bars = ax.bar(["Q (heat in)", "W (work out)", "ΔU (internal)"], [q, w, du],
                      color=["#e57373", "#64b5f6", "#81c784"])
        ax.axhline(0, color="black", lw=0.8)
        ax.set_ylabel("Energy (kJ)")
        ax.set_ylim(-110, 110)
        ax.bar_label(bars, fmt="%.1f")
        ax.set_title("Energy balance")
        self.canvas.figure.tight_layout()
        self.canvas.draw_idle()
        trend = "warms up" if du > 0 else "cools down" if du < 0 else "stays the same"
        self.readout.config(text=(
            f"ΔU = {q:.1f} − {w:.1f} = {du:.1f} kJ\n"
            f"Monatomic gas {trend}:\n"
            f"ΔT = {dT:.1f} K"))


# ======================================================================
def main():
    root = tk.Tk()
    root.title("Interactive Educational Model on Heat Transfer")
    root.geometry("1000x560")
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)
    nb.add(HeatingCurveTab(nb), text="Sensible & Latent Heat")
    nb.add(GasTab(nb), text="Gas Laws & Kinetic Theory")
    nb.add(FirstLawTab(nb), text="First Law")
    root.mainloop()


if __name__ == "__main__":
    main()
