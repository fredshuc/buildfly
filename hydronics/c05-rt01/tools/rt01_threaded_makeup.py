"""RT01-M: can each welded assembly actually be screwed in?

A threaded joint is made up by rotating one side about the thread axis.
Weldments = spools + headers + the custom connectors welded to them (welded
groups found by matching faces). End interfaces (C05 INSTALLED_CONNECTIONS):
  RP1_W33 female onto the frozen HX R1 male: the weldment must rotate
  NPT1_W33 male into a valve/FS body: the weldment or the body must rotate
  R1_W33 male into a ZR union tail: the loose tail rotates (no weldment turn)
  UF_G1 / UF_G15 flat-face union nut: no rotation
A weldment can be turned for at most one threaded joint, and only while its
other ends are free; a second weldment-rotation end makes it non-assemblable
unless a 2-port body between weldments can be turned instead (counted
separately). 68 service ends to commodities are excluded (commodity turns).
"""
import collections
from rt01_common import design, headers, connections, save_csv, save_json


def key(p):
    return tuple(round(x, 2) for x in p)


if __name__ == "__main__":
    d = design(); R = d["pipe_routes"]; H = headers(); C = connections()
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)
    face_owner = {}
    for n, h in H.items():
        face_owner[key(h["main_face"])] = ("H", n)
        for b in h["branch_ports"]:
            face_owner[key(b["face"])] = ("H", n)
    conn_face = {key(c["weld_face"]): p for p, c in C.items()}
    ends = collections.defaultdict(list)
    for e, r in R.items():
        find(("S", e))
        for p in (r["points"][0], r["points"][-1]):
            k = key(p)
            if k in face_owner:
                union(("S", e), face_owner[k])
            elif k in conn_face:
                ends[("S", e)].append(conn_face[k])
    for n, h in H.items():
        find(("H", n))
        if h["root_interface"].startswith("C05_CONN"):
            port = next(p for p, c in C.items() if c["installed_id"] == h["root_interface"])
            ends[("H", n)].append(port)
    groups = collections.defaultdict(lambda: dict(members=[], ends=[]))
    for m in list(parent):
        g = groups[find(m)]; g["members"].append(m[1]); g["ends"] += [(p, C[p]["family"]) for p in ends.get(m, [])]
    rows = []
    for g in groups.values():
        fam = collections.Counter(f for _, f in g["ends"])
        must_turn = fam["RP1_W33"]
        maybe_turn = fam["NPT1_W33"]
        status = ("NOT_ASSEMBLABLE" if must_turn >= 2 else
                  "NEEDS_BODY_TURN" if must_turn + maybe_turn >= 2 else "OK")
        rows.append(dict(weldment="+".join(sorted(g["members"])), n_members=len(g["members"]),
                         ends=";".join(f"{p}:{f}" for p, f in g["ends"]), RP1_to_HX=must_turn, NPT1=maybe_turn,
                         R1_to_ZR=fam["R1_W33"], unions_G=fam["UF_G1"] + fam["UF_G15"], status=status))
    rows.sort(key=lambda r: r["status"])
    save_csv("rt01_threaded_makeup.csv", rows)
    c = collections.Counter(r["status"] for r in rows)
    print(dict(c), "weldments:", len(rows))
    for r in rows:
        if r["status"] != "OK" or r["RP1_to_HX"]:
            print(r["status"], r["weldment"], "|", r["ends"])


def strict(rows, R):
    """C05 sequence (all hot work before commodities): a threaded joint can be
    made only by turning (a) a loose union tail, (b) a free 2-port body, or
    (c) a straight single-spool weldment (axisymmetric about the thread)."""
    def straight(w):
        m = w["weldment"].split("+")
        return len(m) == 1 and m[0] in R and not R[m[0]]["bend_radii"]
    by_port = {}
    for w in rows:
        for item in w["ends"].split(";"):
            if item:
                p, f = item.rsplit(":", 1); by_port[p] = (w, f)
    bad = []
    for p, (w, f) in by_port.items():
        if f == "RP1_W33" and not straight(w):
            bad.append((p, "HX R1/Rp1: 3D weldment must turn"))
    bodies = collections.defaultdict(list)
    for p, (w, f) in by_port.items():
        if f == "NPT1_W33":
            bodies[p.split(":")[0]].append((p, w))
    for b, pp in bodies.items():
        if len(pp) == 2 and not any(straight(w) for _, w in pp):
            bad.append((pp[1][0], f"NPT body {b}: body turn used on {pp[0][0]}, other side 3D weldment"))
    return bad


if __name__ == "__main__":
    bad = strict(rows, R)
    print("not makeable under C05 hot-work-first sequence:", len(bad))
    for b in bad:
        print("  ", b)
    save_json("rt01_threaded_makeup_strict.json", dict(count=len(bad), joints=bad))
