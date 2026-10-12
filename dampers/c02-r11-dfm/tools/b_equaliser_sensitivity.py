"""Re-implementation of the R11 B three-DOF control model (r11_controls.py logic, unchanged
constitutive laws) with the spherical-seat friction radius exposed as a parameter, to test the
DFM option of replacing the custom SR20 seat by a standard DIN 6319 C/D pair (SR9 for d1=6.4).
Usage: python -I b_equaliser_sensitivity.py <R9 evidence dir> <out.json>"""
import sys, json, math, copy
import numpy as np
from scipy.optimize import brentq, least_squares

R9 = sys.argv[1]
U = json.load(open(f'{R9}/R9_UNEQUAL_CLAMP_DIAGNOSTIC.json')); r0 = U['max_rotation']
def poly(s):
    def f(x): return x/.5*((.5-x/.5)*(.5-.5*x/.5)+1)
    return 325*f(s)/f(.1875)
def inv(f, m): return brentq(lambda s: 2*m*poly(s)-f, 0, .25)
du = (48+30+6.25)*17.2e-6*80
Es = 185000.; Ibolt = math.pi*4.2**4/64; Iarms = 2*6*8**3/12
kjaw = 3*Es*Iarms/20**3; kaxial = 1/(57/(Es*14.2)+1/kjaw)
def forces(r, d, lam, loss):
    fs = []; ss = []
    for i, (f0, m, tf, sg, ploss) in enumerate(zip([r['F01'], r['F02']], r['curve_factors'], r['temperature_factors'], r['thermal_signs'], r['losses_N'])):
        shift = lam*sg*du-loss*(.01 if sg < 0 else 0)+(-1 if i == 0 else 1)*20*d; s0 = inv(f0, m)
        def trial(F):
            s = s0+(shift-(F-f0)/kaxial)/5
            return max(0, 2*m*(1+lam*(tf-1))*poly(max(0, s))-loss*ploss), s
        F = brentq(lambda F: F-trial(F)[0], 0, 1e5); fs.append(F); ss.append(trial(F)[1])
    return np.array(fs), np.array(ss)
controls = [('MAX_UNEQUAL', r0)]; r2 = copy.deepcopy(r0)
for k in ['thermal_signs', 'curve_factors', 'temperature_factors', 'losses_N']: r2[k] = r2[k][::-1]
r2['F01'], r2['F02'] = r0['F02'], r0['F01']; controls.append(('MIRROR', r2))
for name, f, sg, m, tf, loss in [('LOW_FORCE', 350, -1, .925, .95, 40), ('HIGH_FORCE', 450, 1, 1.25, 1.05, 0)]:
    controls.append((name, dict(F01=f, F02=f, thermal_signs=[sg, sg], curve_factors=[m, m], temperature_factors=[tf, tf], losses_N=[loss, loss])))

def run(r, mu_seat, rolling_arm, R_sphere, R_crown=4.0, kt=1e5):
    kp = 1e5; ks = 2*Es*Ibolt/42.; plastic = np.zeros(4); angles = np.zeros(3); cold = None; peak = 0; out = []
    path = [('COLD', 0., 0.)]+[('HEAT', float(l), 0.) for l in np.linspace(0, 1, 9)[1:]]; prev = 0.
    for T in [30, 0, -30, 0, 300, 0, -300, 0]:
        path += [('TORQUE', 1., float(t)) for t in np.linspace(prev, T, 4)[1:]]; prev = T
    path += [('COOL', float(l), 0.) for l in np.linspace(1, 0, 9)[1:]]
    for phase, lam, T in path:
        peak = max(peak, lam)
        def evaluate(a):
            theta, alpha, beta = a; f, s = forces(r, theta-beta, lam, peak); Q = sum(f); psi = theta-alpha
            roll = np.clip(kp*(psi-plastic[0]), -Q*rolling_arm, Q*rolling_arm)
            seat = np.clip(ks*(theta-beta-plastic[1]), -mu_seat*Q*R_sphere, mu_seat*Q*R_sphere)
            C = -Q*R_crown*psi+roll; D = 20*(f[0]-f[1]); cap = .05/math.sqrt(1+.05**2)*Q*14.9895
            tau = np.clip(kt*(a[1:]-plastic[2:]), -cap, cap)
            return np.array([D-C-seat, tau[0]-C, tau[1]+C-T]), (f, s, Q, roll, seat, C, cap, tau)
        sol = least_squares(lambda a: evaluate(a)[0], angles, xtol=1e-12, ftol=1e-12, gtol=1e-9, max_nfev=300)
        angles = sol.x; res, vals = evaluate(angles)
        if max(abs(res)) > 1e-3:
            for seed in [angles+np.array([1e-4, 0, 1e-4]), angles+np.array([-1e-4, 0, -1e-4]), np.array([angles[0], angles[1], T/kt])]:
                rt = least_squares(lambda a: evaluate(a)[0], seed, xtol=1e-12, ftol=1e-12, gtol=1e-9, max_nfev=300)
                rr, vv = evaluate(rt.x)
                if max(abs(rr)) < 1e-3: angles = rt.x; res, vals = rr, vv; break
        if max(abs(res)) > 1e-3: raise RuntimeError((phase, res))
        f, s, Q, roll, seat, C, cap, tau = vals; theta, alpha, beta = angles
        plastic = np.r_[theta-alpha-roll/kp, theta-beta-seat/ks, angles[1:]-tau/kt]
        if cold is None: cold = angles.copy()
        out.append(dict(phase=phase, enc=math.degrees(beta-cold[2]), Q=Q, res=float(max(abs(res)))))
    th = max(abs(x['enc']) for x in out if x['phase'] in ('HEAT', 'COOL'))
    heat = max(abs(x['enc']) for x in out if x['phase'] == 'HEAT')
    return dict(max_thermal_or_cool_deg=th, pure_heat_deg=heat, residual_deg=out[-1]['enc'],
                max_any_deg=max(abs(x['enc']) for x in out), max_residual_Nmm=max(x['res'] for x in out))

rows = []
for R_s in [20.0, 9.0]:
    for name, r in controls:
        for mu, arm in [(.05, .005), (.12, .030)]:
            res = run(r, mu, arm, R_s); res.update(sphere_radius_mm=R_s, control=name, mu_seat=mu, rolling_arm_mm=arm); rows.append(res)
            print(json.dumps(res))
json.dump(rows, open(sys.argv[2], 'w'), indent=1)
