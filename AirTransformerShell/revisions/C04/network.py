"""Reduced pressure network; explicitly imposed pressure variations, no CFD."""
from design import *
import json, csv, itertools
import numpy as np
from scipy.optimize import brentq
from pathlib import Path
OUT=Path(__file__).parent
rho,cd=1.18,.65
clear_pitch=DEPTH/N/sqrt(1+SLOPE**2)-T
ach=W*clear_pitch/1e6
af=W*BAND/1e6
dh=2*W*clear_pitch/(W+clear_pitch)/1000
q0=4870/3600/N
length=np.array([path_length(i)/1000 for i in range(N)])
def duct_loss(f):
    # Combined entrance, turning, exit losses for supply and return. Assumed K.
    return rho/2*(q0/ach)**2*(1.8+2*f*length/dh)
def screens(d,c):
    phi=120*np.pi*d**2/4/(W*BAND)
    return rho*(q0/af/(c*phi))**2   # two faces, referenced to gross face speed
loss=duct_loss(.03)
target=loss.max()+screens(20.,cd)
diam=(20*(screens(20,cd)/(target-loss))**.25).round(1)
def run(flow,f=.03,c=cd,hx=60,bias=0,side=0):
    # Parallel 8 x 12 face patches. Each patch represents an equal part of a band.
    # Face-width pressure gradient is prescribed, not computed from the inlet jet.
    k=(duct_loss(f)+screens(diam,c)+hx)[:,None]
    height=np.linspace(-1,1,8)[:,None];width=np.linspace(-1,1,12)[None,:]
    delta=bias*height+side*width
    r=flow/4870
    def rates(p):return np.sqrt(np.maximum(p+delta*r*r,0)/k)
    p=brentq(lambda p:rates(p).mean()-r,0.,1e4)
    a=rates(p)/r
    return dict(dp_pa=round(p,2),cv_pct=round(a.std()*100,3),min_mean=round(a.min(),4),max_mean=round(a.max(),4))
if __name__=='__main__':
    cases=[]
    for mode,flow in [('P forward',4870),('P reverse',4870),('R forward example',2435),('R reverse example',2435)]:
        sg=-1 if 'reverse' in mode else 1
        cases.append(dict(mode=mode,flow_m3h=flow,nominal=run(flow),example_gradient=run(flow,bias=sg*12,side=sg*8)))
    stress=[run(4870,f,c,h,b,s) for f,c,h,b,s in itertools.product([.018,.05],[.58,.72],[0,60,120],[-20,20],[-10,10])]
    checks=dict(assumptions=dict(rho_kg_m3=rho,orifice_Cd=cd,hx_nominal_Pa=60,full_flow_m3h=4870,regen_comparison_only_m3h=2435,stress_band_width_differential_pressure_Pa_at_full_flow=[20,10],assumed_minor_K_two_paths=1.8),length_m=length.tolist(),diameter_mm=diam.tolist(),branch_and_screens_Pa_at_equal_flow=(loss+screens(diam,cd)).tolist(),cases=cases,stress=dict(n=len(stress),cv_max_pct=max(v['cv_pct'] for v in stress),lowest=min(v['min_mean'] for v in stress),highest=max(v['max_mean'] for v in stress)))
    (OUT/'flow_checks.json').write_text(json.dumps(checks,indent=2))
    print(checks)
