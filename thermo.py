"""Thermo Lab physics engine (stdlib only) with CLI and tests.
Usage: python thermo.py curve [water|ethanol] [mass_kg]  |  gas n T V  |  test"""
import math, sys, unittest

R, KB = 8.314, 1.380649e-23
SUBSTANCES = {
    "water":   dict(mp=0,    bp=100, ci=2.09, cl=4.18, cg=2.01, lf=334, lv=2260),
    "ethanol": dict(mp=-114, bp=78,  ci=0.97, cl=2.44, cg=1.43, lf=108, lv=846),
}

def sensible(m, c, dT): return m * c * dT          # Q = mc*dT  (kJ)
def latent(m, L): return m * L                     # Q = mL     (kJ)
def first_law(Q, W): return Q - W                  # dU = Q - W
def gas_pressure(n, T, V_L): return n * R * T / (V_L / 1000) / 1000   # kPa
def v_rms(T, M): return math.sqrt(3 * R * T / M)   # m/s
def avg_ke(T): return 1.5 * KB * T                 # J

def heating_curve(sub, m, below_mp=20):
    """Return [(cumulative_Q_kJ, T_C), ...] corner points of the heating curve."""
    s = SUBSTANCES[sub]; t0 = s["mp"] - below_mp; top = s["bp"] + 50
    steps = [(sensible(m, s["ci"], s["mp"] - t0), s["mp"]), (latent(m, s["lf"]), s["mp"]),
             (sensible(m, s["cl"], s["bp"] - s["mp"]), s["bp"]), (latent(m, s["lv"]), s["bp"]),
             (sensible(m, s["cg"], top - s["bp"]), top)]
    pts, q = [(0.0, t0)], 0.0
    for dq, t in steps:
        q += dq; pts.append((q, t))
    return pts

class Tests(unittest.TestCase):
    def test_water_total(self):
        self.assertAlmostEqual(heating_curve("water", 1)[-1][0], 41.8 + 334 + 418 + 2260 + 100.5, 1)
    def test_first_law(self): self.assertEqual(first_law(30, 10), 20)
    def test_pressure(self): self.assertAlmostEqual(gas_pressure(1, 273.15, 22.4), 101.4, 0)

if __name__ == "__main__":
    a = sys.argv[1:] or ["test"]
    if a[0] == "curve":
        for q, t in heating_curve(a[1] if len(a) > 1 else "water", float(a[2]) if len(a) > 2 else 1):
            print(f"Q = {q:9.1f} kJ   T = {t:7.1f} C")
    elif a[0] == "gas":
        n, T, V = map(float, a[1:4]); print(f"P = {gas_pressure(n, T, V):.1f} kPa, v_rms(N2) = {v_rms(T, .028):.0f} m/s")
    else:
        unittest.main(argv=["x"])
