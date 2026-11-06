"""One-dimensional Z-manifold model of a vertical coil between two sloped plenums (SI).
Usage: python zflow_manifold.py <out.json>
Process: enters the top of the front plenum, descends, crosses the coil in +X, leaves at the bottom of the rear plenum.
Regeneration: enters the bottom of the rear plenum, ascends, crosses in -X, leaves at the top of the front plenum.
The front plenum depth tapers from D at the top to g at the bottom; the rear plenum is the mirror (g at top, D at bottom).
Header momentum: dividing header static regain k_d*(V1^2-V2^2)/2, combining header loss k_c*(V2^2-V1^2)/2,
plus Darcy wall friction. Coil: dp = 60 Pa*(0.6 v/v0 + 0.4 (v/v0)^2), v0 = 2.21 m/s face velocity.
Inlet-jet momentum at the plenum mouth is NOT modelled (see G0)."""
import json,sys,math
import numpy as np
rho,W,H,N=1.18,0.612,1.0,48
def coil(v):return 60*(0.6*v/2.21+0.4*(v/2.21)**2)
def solve(Q,D,g,kd,kc,f=0.02,taper=True,inlet_top=True):
    z=(np.arange(N)+0.5)/N*H           # band centres from bottom
    dz=H/N
    # front depth at band boundaries: tapered from g (bottom) to D (top) or constant D
    zb=np.linspace(0,H,N+1)
    dF=(g+(D-g)*zb/H) if taper else np.full(N+1,D)
    dR=(D-(D-g)*zb/H) if taper else np.full(N+1,D)
    q=np.full(N,Q/N)
    for it in range(400):
        # header flows at boundaries. P mode: front inlet at top, flow downward; rear outlet at bottom.
        if inlet_top:
            QF=np.array([q[:i].sum() for i in range(N+1)])        # flow in front header crossing boundary i (from above) = sum of bands below
            QR=np.array([q[i:].sum() for i in range(N+1)])        # rear header flow crossing boundary i downward = sum of bands above
        else:  # R mode: rear inlet at bottom flowing up, front outlet at top
            QR=np.array([q[i:].sum() for i in range(N+1)])        # rear flow crossing boundary i upward = bands above
            QF=np.array([q[:i].sum() for i in range(N+1)])        # front flow crossing boundary i upward = bands below
        VF=QF/(W*np.maximum(dF,1e-6));VR=QR/(W*np.maximum(dR,1e-6))
        def dh(d):d=max(d,1e-3);return 2*W*d/(W+d)
        # march pressures from the closed ends. pF at band centres, pR at band centres
        pF=np.zeros(N);pR=np.zeros(N)
        if inlet_top:
            # front: dividing, flowing down from top boundary N. pressure rises downstream by regain, falls by friction
            p=0.0
            for i in range(N-1,-1,-1):
                v1=VF[i+1];v2=VF[i]
                p+=kd*rho/2*(v1**2-v2**2)-f*dz/dh(dF[i+1])*rho/2*v1**2
                pF[i]=p
            # rear: combining, flowing down, outlet at bottom; start at top boundary
            p=0.0
            for i in range(N-1,-1,-1):
                v1=VR[i+1];v2=VR[i]
                p+=-kc*rho/2*(v2**2-v1**2)-f*dz/dh(dR[i])*rho/2*v2**2
                pR[i]=p
        else:
            # rear: dividing, flowing up from bottom boundary 0
            p=0.0
            for i in range(N):
                v1=VR[i];v2=VR[i+1]
                p+=kd*rho/2*(v1**2-v2**2)-f*dz/dh(dR[i])*rho/2*v1**2
                pR[i]=p
            # front: combining, flowing up to outlet at top
            p=0.0
            for i in range(N):
                v1=VF[i];v2=VF[i+1]
                p+=-kc*rho/2*(v2**2-v1**2)-f*dz/dh(dF[i+1])*rho/2*v2**2
                pF[i]=p
        dp=(pF-pR) if inlet_top else (pR-pF)
        # common offset: branch dp = offset + dp_i ; find offset so that sum q = Q
        vface=lambda o:np.array([invcoil(o+x) for x in dp])
        lo,hi=-500,2000
        for _ in range(60):
            mid=(lo+hi)/2
            if (vface(mid)*W*dz).sum()>Q:hi=mid
            else:lo=mid
        qn=vface((lo+hi)/2)*W*dz
        if np.max(np.abs(qn-q))<1e-9*Q:q=qn;break
        q=0.5*q+0.5*qn
    v=q/(W*dz);r=v/v.mean()
    bands=r.reshape(8,-1).mean(1)
    return dict(min_over_mean=round(float(r.min()),4),max_over_mean=round(float(r.max()),4),cv_pct=round(float(r.std()*100),3),
        band8_ratio=[round(float(b),4) for b in bands],header_mouth_velocity_ms=round(Q/(W*D),2),iterations=it)
def invcoil(p):
    if p<=0:return 0.0
    a,b=60*0.6/2.21,60*0.4/2.21**2
    return (-a+math.sqrt(a*a+4*b*p))/(2*b)
out=dict(assumptions=dict(rho=rho,W_m=W,H_m=H,bands=N,coil_dp_Pa_at_2p21='60 (60% linear, 40% quadratic)',friction_f=0.02,
  note='Header model only: inlet-jet momentum, damper wakes and turning at the mouth not resolved'),cases=[])
QP=4870/3600;QR=2435/3600
for D in (0.5,0.6,0.7):
    for g in (0.0,0.01,0.03):
        for kd,kc in ((0.6,1.8),(1.0,2.2)):
            for mode,Q,top in (('P_down_+X',QP,True),('R_up_-X',QR,False)):
                r=solve(Q,D,g,kd,kc,inlet_top=top)
                out['cases'].append(dict(mode=mode,D_mouth_m=D,apex_gap_m=g,k_div=kd,k_comb=kc,taper=True,**r))
    for kd,kc in ((0.6,1.8),(1.0,2.2)):
        r=solve(QP,D,D,kd,kc,taper=False)
        out['cases'].append(dict(mode='P_down_+X',D_mouth_m=D,apex_gap_m=None,k_div=kd,k_comb=kc,taper=False,**r))
tap=[c for c in out['cases'] if c['taper']]
out['summary']=dict(tapered_worst_min=min(c['min_over_mean'] for c in tap),tapered_worst_max=max(c['max_over_mean'] for c in tap),
  tapered_worst_cv=max(c['cv_pct'] for c in tap),
  untapered_worst_min=min(c['min_over_mean'] for c in out['cases'] if not c['taper']),
  untapered_worst_max=max(c['max_over_mean'] for c in out['cases'] if not c['taper']))
print(json.dumps(out['summary'],indent=1))
for c in out['cases']:
    if c['apex_gap_m'] in (0.0,0.03,None) and c['k_div']==0.6:print(c['mode'],c['D_mouth_m'],c['taper'],c['min_over_mean'],c['max_over_mean'],c['cv_pct'],c['header_mouth_velocity_ms'])
json.dump(out,open(sys.argv[1],'w'),indent=1)
