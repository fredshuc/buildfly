"""Closed-form RT4 calculations (SI unless stated). Usage: python c09_calcs.py <out.json>
Inputs are package coordinates (D03_SEAT_APERTURES.csv, PLACEMENTS.json, D03_AXES.csv, air_sections.csv)
plus explicitly labelled assumptions."""
import json, sys, math
rho = 1.18
Q_P = 4870 / 3600            # [A] C06/C07 design point; no four-core flow is stated in C09/D03
fin_face = 1.000 * 0.61015   # PLACEMENTS.json fin X -410..590, Y 127.425..737.575
apert = 0.630 * 0.180        # D03_SEAT_APERTURES: Pin/Pout 630 x 180.0; Rin/Rout sloped 630 x 180.0
rin_throat = 0.630 * 0.135364  # air_sections.csv min Rin clear height; 630 mm width assumed (seat span)
def v(Q, A): return Q / A
def qd(V): return 0.5 * rho * V * V
out = {}
for name, A in (('fin_face', fin_face), ('damper_aperture', apert), ('Rin_throat', rin_throat)):
    out[name] = {'area_m2': round(A, 4), 'v_per_1000m3h_ms': round(v(1000 / 3600, A), 3),
                 'v_at_4870_ms': round(v(Q_P, A), 2), 'q_at_4870_Pa': round(qd(v(Q_P, A)), 1),
                 'v_at_2435_ms': round(v(Q_P / 2, A), 2), 'q_at_2435_Pa': round(qd(v(Q_P / 2, A)), 1)}
out['fin_face']['fpm_at_4870'] = round(out['fin_face']['v_at_4870_ms'] * 196.85, 0)
# lower selector shafts: A Y -893..-8 (885 mm), B Y -7..893 (900 mm), nominal end gap 1.000 mm
gap = 1.000; LA, LB = 0.885, 0.900
th = {}
for mat, a in (('carbon steel', 11.7e-6), ('stainless 304', 17.3e-6)):
    for dT in (40, 70):
        th[f'{mat}, one shaft hot dT={dT}K'] = round(a * dT * LB * 1000, 3)
        th[f'{mat}, both shafts dT={dT}K'] = round(a * dT * (LA + LB) * 1000, 3)
out['lower_shaft_end_gap'] = {'nominal_gap_mm': gap, 'closure_mm': th,
    'ISO2768m_length_tol_400_1000_mm': 0.8,
    'note': 'axial location at the outboard bearing (README_CN: shoulder + lock ring), so growth closes the central gap'}
# face seal: 2 mm nominal, footprint 41,741.78 mm2 per ring (Final_Red_Team_EN.md)
out['face_seal'] = {'thickness_mm': 2.0, 'working_stroke_25_40pct_mm': [0.5, 0.8],
    'perimeter_estimate_m': round(2 * (1.000 + 0.61015), 3), 'implied_land_width_mm': round(41741.78 / (2 * (1000 + 610.15)), 1)}
# upper seat vs upper-core W2 end pipe (probe_seat_vs_endpipe_S1.json)
out['upper_seat_vs_W2_pipe'] = {'seat_bottom_Z': 1133.0, 'pipe_top_Z_A': 1139.48, 'pipe_top_Z_B': 1139.85,
    'penetration_mm_A': round(1139.48 - 1133.0, 2), 'penetration_mm_B': round(1139.85 - 1133.0, 2),
    'Pin_aperture_bottom_Z': 1174.9925, 'flange_below_aperture_mm': round(1174.9925 - 1133.0, 2)}
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
