"""Explicit roof/gland actions; never imply complete Pin/core service closure."""
from integrate import *
def run():
    folder,rows=cache_scene('S1');fixed={r['group']+'/'+r['name']:cq.Shape.importBrep(str(folder/r['file'])) for r in rows}
    development='--development-shell' in sys.argv
    if development:
        fixed={n:s for n,s in fixed.items() if not n.startswith('SHELL/')}
        sr=json.loads((WORK/'shell/index.json').read_text())
        fixed.update({'SHELL/'+r['name']:cq.Shape.importBrep(str(WORK/'shell'/r['file'])) for r in sr})
    normalized=named(D05/'cad/C11_D05_DAMPERS_NORMALIZED_P.step')
    for n,s in normalized.items():
        if moving(n):fixed['DAMPERS/'+n]=s
    boxes={n:bounds(s) for n,s in fixed.items()};results=[];refs={}
    def exact_axial_prism(s,v):
        # Valid only for these documented constant-section X/Z extrusions.
        vec=cq.Vector(*v);end=[f for f in s.Faces() if f.geomType()=='PLANE' and f.normalAt().dot(vec)>vec.Length*.999999]
        assert end
        shapes=[s]+[cq.Solid.extrudeLinear(f.outerWire(),f.innerWires(),vec) for f in end]
        return shapes[0].fuse(*shapes[1:]).clean()
    def check_envelope(label,envelope,absent,scope):
        b=bounds(envelope);hits=[]
        for n,t in fixed.items():
            if n in absent or not overlap(b,boxes[n],-1e-5):continue
            try:v=envelope.intersect(t).Volume()
            except Exception as e:hits.append([n,'KERNEL_ERROR '+str(e)]);continue
            if v>.001:hits.append([n,v])
        results.append({'action':label,'method':'Exact axial-prism sweep or explicitly dimensioned tool body','scope':scope,'removed_or_tool_target':sorted(absent),'hits':hits,'status':'COLLISION' if hits else 'NOMINAL_ENVELOPE_CLEAR'})
        refs[label]=envelope;print(label,len(hits),flush=True)
    roof='SHELL/SKIN_DRY_ROOF_O'
    if roof not in fixed:roof=next(n for n in fixed if n.startswith('SHELL/SKIN_DRY_ROOF'))
    roof_removed={n for n in fixed if n.startswith('SHELL/C11_ROOF_M5_') and n.endswith(('_SCREW','_WASHER','_RENEWABLE_SEAL_CAP'))}
    seam='SHELL/C11_DRY_ROOF_RENEWABLE_SEAM'
    for n,s in fixed.items():
        if not (n.startswith('SHELL/C11_ROOF_M5_') and n.endswith('_SCREW')):continue
        p=s.Center().toTuple();x=(boxes[n][0]+boxes[n][3])/2;y=(boxes[n][1]+boxes[n][4])/2;prefix=n.removesuffix('_SCREW')
        absent={prefix+'_SCREW',prefix+'_WASHER',prefix+'_RENEWABLE_SEAL_CAP',prefix+'_INSERT'}
        tool=cyl(6,90,(x,y,1530),(0,0,1))
        check_envelope(n.split('/')[-1]+'_TOOL',tool,absent,'6mm-radius driver,90mm axial access; cap cut before access; insert/target screw excluded only as tool engagement')
    attached={roof}|{n for n in fixed if n.startswith('SHELL/M401_ROOF_NECK_') or n=='SHELL/ROOF_FLANGE_O'}
    assert len(attached)==6,attached
    sweep=cq.Compound.makeCompound([exact_axial_prism(fixed[n],(0,0,500)) for n in sorted(attached)])
    check_envelope('ROOF_ASSEMBLY_LIFT_Z500',sweep,roof_removed|attached|{seam},'Roof plus four attached neck walls and flange move as one assembly; external duct disconnected first;24 screws/washers/caps removed and seam cut; rated lifting fixture and external duct removal not represented')
    for tag in ['A_L','A_U','B_L','B_U']:
        pre='SHELL/C11_'+tag+'_GLAND';removed={n for n in fixed if n.startswith(pre) and any(t in n for t in ['_BOLT_','_WASHER_','_SLIT_'])}
        for half,sign in [('LOW',-1),('HIGH',1)]:
            n=pre+'_GUARD_'+half;s=fixed[n]
            # Z motion has curved boundaries: use distance/motion-bound proof,
            # not planar-face extrusion, which could omit swept curved material.
            start=s;v=(0,0,sign*90);a=bounds(start);swept=[min(a[i],a[i]+v[i]) for i in range(3)]+[max(a[i+3],a[i+3]+v[i]) for i in range(3)]
            pairs=[]
            for m,t in fixed.items():
                if m in removed|{n} or not overlap(swept,boxes[m],-1e-5):continue
                stack=[(0.,1.)];status='CERTIFIED_CLEAR';sample=None;steps=0
                while stack:
                    lo,hi=stack.pop();mid=(lo+hi)/2;q=start.translate((0,0,v[2]*mid));dist=q.distance(t);steps+=1
                    if dist>90*(hi-lo)/2+1e-6:continue
                    vol=q.intersect(t).Volume()
                    if vol>.001:status='COLLISION';sample={'fraction':mid,'volume_mm3':vol};break
                    if (hi-lo)*90<=.05 or steps>=2048:status='UNRESOLVED';sample={'interval_fraction':[lo,hi],'distance_mm':dist};break
                    stack.extend([(lo,mid),(mid,hi)])
                pairs.append({'fixed':m,'status':status,'evidence':sample})
            results.append({'action':f'{tag}_{half}_GUARD_Z{sign*90}','method':'Exact distance with translation displacement bound','removed_or_tool_target':sorted(removed|{n}),'pairs':pairs,'status':'NONCLEAR_PAIRS' if any(r['status']!='CERTIFIED_CLEAR' for r in pairs) else 'CERTIFIED_CLEAR'})
            check_envelope(f'{tag}_{half}_GUARD_NEG_X20_AFTER_RADIAL',exact_axial_prism(s.translate(v),(-20,0,0)),removed|{n},'Six M4 bolts fully extracted from blind backer and washers removed; slit/splice cut; radial Z90 motion FIRST then X-20; opposite level and all pressure pipework retained')
    save(refs,CAD/'C11_ROOF_GLAND_SERVICE_REFERENCE.step')
    dump(E/('development_service_subset.json' if development else 'service_subset.json'),{'status':'DEVELOPMENT_MIXED_SOURCE_ONLY' if development else 'PARTIAL_SERVICE_SCOPE_ONLY','maintenance_pose':'All D05 shafts P=0; fans/water isolated','installed_source_sha256':sha(CAD/'C11_INSTALLED_S1.step'),'development_shell_source_hashes':json.loads((E/'shell_source_hashes.json').read_text()) if development else None,'actions':results,'unverified':['Roof screw unscrewing and handling fixture','Complete inlet floor/wrap/pocket demountable joints and predecessor removals','Whole-core extraction and temporary support stability','Gland adhesive cleaning/cure access and realistic hand envelope','Drain coupler/clip tools, collection vessel and receptor bracing','Cassette lower-seat predecessor, bridge attachment and temporary stability'],'acceptance':'No complete Pin, core, gland replacement or cassette service PASS is claimed by this subset.'})
if __name__=='__main__':run()
