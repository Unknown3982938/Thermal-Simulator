# Thermo Lab 3D

An interactive thermodynamics learning website built with HTML, CSS, JavaScript, and Three.js.

## Files

- `dashboard.html` — project landing page and module launcher
- `index.html` — interactive 3D simulation
- `tutorial.html` — user guide
- `about.html` — project overview
- `references.html` — learning and technical references
- `credits.html` — project contributors and acknowledgments
- `disclaimer.html` — educational-use and simulation limitations
- `404.html` — custom GitHub Pages not-found page
- `navigation.css` / `navigation.js` — shared navigation used by the information pages

## Deploy with GitHub Pages

1. Upload the contents of this folder to the root of your GitHub repository. Do not upload the outer ZIP folder itself.
2. In GitHub, open **Settings → Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Select branch `main` and folder `/(root)`, then save.
5. Wait for the Pages deployment to finish. Open the published site and test the Dashboard, Simulation, Tutorial, About, References, Credits, and Disclaimer links.

If your repository uses a GitHub Actions Pages workflow already, keep that workflow and its configured publishing directory. Place these files in the directory that the workflow publishes.

## Notes

- The site is a static website, but its front-end interactions and 3D simulation still run in the browser.
- The simulation loads Three.js r128 from a CDN, so an internet connection is required for the 3D library to load.
- The site uses relative links so it can be hosted from a GitHub Pages project repository.
- The `404.html` page is recognized by GitHub Pages when it is placed in the published root.
