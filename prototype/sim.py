import numpy as np
from scipy.optimize import least_squares
from skimage.color import deltaE_ciede2000

C = 6          # ink channels
R = 7          # measurement regions per tile
TOL_MEAN, TOL_MAX = 1.0, 1.5
DE = lambda a, b: deltaE_ciede2000(a, b)


# ---------------------------------------------------------------- synthetic device
class Device:
    """Synthetic printer+kiln: ink amounts (0..1)^6 -> fired Lab. Nonlinear, with channel
    interactions. `gain` and `offset` are the hidden drift (ink lot, kiln) that makes the
    same file print a different shade on a different day."""
    def __init__(self, seed=0):
        rng = np.random.default_rng(seed)
        self.W = rng.normal(0, 1, (C, 3)) * np.array([22, 14, 14])   # per-ink Lab effect
        self.k = rng.uniform(1.2, 2.5, C)                              # saturation (dot gain)
        self.I = rng.normal(0, 1, (C, C, 3)) * 2.0                     # pair interactions
        self.base = np.array([88.0, 0.5, 4.0])                         # bare tile Lab

    def lab(self, ink, gain=None, offset=None):
        ink = np.atleast_2d(ink)
        g = np.ones(C) if gain is None else gain
        a = np.clip(ink * g, 0, 1.2)
        s = 1 - np.exp(-self.k * a)                                    # (n, C)
        out = self.base + s @ self.W
        out = out + np.einsum('nc,nd,cdj->nj', s, s, self.I)
        if offset is not None:
            out = out + offset
        return out


def tile_inks(rng):
    """Ink amounts at R measurement regions (a patterned tile: different regions, different mixes)."""
    e = rng.dirichlet(np.ones(C) * 0.7, size=R) * rng.uniform(0.5, 1.0, (R, 1))
    return np.clip(e, 0, 1)


# ---------------------------------------------------------------- calibration chart
def calibration_chart(dev, rng, n=250, sigma=0.3):
    """Ramps per ink + 2-3 ink mixes + random mixes. Measured with print/fire/measure noise."""
    X = []
    for c in range(C):
        for v in np.linspace(0.1, 1, 8):
            x = np.zeros(C); x[c] = v; X.append(x)
    while len(X) < n:
        x = np.zeros(C)
        idx = rng.choice(C, size=rng.integers(2, 5), replace=False)
        x[idx] = rng.uniform(0.1, 0.9, len(idx)); X.append(x)
    X = np.array(X)
    Y = dev.lab(X) + rng.normal(0, sigma, (len(X), 3))
    return X, Y


def fit_model(X, Y):
    """Forward model: per-channel tone curve (sat. exponential) + linear + quadratic mixing.
    Deliberately simple and *wrong* vs the true device structure (the true device has
    unknown pair interactions) -- a realistic model mismatch."""
    from sklearn.linear_model import Ridge
    k = 1.8  # shared assumed saturation constant (not the true per-channel values)
    def feats(x):
        s = 1 - np.exp(-k * np.clip(x, 0, 1.2))
        quad = np.stack([s[:, i] * s[:, j] for i in range(C) for j in range(i, C)], 1)
        return np.hstack([s, quad])
    m = Ridge(alpha=1e-2).fit(feats(X), Y)
    W, b = m.coef_.T.copy(), m.intercept_.copy()
    return lambda x: feats(np.atleast_2d(x)) @ W + b


def jacobian(model, e, eps=0.02):
    """dLab / d(relative change in each ink) at ink vector e (3 x C), by finite differences."""
    J = np.zeros((3, C))
    f0 = model(e)[0]
    for c in range(C):
        d = e.copy(); d[c] *= (1 + eps) if e[c] > 0 else 1
        J[:, c] = (model(d)[0] - f0) / eps if e[c] > 0 else 0
    return J


def jacobian_all(model, E, eps=0.02):
    """Batched: (R, 3, C) sensitivity of Lab to a relative change in each ink, at each region."""
    R_, C_ = E.shape
    base = model(E)                                              # (R, 3)
    J = np.zeros((R_, 3, C_))
    for c in range(C_):
        D = E.copy(); D[:, c] *= (1 + eps)
        J[:, :, c] = (model(D) - base) / eps
    return J


# ---------------------------------------------------------------- the advisor
def advise(model, E, p_meas, m_target, bound=0.25, lam=1e-3):
    """Find per-channel relative changes delta (C,) minimising sum_r dE00(p_r + J_r*delta, m_r)^2.
    Local linear model anchored to the *measured* production tile."""
    Js = jacobian_all(model, E)
    def resid(d):
        pred = np.array([p_meas[r] + Js[r] @ d for r in range(R)])
        return np.concatenate([DE(pred, m_target), np.sqrt(lam) * d * 10])
    sol = least_squares(resid, np.zeros(C), bounds=(-bound, bound))
    return sol.x


# ---------------------------------------------------------------- one SKU re-run event
def make_event(dev, rng, drift_gain=0.15, drift_off=0.25):
    E = tile_inks(rng)
    master = dev.lab(E)                                  # master tile as originally approved
    gain = 1 + rng.normal(0, drift_gain, C)              # ink lot / kiln drift since then
    off = rng.normal(0, drift_off, 3)
    return E, master, gain, off


def print_measure(dev, E, gain, off, delta, rng, sigma_rep, sigma_meas=0.15):
    """Print the file with channel changes `delta`, fire, measure. sigma_rep = same-file
    print+fire repeatability (the week-2 gate), sigma_meas = instrument noise."""
    lab = dev.lab(E * (1 + delta), gain, off)
    return lab + rng.normal(0, sigma_rep, lab.shape[:1] + (3,)) + rng.normal(0, sigma_meas, (len(E), 3))


def passes(true_lab, master):
    d = DE(true_lab, master)
    return d.mean() <= TOL_MEAN and d.max() <= TOL_MAX


def advisor_event(dev, model, rng, sigma_rep, max_rounds=4):
    E, master, gain, off = make_event(dev, rng)
    delta = np.zeros(C)
    p = print_measure(dev, E, gain, off, delta, rng, sigma_rep)   # first sample (fails, usually)
    de0 = DE(p, master).mean()
    for rnd in range(1, max_rounds + 1):
        d_step = advise(model, E * (1 + delta), p, master)   # ink amounts as currently printed
        delta = (1 + delta) * (1 + d_step) - 1
        p = print_measure(dev, E, gain, off, delta, rng, sigma_rep)   # confirmation tile
        if passes(p, master):
            return rnd, DE(p, master).mean(), de0
    return max_rounds + 1, DE(p, master).mean(), de0


def manual_event(dev, rng, sigma_rep, sigma_eye=0.8, max_rounds=8, variants=7):
    """Straw-man of today's loop: QC picks a channel by eye, tries 6-7 variants in 5% steps
    around the current best, judges them by eye (noisy), picks one; lab measures; repeat."""
    E, master, gain, off = make_event(dev, rng)
    best = np.zeros(C)
    p = print_measure(dev, E, gain, off, best, rng, sigma_rep)
    de0 = DE(p, master).mean()
    for rnd in range(1, max_rounds + 1):
        cands = []
        for _ in range(variants):
            d = best.copy()
            for c in rng.choice(C, size=rng.integers(1, 3), replace=False):
                d[c] += rng.choice([-0.10, -0.05, 0.05, 0.10])
            cands.append(d)
        meas = [print_measure(dev, E, gain, off, d, rng, sigma_rep) for d in cands]
        seen = [DE(m + rng.normal(0, sigma_eye, m.shape), master).mean() for m in meas]  # judged by eye
        k = int(np.argmin(seen)); best = cands[k]
        if passes(meas[k], master):
            return rnd, DE(meas[k], master).mean(), de0
    return max_rounds + 1, DE(meas[k], master).mean(), de0


def naive_event(dev, model, rng, sigma_rep, max_rounds=4):
    """Rule-of-thumb baseline: one knob. Scale ALL inks by the same factor to cancel the mean
    lightness gap (what a 'brown a bit lighter, add 5%' habit amounts to), then re-measure."""
    E, master, gain, off = make_event(dev, rng)
    delta = np.zeros(C)
    p = print_measure(dev, E, gain, off, delta, rng, sigma_rep)
    de0 = DE(p, master).mean()
    for rnd in range(1, max_rounds + 1):
        cur = E * (1 + delta)
        dL_ds = jacobian_all(model, cur)[:, 0, :].sum(1).mean()   # dL per unit uniform change
        s = np.clip(-(p[:, 0] - master[:, 0]).mean() / dL_ds, -0.25, 0.25)
        delta = (1 + delta) * (1 + s) - 1
        p = print_measure(dev, E, gain, off, delta, rng, sigma_rep)
        if passes(p, master):
            return rnd, DE(p, master).mean(), de0
    return max_rounds + 1, DE(p, master).mean(), de0


def advisor_trace(dev, model, rng, sigma_rep, rounds=3):
    """Mean dE00 after each round for one event (round 0 = first failed sample)."""
    E, master, gain, off = make_event(dev, rng)
    delta = np.zeros(C)
    p = print_measure(dev, E, gain, off, delta, rng, sigma_rep)
    tr = [DE(p, master).mean()]
    for _ in range(rounds):
        d_step = advise(model, E * (1 + delta), p, master)
        delta = (1 + delta) * (1 + d_step) - 1
        p = print_measure(dev, E, gain, off, delta, rng, sigma_rep)
        tr.append(DE(p, master).mean())
    return tr
