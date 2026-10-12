"""Independent R10->R11 native delta (BRep string identity + occurrence count). Usage: python -I native_delta.py <R10 native> <R11 native> <out.json>"""
import sys, json, hashlib, collections
def load(d):
    P = json.load(open(f"{d}/PARAMETRIC_PARTS_C02.json")); O = json.load(open(f"{d}/OCCURRENCES_C02.json"))
    return {p['pn']: hashlib.sha256(p['brep'].encode()).hexdigest() for p in P}, O
a, Oa = load(sys.argv[1]); b, Ob = load(sys.argv[2])
changed = sorted(k for k in a if k in b and a[k] != b[k]); added = sorted(set(b) - set(a)); removed = sorted(set(a) - set(b))
same = sum(1 for k in a if k in b and a[k] == b[k])
pn_prefix = collections.defaultdict(list)
for k in b: pn_prefix[k[:4]].append(k)
collisions = {k: v for k, v in pn_prefix.items() if k in b and len(v) > 1 and any(x != k for x in v) and k in [x for x in v]}
res = dict(R10_definitions=len(a), R11_definitions=len(b), R10_instances=len(Oa), R11_instances=len(Ob), changed=changed,
           added=added, removed=removed, unchanged=same, pn_prefix_collisions={k: sorted(v) for k, v in collisions.items()})
json.dump(res, open(sys.argv[3], 'w'), indent=1); print(json.dumps(res, indent=1))
