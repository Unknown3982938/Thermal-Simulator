# Thermodynamics Lab

A self-contained, browser-based educational prototype inspired by the interaction style of PhET simulations.

## Run it
1. Extract the ZIP.
2. Open `index.html` in a modern browser (Chrome, Firefox, Edge, Safari).
3. No server, build step, or internet connection is required for the simulation itself.

## Files
- `index.html` — page structure and controls
- `styles.css` — responsive interface styling
- `app.js` — particle animation, simplified thermodynamic model, and graphs

## Included prototype features
- Heating/cooling control and a simplified phase-change model
- Animated particle view
- Ideal-gas-inspired temperature, volume, and pressure model
- First-law energy accounting: ΔU = Q − W
- Live temperature graph
- Pause and reset controls
- Responsive desktop/mobile layout

## Important physics limitations
This is an educational prototype, not a validated scientific simulator. The phase-change logic is intentionally simplified; it does not yet model a full energy ledger for latent heat, pressure-dependent phase boundaries, molecular potentials, real piston mechanics, or calibrated material properties. The gas mode uses an ideal-gas approximation and illustrative expansion behavior. Clearly label these assumptions if presenting it for assessment.

## Suggested development roadmap
1. Validate the physics model and units with a teacher or reliable thermodynamics reference.
2. Add a true energy ledger: sensible heat, latent heat, and work as distinct terms.
3. Add selectable materials with sourced properties.
4. Add graph axes, markers for melting/boiling points, and exportable experiment data.
5. Add guided activities and prediction questions for learners.
