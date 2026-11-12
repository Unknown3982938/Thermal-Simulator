# Thermo Lab 3D

A static, browser-based thermodynamics learning project built as a Physics 2 school project. Features an interactive 3D simulation, experiment journal, achievement tracking, and supporting documentation — no backend required.

## Features

- **Interactive 3D Simulation** — Real-time thermodynamics simulation powered by Three.js (loaded via CDN).
- **Experiment Journal** — Take notes during experiments and export/import them as JSON.
- **Achievements** — Locally tracked milestones as you explore.
- **Learning Resources** — Tutorial, references, and about pages to support the project.
- **Easter Egg** — Type `THERMO` on any page (outside a text field) or click the laboratory brand mark seven times to reveal a hidden surprise.
- **Built-in python Calculator** - A convenient tool for calculating values and variables.

## Pages

| Page | Description |
|------|-------------|
| `index.html` | Interactive 3D simulation (requires internet access for the Three.js CDN). |
| `dashboard.html` | Project landing page. |
| `journal.html` | Local experiment notebook with JSON export/import. |
| `achievements.html` | Locally tracked milestones. |
| `tutorial.html` | Tutorial and usage guide. |
| `about.html` | Project information. |
| `references.html` | References and sources. |
| `credits.html` | Credits and acknowledgements. |
| `disclaimer.html` | Disclaimer. |
| `404.html` | Custom not-found page. |

## Local Data

Journal entries and achievement progress are saved in the browser's `localStorage` on the current device/browser. They are **not** uploaded or synchronized. Clearing site data or switching browsers/devices may remove or separate that information — export your journal entries regularly if you want a backup.

## Deploy

This is a static site — GitHub Pages can host it without a backend.

1. Upload the files and assets in this folder to the published root of your GitHub repository.
2. In your repository settings, enable **GitHub Pages** and set the source to the branch/folder containing these files (typically the root of `main`).
3. Visit the published URL to use the project.

Published simulation URL:  https://unknown3982938.github.io/Thermal-Simulator/

> **Note:** The 3D simulation loads Three.js from a CDN, so an internet connection is required for that page to work. Additionally, this repo is not intended for commercial use - it is intended for personal school project.

## License

GNU-GPL-v3.0
