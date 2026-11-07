"""Continuous rotation certificate against actual C11 fixed components.

Distance is 1-Lipschitz under the conservative maximum point displacement
R*dtheta. Positive clearance at the midpoint greater than R*half-interval
certifies the complete interval. Unresolved intervals are never called PASS.
"""
from integrate import *
def run():
    folder,rows=cache_scene('S1');fixed=[r for r in rows if r['group']!='DAMPERS'];cache={}
    p=named(D05/'cad/C11_D05_DAMPERS_NORMALIZED_P.step');out=[]
    for n,s in p.items():
        if not moving(n):continue
        tag=next((f'{b}_{l}' for b in 'AB' for l in ('LOWER','UPPER') if f'{b}_{l}' in n),None)
        if not tag:continue
        x,z=(610,342) if 'LOWER' in tag else (-500,1385);b=bb(s)
        radius=max(math.hypot(xx-x,zz-z) for xx in (b[0],b[3]) for zz in (b[2],b[5]))
        broad=[x-radius,b[1],z-radius,x+radius,b[4],z+radius]
        candidates=[r for r in fixed if overlap(broad,r['bbox'],-1e-5)]
        poses={}
        def pose(deg):
            if deg not in poses:poses[deg]=s.rotate((x,0,z),(x,1,z),deg)
            return poses[deg]
        for r in candidates:
            if not r.get('valid',True):
                out.append({'moving':n,'fixed_group':r['group'],'fixed':r['name'],'status':'INVALID_TARGET_NOT_CERTIFIED','pose_queries':0,'minimum_sampled_distance_mm':None,'certified_distance_lower_bound_mm':None,'failure':'Installed solid failed validity; no geometric clearance certificate assigned'})
                continue
            k=r['file']
            if k not in cache:cache[k]=cq.Shape.importBrep(str(folder/k))
            target=cache[k];stack=[(0.,ANGLE)];steps=0;status='CERTIFIED_CLEAR';minlower=float('inf');sample=float('inf');failure=None
            while stack:
                lo,hi=stack.pop();mid=(lo+hi)/2;t=pose(mid);d=t.distance(target);steps+=1;sample=min(sample,d)
                bound=radius*math.radians((hi-lo)/2)
                if d>bound+1e-6:minlower=min(minlower,d-bound);continue
                v=t.intersect(target).Volume()
                if v>.001:status='COLLISION';failure={'angle_deg':mid,'volume_mm3':v};break
                if hi-lo<=.002 or steps>=2048:status='UNRESOLVED_INTERVAL';failure={'interval_deg':[lo,hi],'mid_distance_mm':d,'point_motion_bound_mm':bound};break
                stack.extend([(lo,mid),(mid,hi)])
            out.append({'moving':n,'fixed_group':r['group'],'fixed':r['name'],'status':status,'pose_queries':steps,'minimum_sampled_distance_mm':sample,'certified_distance_lower_bound_mm':minlower if status=='CERTIFIED_CLEAR' else None,'failure':failure})
        print('Motion',n,len(candidates),'nonclear',sum(r['status']!='CERTIFIED_CLEAR' for r in out if r['moving']==n),flush=True)
        dump(E/'motion_delta.json',{'status':'IN_PROGRESS','pairs':out})
    dump(E/'motion_delta.json',{'status':'NONCLEAR_PAIRS_PRESENT' if any(r['status']!='CERTIFIED_CLEAR' for r in out) else 'CERTIFIED_GEOMETRY_CLEAR_WITHIN_SCOPE','installed_S1_sha256':sha(CAD/'C11_INSTALLED_S1.step'),'interval_deg':[0,ANGLE],'method':'Midpoint exact shape distance with R*dtheta displacement bound; nonclear terminal intervals are unresolved, not passes','scope':'Every moving D05 component against all six non-DAMPERS installed groups. D05 internal pairs and asynchronous rotor-to-rotor checks remain pinned owner evidence. No tolerance, thermal or loaded-shape release follows from nominal geometry.','pairs':out})
if __name__=='__main__':run()
