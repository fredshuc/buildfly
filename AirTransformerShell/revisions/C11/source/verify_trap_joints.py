"""Check the real fishmouth and its exported joint, including the former no-op cut."""
from integrate import *
from intersection_tools import common_volume

def run():
    folder,installed=cache_scene('S1');design=json.loads((WORK/'shell/index.json').read_text());results=[]
    for bed in 'AB':
        for level in ['LOWER','UPPER']:
            pre=f'C11_{bed}_{level}_COND';names=[pre+'_TRAP_PIPE',pre+'_SIPHON_BREAK_STUB'];versions={}
            for label,rows,root in [('design',design,WORK/'shell'),('installed',installed,folder)]:
                shapes=[cq.Shape.importBrep(str(root/next(r['file'] for r in rows if r['name']==n))) for n in names]
                a,b=shapes;removed=math.pi*(9**2-8**2)*45-b.Volume()
                versions[label]={'volumes_mm3':[s.Volume() for s in shapes],'bbox':[bb(s) for s in shapes],'stub_fishmouth_removed_mm3':removed,'common_mm3':common_volume(a,b,*names),'all_valid':all(s.isValid() for s in shapes)}
            x,y=versions['design'],versions['installed']
            assert all(v['stub_fishmouth_removed_mm3']>300 and v['common_mm3']<.001 and v['all_valid'] for v in versions.values()),pre
            differences=[abs(u-v) for u,v in zip(x['volumes_mm3'],y['volumes_mm3'])]
            tolerances=[max(.001,abs(u)*1e-6) for u in x['volumes_mm3']]
            # STEP reparameterisation changes numerical volume quadrature;
            # use the same 1ppm envelope as the H02 export normalization.
            # This does not relax the 0.001mm3 intersection threshold.
            assert all(d<=t for d,t in zip(differences,tolerances)),(pre,differences,tolerances)
            bbox_difference=max(abs(u-v) for a,b in zip(x['bbox'],y['bbox']) for u,v in zip(a,b))
            assert bbox_difference<1e-5,(pre,bbox_difference)
            results.append({'joint':pre,'nominal_root_gap_mm':.15,'branch_bore_mm':16.2,'versions':versions,'volume_differences_mm3':differences,'volume_tolerances_mm3':tolerances,'max_exact_bbox_difference_mm':bbox_difference,'status':'PASS_GEOMETRY_AND_STEP_ROUNDTRIP_ONLY'})
    dump(E/'trap_joint_export_check.json',{'installed_S1_sha256':sha(CAD/'C11_INSTALLED_S1.step'),'shell_index_sha256':sha(WORK/'shell/index.json'),'status':'PASS','joints':results,'limitation':'Thin-wall welding procedure, bore finish, leakage and service qualification remain open; this is not a weld acceptance.'})
    print('Four fishmouth joints: real material removal and STEP roundtrip PASS',flush=True)
if __name__=='__main__':run()
