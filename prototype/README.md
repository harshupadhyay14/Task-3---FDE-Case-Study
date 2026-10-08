# Tile shade advisor: synthetic prototype

Supports one claim in the case study: a **calibration chart + local sensitivity model + one confirmation tile** converges to tolerance in about one round, and the plan has a clear stop line when same-file print repeatability is too poor.

**Everything here is synthetic.** The "printer and kiln" is a made-up nonlinear function with hidden drift. It shows the mechanism works *if* the device behaves like this. It says nothing about real tiles. Do not quote the numbers as expected client performance.

## Files
- `tile_shade_advisor_prototype.ipynb`: the notebook (executed, outputs included)
- `sim.py`: synthetic device, calibration, forward model, solver (the "advisor"), naive baseline
- `convergence.png`, `repeatability_gate.png`: plots from the notebook

## Run
```
pip install numpy scipy scikit-learn scikit-image matplotlib jupyter
jupyter notebook tile_shade_advisor_prototype.ipynb
```

## What it does
1. Checks the scenario is solvable by an oracle (otherwise the test is meaningless).
2. Fits a forward model from a 250-patch calibration chart (deliberately imperfect).
3. Solves a bounded least-squares problem for per-channel ink changes that minimise dE00 against the master, anchored to the measured production tile.
4. Compares against a one-knob rule of thumb.
5. Sweeps same-file print repeatability to show where the approach stops working (the week-2 gate).

## Honest limits
Drift is assumed mostly per-channel gain (correctable by ink changes). Real drift from kiln position or body colour may not be. Registration on patterned tiles, instrument error beyond flat noise, gloss and metamerism are not modelled. No manual-QC baseline is simulated on purpose, since a made-up one would only reflect my assumptions.
