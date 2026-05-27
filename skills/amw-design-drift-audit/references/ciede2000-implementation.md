# CIEDE2000 ΔE — pure-Python reference implementation

A self-contained CIEDE2000 implementation for the color-drift detection in `references/audit-procedure.md` §Phase 1. No external dependencies — uses only the Python standard library (`math`).

CIEDE2000 is the CIE-recommended successor to CIE76 and CIE94. It corrects perceptual non-uniformity in the L*a*b* space for blue colors and near-neutral grays. Threshold guide:

| ΔE | Perceptibility |
|---|---|
| <1.0 | Not perceptible by human eye |
| 1.0 – 2.0 | Perceptible through close observation |
| 2.0 – 10.0 | Perceptible at a glance |
| 11 – 49 | Colors are more similar than opposite |
| 100 | Exact opposite |

The audit flags any pair with ΔE<3.0 as a drift candidate.

## Implementation

```python
import math

# --- Step 1: hex / rgb / hsl input → sRGB linear → CIE XYZ → CIE LAB ---

def hex_to_rgb(hex_str: str) -> tuple[float, float, float]:
    """Hex like '#2563eb' or '2563eb' → (r, g, b) in [0..255]."""
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"bad hex: {hex_str!r}")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def rgb_to_linear(c: float) -> float:
    """sRGB gamma → linear. c in [0..1]."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rgb_to_xyz(r: float, g: float, b: float) -> tuple[float, float, float]:
    """RGB [0..255] → CIE XYZ (D65)."""
    rl = rgb_to_linear(r / 255.0)
    gl = rgb_to_linear(g / 255.0)
    bl = rgb_to_linear(b / 255.0)
    x = (rl * 0.4124564 + gl * 0.3575761 + bl * 0.1804375) * 100.0
    y = (rl * 0.2126729 + gl * 0.7151522 + bl * 0.0721750) * 100.0
    z = (rl * 0.0193339 + gl * 0.1191920 + bl * 0.9503041) * 100.0
    return (x, y, z)


def xyz_to_lab(x: float, y: float, z: float) -> tuple[float, float, float]:
    """CIE XYZ (D65) → CIE L*a*b*."""
    # D65 reference white
    xn, yn, zn = 95.047, 100.000, 108.883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx = f(x / xn)
    fy = f(y / yn)
    fz = f(z / zn)

    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)
    return (L, a, b)


def hex_to_lab(hex_str: str) -> tuple[float, float, float]:
    r, g, b = hex_to_rgb(hex_str)
    x, y, z = rgb_to_xyz(r, g, b)
    return xyz_to_lab(x, y, z)


# --- Step 2: CIEDE2000 ---

def ciede2000(lab1: tuple[float, float, float], lab2: tuple[float, float, float]) -> float:
    """
    CIEDE2000 color difference.
    Returns ΔE — 0 = identical, ~2 = very close, ~5 = obvious, ~10+ = different.
    Reference: Sharma, Wu, Dalal (2005) "The CIEDE2000 Color-Difference Formula".
    """
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2

    # Constants
    kL = kC = kH = 1.0

    C1 = math.hypot(a1, b1)
    C2 = math.hypot(a2, b2)
    Cbar = (C1 + C2) / 2.0

    G = 0.5 * (1 - math.sqrt(Cbar ** 7 / (Cbar ** 7 + 25 ** 7)))

    a1p = (1 + G) * a1
    a2p = (1 + G) * a2

    C1p = math.hypot(a1p, b1)
    C2p = math.hypot(a2p, b2)

    def hp(ap: float, b: float) -> float:
        if ap == 0 and b == 0:
            return 0.0
        h = math.degrees(math.atan2(b, ap))
        return h + 360.0 if h < 0 else h

    h1p = hp(a1p, b1)
    h2p = hp(a2p, b2)

    dLp = L2 - L1
    dCp = C2p - C1p

    if C1p * C2p == 0:
        dhp = 0.0
    else:
        diff = h2p - h1p
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360
        dhp = diff

    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2)

    Lpbar = (L1 + L2) / 2.0
    Cpbar = (C1p + C2p) / 2.0

    if C1p * C2p == 0:
        hpbar = h1p + h2p
    else:
        s = h1p + h2p
        d = abs(h1p - h2p)
        if d <= 180:
            hpbar = s / 2.0
        else:
            hpbar = (s + 360) / 2.0 if s < 360 else (s - 360) / 2.0

    T = (1
         - 0.17 * math.cos(math.radians(hpbar - 30))
         + 0.24 * math.cos(math.radians(2 * hpbar))
         + 0.32 * math.cos(math.radians(3 * hpbar + 6))
         - 0.20 * math.cos(math.radians(4 * hpbar - 63)))

    dTheta = 30 * math.exp(-(((hpbar - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(Cpbar ** 7 / (Cpbar ** 7 + 25 ** 7))
    Sl = 1 + (0.015 * (Lpbar - 50) ** 2) / math.sqrt(20 + (Lpbar - 50) ** 2)
    Sc = 1 + 0.045 * Cpbar
    Sh = 1 + 0.015 * Cpbar * T
    Rt = -math.sin(math.radians(2 * dTheta)) * Rc

    dE = math.sqrt(
        (dLp / (kL * Sl)) ** 2
        + (dCp / (kC * Sc)) ** 2
        + (dHp / (kH * Sh)) ** 2
        + Rt * (dCp / (kC * Sc)) * (dHp / (kH * Sh))
    )

    return dE


# --- Usage in the audit ---

def cluster_colors(hex_colors: list[str], threshold: float = 3.0) -> list[list[str]]:
    """
    Group hex colors by CIEDE2000 ΔE < threshold.
    Returns a list of clusters; singletons are omitted.
    Uses a simple union-find — O(n²) for the pair scan, fine for token sets of <500 colors.
    """
    if not hex_colors:
        return []

    labs = [hex_to_lab(h) for h in hex_colors]
    n = len(hex_colors)
    parent = list(range(n))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj

    for i in range(n):
        for j in range(i + 1, n):
            if ciede2000(labs[i], labs[j]) < threshold:
                union(i, j)

    clusters: dict[int, list[str]] = {}
    for i, h in enumerate(hex_colors):
        clusters.setdefault(find(i), []).append(h)

    return [c for c in clusters.values() if len(c) >= 2]
```

## Validation

Sanity check the implementation against published reference pairs from Sharma, Wu, Dalal (2005) Table 1:

```python
# (L1,a1,b1), (L2,a2,b2), expected_dE
test_pairs = [
    ((50.0000, 2.6772, -79.7751), (50.0000, 0.0000, -82.7485), 2.0425),
    ((50.0000, 3.1571, -77.2803), (50.0000, 0.0000, -82.7485), 2.8615),
    ((50.0000, 2.8361, -74.0200), (50.0000, 0.0000, -82.7485), 3.4412),
    ((50.0000, -1.3802, -84.2814), (50.0000, 0.0000, -82.7485), 1.0000),
]
for lab1, lab2, expected in test_pairs:
    got = ciede2000(lab1, lab2)
    assert abs(got - expected) < 0.0001, f"ΔE mismatch: got {got}, expected {expected}"
```

If the reference implementation in a future bin script disagrees with these published values by more than 0.0001, the bug is in the bin script — not the test data.

## Why CIEDE2000 instead of CIE76 / Lab Euclidean

CIE76 (plain Lab Euclidean distance) over-weights near-neutral grays and blues. A pair `(#000010, #100000)` has small Lab Euclidean but obvious visual difference; a pair `(#2563eb, #2864ec)` has the opposite — CIE76 says they're far apart, but a human eye barely sees a difference. CIEDE2000 corrects both and is the current CIE recommendation. The extra math is worth it for token-drift detection because designers DO operate in the perceptual regime where CIE76 is wrong.
