"""RT01-F: fabricability of the 386 single-cut 90 deg miters, piece by piece.

For each straight piece of each spool, compute the shortest generator (outer
surface line) between its two cut planes. A single-cut 90 deg miter plane at a
corner with incoming direction a and outgoing u has normal (a-u)/|a-u|. For a
piece of centreline length L with neighbours a (before) and b (after):
  generator(w) = L + w.(b - a),  |w| = OD/2, w perpendicular to the piece,
so g_min = L - r*|b - a|  (Z-jog |b-a|=0, out-of-plane sqrt2, U-turn 2).
At a square-cut terminal end the term for that side is r*|a| = r.
g_min <= 0 means the piece cannot exist; small g_min means two welds that are
closer than any practical fit-up, purge and torch/orbital-head access allow.
"""
import math, collections
from rt01_common import design, save_csv, save_json

WELD_GAP_LIMITS = (0.0, 10.0, 25.0)  # mm: impossible / unweldable / manual-only


def pieces():
    d = design()
    out = []
    for eid, r in d["pipe_routes"].items():
        P = r["points"]
        rad = r["OD_mm"] / 2
        segs = []
        for p, q in zip(P, P[1:]):
            v = [b - a for a, b in zip(p, q)]
            L = math.sqrt(sum(x * x for x in v))
            segs.append((L, [x / L for x in v]))
        n = len(segs)
        for i, (L, u) in enumerate(segs):
            a = segs[i - 1][1] if i > 0 else None
            b = segs[i + 1][1] if i < n - 1 else None
            # each side contributes r*|projection| ; build vector b - a with
            # square ends treated as a unit side term of r
            if a is not None and b is not None:
                diff = [y - x for x, y in zip(a, b)]
                k = math.sqrt(sum(x * x for x in diff))
                shape = {0: "Z_JOG", 1: "OUT_OF_PLANE", 2: "U_TURN"}[round(k * k / 2)]
                gmin = L - rad * k
            elif a is None and b is None:
                shape, gmin = "STRAIGHT", L
            else:
                shape, gmin = "TERMINAL", L - rad
            out.append(dict(edge=eid, kind=r["kind"], OD_mm=r["OD_mm"], piece=i + 1,
                            pieces_in_spool=n, centreline_mm=round(L, 3), shape=shape,
                            min_generator_mm=round(gmin, 3),
                            weld_to_weld_class=("IMPOSSIBLE" if gmin <= 0 else
                                                "UNWELDABLE_<10" if gmin < 10 else
                                                "MANUAL_ONLY_<25" if gmin < 25 else "OK_>=25")))
    return out


if __name__ == "__main__":
    pp = pieces()
    save_csv("rt01_miter_pieces.csv", pp)
    c = collections.Counter(p["weld_to_weld_class"] for p in pp)
    by = collections.defaultdict(collections.Counter)
    for p in pp:
        by[p["OD_mm"]][p["weld_to_weld_class"]] += 1
    spools_bad = sorted({p["edge"] for p in pp if p["min_generator_mm"] < 10})
    summ = dict(pieces=len(pp), classes=dict(c), by_OD={str(k): dict(v) for k, v in by.items()},
                spools_with_piece_below_10mm=len(spools_bad), spools=spools_bad,
                worst=sorted(pp, key=lambda p: p["min_generator_mm"])[:15])
    save_json("rt01_miter_pieces_summary.json", summ)
    print(dict(c)); print({k: dict(v) for k, v in by.items()})
    print("spools with a piece <10 mm:", len(spools_bad))
    for p in summ["worst"]:
        print(p)
