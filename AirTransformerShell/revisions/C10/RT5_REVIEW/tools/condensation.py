"""Surface temperature of insulated D35 cold pipe vs dew point (cylindrical conduction + outer film).
Usage: python condensation.py <out.json>. Assumptions labelled in output."""
import json, sys, math
r1 = 0.0175; Tw = 5.0                              # pipe OD 35 mm; cold supply 5 C (HYD-S2 bed_duty.csv)
cases = []
for k in (0.034, 0.040):                            # elastomeric foam, W/mK (new / aged-wet)
    for h in (5.0, 8.0):                            # still air in wet bay / mild convection, W/m2K
        for t_mm in (2.0, 5.0, 10.0, 15.0, 19.143, 25.0):
            r2 = r1 + t_mm / 1000
            for Ta, Td in ((32.0, 26.0), (30.0, 24.0), (25.0, 20.0)):
                Rins = math.log(r2 / r1) / (2 * math.pi * k); Rf = 1 / (2 * math.pi * r2 * h)
                Ts = Ta - (Ta - Tw) * Rf / (Rins + Rf)
                cases.append(dict(k=k, h=h, t_mm=t_mm, Ta=Ta, Td=Td, Ts=round(Ts, 2), margin_K=round(Ts - Td, 2)))
def tmin(k, h, Ta, Td):
    for t in [x / 10 for x in range(1, 1000)]:
        r2 = r1 + t / 1000; Rins = math.log(r2 / r1) / (2 * math.pi * k); Rf = 1 / (2 * math.pi * r2 * h)
        if Ta - (Ta - Tw) * Rf / (Rins + Rf) >= Td: return t
req = {f'k={k},h={h},Ta={Ta},Td={Td}': tmin(k, h, Ta, Td) for k in (0.034, 0.040) for h in (5.0, 8.0) for Ta, Td in ((32.0, 26.0), (30.0, 24.0), (25.0, 20.0))}
out = dict(assumptions='Tw=5 C (HYD-S2 cold point); D35 pipe; steady 1-D cylindrical; no vapour-barrier failure; '
           'Ta/Td pairs are illustrative humid-outdoor cases, not a project design condition', min_thickness_mm_for_Ts_ge_Td=req, cases=cases)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
for k, v in req.items(): print(k, v)
for c in cases:
    if c['k'] == 0.034 and c['h'] == 8.0 and c['Td'] == 26.0: print(c)
