"""Quick terminal demo (about 30-60 s). The notebook has the full version with plots."""
import numpy as np
from sim import *

rng = np.random.default_rng(7)
dev = Device(seed=3)
X, Y = calibration_chart(dev, rng, n=250, sigma=0.3)
model = fit_model(X, Y)

# one typical failing event, solved end to end
rng2 = np.random.default_rng(21)
while True:
    E, master, gain, off = make_event(dev, rng2)
    p = print_measure(dev, E, gain, off, np.zeros(C), rng2, 0.3)
    if not passes(p, master) and 1.5 <= DE(p, master).mean() <= 2.6:
        break
delta = np.zeros(C)
print(f"First sample: mean dE00 {DE(p, master).mean():.2f} -> fails tolerance (mean<=1.0, max<=1.5)")
for rnd in (1, 2, 3):
    step = advise(model, E * (1 + delta), p, master)
    delta = (1 + delta) * (1 + step) - 1
    p = print_measure(dev, E, gain, off, delta, rng2, 0.3)
    print(f"Round {rnd}: change per ink " + ", ".join(f"{v*100:+.1f}%" for v in step)
          + f" -> mean dE00 {DE(p, master).mean():.2f}")
    if passes(p, master):
        print("PASS, release batch"); break

# advisor vs one-knob rule, 40 events
N = 40
rngm = np.random.default_rng(100)
adv = np.array([advisor_event(dev, model, rngm, 0.3)[0] for _ in range(N)])
nai = np.array([naive_event(dev, model, rngm, 0.3)[0] for _ in range(N)])
print(f"\nOver {N} simulated events (rounds capped at 4; 5 = did not converge):")
print(f"  Advisor  : first-pass {np.mean(adv==1):.0%}, mean rounds {adv.mean():.2f}")
print(f"  One-knob : first-pass {np.mean(nai==1):.0%}, mean rounds {nai.mean():.2f}")
