# Thermo Lab: Heat Transfer Project

| Folder | Language | What it does |
|---|---|---|
| `web/index.html` | HTML + CSS + JavaScript (three.js) | 3D interactive model: gas laws, phase change, First Law |
| `python/thermo.py` | Python | Physics engine, CLI and unit tests |
| `python/desktop_app.py` | Python (Tkinter + Matplotlib) | Offline desktop version |

## Run
- Web: open `web/index.html` in a browser (needs internet once for three.js from cdnjs).
- Physics CLI: `python python/thermo.py curve water 1`, `python python/thermo.py gas 2 300 25`, `python python/thermo.py test`
- Desktop: `pip install numpy matplotlib` then `python python/desktop_app.py`

## Physics
Q = mcΔT, Q = mL, ΔU = Q − W, PV = nRT, KE = (3/2)kT.

## Ideas to extend
Add calorimetry, a C++ or Rust simulation core compiled to WebAssembly, more substances, a Flask API serving `thermo.py`.
