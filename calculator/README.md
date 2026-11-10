# Scientific Calculator add-on for Thermal-Simulator

A scientific calculator written in **Python**, available two ways:

| File | What it is |
|---|---|
| `calc_engine.py` | Python calculator engine (safe `ast` parser, no `eval`). Shared by both front ends. |
| `scientific_calculator.py` | Desktop **Tkinter GUI** calculator. Run: `python calculator/scientific_calculator.py` |
| `calc_toggle.js` / `calc_toggle.css` | Floating 🧮 toggle button + calculator panel for the **lab (Simulation) page only**. Runs `calc_engine.py` in the browser through Pyodide. |
| `test_calc_engine.py` | Unit tests. Run from this folder: `python -m unittest` |

## Install (one line)

1. Copy the `calculator/` folder into the root of your repo (next to `index.html`).
2. In `index.html`, add this line right after `<script src="extras.js"></script>`, before `</body>`:

```html
<script src="calculator/calc_toggle.js"></script>
```

No other page is edited. The script checks the page name and does nothing anywhere except `index.html`, so the toggle button exists only in the lab.

## How it behaves

- 🧮 button sits next to the ☰ navigation button; tap it to open or close the calculator (Esc also closes it).
- Python (Pyodide, about 10 MB) downloads the first time you open the panel, then stays cached. It needs internet, like the Three.js CDN already does.
- Test locally over http, not by double-clicking the file: `python -m http.server`, then open `http://localhost:8000/`.

## Features

Deg/Rad mode, sin cos tan, inverse trig, sinh cosh tanh, ln, log (log(x, base) works too), log2, square root, cube root, x², x^y, exp, abs, factorial (`5!`, `(2+1)!`), `nCr(n,r)`, `nPr(n,r)`, floor, ceil, round, π, e, tau, `Ans` (previous result), EXP (×10^), implicit multiplication (`2pi`, `3(4+1)`), history, and clear error messages.
