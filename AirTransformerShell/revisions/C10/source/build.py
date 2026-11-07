"""Integrate H01, D04 and HYD-S2; new shell revision, never edit owner parts."""
from common import *
import csv,math,warnings
import faulthandler
faulthandler.enable()
warnings.filterwarnings('ignore',category=FutureWarning)

def cache_host(state):
    src=D04/f'cad/D04_C09R1_INSTALLED_{state}.step'
    target=WORK/('host_'+state); target.mkdir(exist_ok=True)
    idx=target/'index.json'
    if idx.exists():
        data=json.loads(idx.read_text())
        assert data['source_sha256']==sha(src)
        return {g:{n:cq.Shape.importBrep(str(target/f)) for n,f in rows.items()} for g,rows in data['groups'].items()}
    groups={'SHELL':{},'DAMPERS':{}};files={'SHELL':{},'DAMPERS':{}}
    for p,s in leaves(src):
        if '/HEAT_EXCHANGERS' in p:continue
        group='SHELL' if '/SHELL/' in p else 'DAMPERS'
        n=p.split('/')[-1];assert n not in groups[group]
        groups[group][n]=s;file=f'{len(files["SHELL"])+len(files["DAMPERS"]):04}.brep'
        s.exportBrep(str(target/file));files[group][n]=file
    assert {g:len(v) for g,v in groups.items()}=={'SHELL':494,'DAMPERS':244}
    dump(idx,{'source_sha256':sha(src),'groups':files})
    return groups

def strip_profile(nodes,y0,y1,gauge=1.5):
    # Parallel offset lines with true normal gauge and intersected mitres.
    m=[(b[1]-a[1])/(b[0]-a[0]) for a,b in zip(nodes,nodes[1:])]
    sides=[]
    for sign in [-1,1]:
        c=[a[1]-s*a[0]+sign*gauge/2*math.sqrt(1+s*s) for a,s in zip(nodes,m)]
        pts=[(nodes[0][0],m[0]*nodes[0][0]+c[0])]
        for i in range(1,len(nodes)-1):
            x=(c[i]-c[i-1])/(m[i-1]-m[i]);pts.append((x,m[i]*x+c[i]))
        pts.append((nodes[-1][0],m[-1]*nodes[-1][0]+c[-1]));sides.append(pts)
    wire=cq.Wire.makePolygon([cq.Vector(x,y0,z) for x,z in sides[0]+list(reversed(sides[1]))],close=True)
    return cq.Solid.extrudeLinear(wire,[],cq.Vector(0,y1-y0,0)),sides

def top_deck(s):
    b=bb(s)
    # Keep rear inlet notch/feedback pocket and final exit datum. Deepen the
    # final 100 mm of the active coil face by 60 mm, with a constant-gauge roof.
    nodes=[(-251,1330.5+.19262686567164),(420,1261.43971343284),
           (500.389,1243.997),(640,1242.88),(744,1165.048),(748.9,1165.0088)]
    new,edges=strip_profile(nodes,b[1],b[4])
    old=s.intersect(block(-1000,-2000,0,-250,2000,2000))
    return old.fuse(new).clean(),nodes,edges

def side_extension(s,edges):
    b=bb(s)
    # The C09 lifted roof did not extend the inner cheek. Close that mismatch
    # as well as the C10 lift; retain all low shaft holes and frame geometry.
    bottom=[(-250,1330.3),(500,1166.8),(748.9,1164.8088)]
    top=[p for p in edges[1] if p[0]>-250]
    top.insert(0,(-250,1331.3))
    wire=cq.Wire.makePolygon([cq.Vector(x,b[1],z) for x,z in bottom+list(reversed(top))],close=True)
    add=cq.Solid.extrudeLinear(wire,[],cq.Vector(0,b[4]-b[1],0))
    return s.fuse(add).clean()

def thermal_pocket(shell,bed):
    # Four-sided raised corner (open towards the wet bay), nominal 1.5 mm
    # sheet. Two end closures and an inboard return make a closed air wall.
    floor=shell[f'AIR_PROCESS_IN_FLOOR_{bed}_O'];wrap=shell[f'AIR_PROCESS_IN_WRAP_{bed}_O']
    y0=bb(wrap)[1];yi=-744 if bed=='A' else 120
    x0,xr,xf=-584,-582.5,-506.5;z0,zt=1143.5,1168.5
    cut=block(x0,y0-1,z0-1,xf+.001,yi,1170)
    floor=floor.cut(cut).clean();wrap=wrap.cut(cut).clean()
    shell[f'AIR_PROCESS_IN_FLOOR_{bed}_O']=floor
    shell[f'AIR_PROCESS_IN_WRAP_{bed}_O']=wrap
    return {
      f'C10_{bed}_W2_POCKET_ROOF':block(x0,y0,zt,-505,yi,zt+1.5),
      f'C10_{bed}_W2_POCKET_INBOARD_RETURN':block(xr,yi-1.5,z0,xf,yi,zt),
      f'C10_{bed}_W2_POCKET_REAR_RETURN':block(x0,y0,z0,xr,yi,zt),
      f'C10_{bed}_W2_POCKET_FRONT_RETURN':block(xf,y0,z0,-505,yi,zt),
    }

def outer_glands(cuts,svc):
    parts={};schedule=[]
    for bed in 'AB':
      for stage in 'LU':
        rows=[r for r in cuts if r['tag'].startswith(bed+'_'+stage) and r['layer']=='SKIN']
        yy=[float(r['y_mm']) for r in rows];zz=float(rows[0]['z_mm']);rr=[float(r['diameter_mm'])/2 for r in rows]
        ylo=min(y-r for y,r in zip(yy,rr))-12;yhi=max(y+r for y,r in zip(yy,rr))+12
        half=max(rr)+12
        tag=bed+'_'+stage;boot=svc[tag+'_W1__WET_BAY_COMMON_BOOT']
        membrane=block(-652.8,ylo,zz-half,-650.8,yhi,zz+half).cut(boot).clean()
        # A fitted, field-sealed flexible boot, with a service slit specified
        # in the interface drawing. The STEP represents the sealed condition.
        plate=block(-654.3,ylo,zz-half,-652.8,yhi,zz+half)
        # The steel retainer must slide over the curved insulation during its
        # 12 mm axial release. 3 mm over the skin radius clears that sweep;
        # the fitted soft membrane still seals at the actual insulation.
        for y,r in zip(yy,rr):plate=plate.cut(cq.Solid.makeCylinder(r+3,5,cq.Vector(-656,y,zz),cq.Vector(1,0,0)))
        centres=[(y,z) for y in (ylo+6,(ylo+yhi)/2,yhi-6) for z in (zz-half+6,zz+half-6)]
        for k,(y,z) in enumerate(centres):
            hole=cq.Solid.makeCylinder(2.25,6,cq.Vector(-656,y,z),cq.Vector(1,0,0))
            plate=plate.cut(hole);membrane=membrane.cut(hole)
            parts[f'C10_{tag}_GLAND_STUD_{k+1}']=cq.Solid.makeCylinder(2,9,cq.Vector(-659.8,y,z),cq.Vector(1,0,0))
            # AF7 nut envelope, threaded hole represented by nominal clearance.
            poly=cq.Wire.makePolygon([cq.Vector(-658.3,y+7/math.sqrt(3)*math.cos(a*math.pi/3),z+7/math.sqrt(3)*math.sin(a*math.pi/3)) for a in range(6)],close=True)
            nut=cq.Solid.extrudeLinear(poly,[],cq.Vector(4,0,0)).cut(cq.Solid.makeCylinder(2,5,cq.Vector(-658.5,y,z),cq.Vector(1,0,0)))
            parts[f'C10_{tag}_GLAND_NUT_{k+1}']=nut
            schedule.append({'panel':tag,'y_mm':y,'z_mm':z,'hole_diameter_mm':4.5,'stud':'M4 weld stud envelope; 9 mm projection'})
        parts[f'C10_{tag}_GLAND_MEMBRANE']=membrane
        for side,z0,z1 in [('LOW',zz-half,zz-.15),('HIGH',zz+.15,zz+half)]:
            parts[f'C10_{tag}_GLAND_RETAINER_{side}']=plate.intersect(block(-656,ylo-1,z0,-650,yhi+1,z1)).clean()
    return parts,schedule

def export_service():
    # HYD-S2 already contains the 204 H01 envelopes. Do not duplicate them.
    combine([('HYD_S2_AND_H01_SERVICE',HYD/'S2_SERVICE.step'),('HYD_OUTBOARD',HYD/'S2_OUTBOARD_SERVICE.step'),
             ('D04_SERVICE',D04/'cad/D04_LOCAL_SERVICE.step'),('D03_MOTION_SERVICE',WORK/'D03_MOTION_AND_SERVICE.step'),
             ('W2_CROWN',HYD/'W2_ADDITIONAL_INSULATION.step')],CAD/'C10_SERVICE_AND_THERMAL_REFERENCE.step')

def run():
    print('C10 start',flush=True)
    cuts=list(csv.DictReader((HX/'HOST_CUT_PROPOSAL.csv').open()))
    svc=named(HX/'H01_TOOL_AND_REMOVAL.step');build={}
    print('H01 service loaded',len(svc),flush=True)
    for state in ['S1','S2']:
        groups=cache_host(state);dampers=groups['DAMPERS']
        print('Host loaded',state,flush=True)
        if state=='S1':
            base=groups['SHELL'];shell=dict(base);modified={};added={}
            for n,s in list(shell.items()):
                b=bb(s)
                plane='SKIN' if abs(b[0]+650.8)<.01 and abs(b[3]+649.3)<.01 else None
                if plane:
                    s=s.cut(*[cq.Solid.makeCylinder(float(r['diameter_mm'])/2,4,cq.Vector(float(r['cut_from_x']),float(r['y_mm']),float(r['z_mm'])),cq.Vector(1,0,0)) for r in cuts if r['layer']==plane]).clean()
                    if abs(s.Volume()-base[n].Volume())>.001:shell[n]=s;modified[n]='H01 eight outer-skin openings'
            for bed in 'AB':
                print('Edit roof and pocket',bed,flush=True)
                top=f'AIR_TOP_SPLITTER_{bed}_O';inner=f'AIR_SIDE_IN_{bed}_O'
                shell[top],nodes,edges=top_deck(base[top]);shell[inner]=side_extension(base[inner],edges)
                modified[top]='constant-gauge roof; +60 mm over end of upper fin face'
                modified[inner]='extend inner cheek continuously to raised roof'
                added.update(thermal_pocket(shell,bed))
                for n in [f'AIR_PROCESS_IN_FLOOR_{bed}_O',f'AIR_PROCESS_IN_WRAP_{bed}_O']:modified[n]='sealed W2 insulation corner pocket'
            print('Build glands',flush=True)
            glands,holes=outer_glands(cuts,svc);added.update(glands)
            # End return meets the original Pin steel seat, without modifying D04.
            inherited_closures=[]
            for n,s in list(added.items()):
                if '_POCKET_' in n:
                    for dn,ds in dampers.items():
                        if overlap(bb(s),bb(ds)):
                            vol=s.intersect(ds).Volume()
                            if vol>.001:
                                print('Pocket seat junction',n,dn,round(vol,3),flush=True)
                                s=s.cut(ds)
                                if not s.Solids():
                                    inherited_closures.append({'part':n,'closed_by_retained_part':dn});break
                    if s.Solids():added[n]=s.clean()
                    else:del added[n]
            shell.update(added)
            print('Validate changed shell shapes',flush=True)
            report={}
            for n,s in shell.items():
                if n in added or n in modified:
                    assert s.Solids() and s.isValid(),n
                    report[n]={'operation':modified.get(n,'add'),'bbox':bb(s),'volume_mm3':s.Volume(),'solids':len(s.Solids())}
            save(shell,CAD/'C10_SHELL.step')
            save({n:s for n,s in shell.items() if n in added or n in modified},CAD/'C10_CHANGED_SHEET_AND_GLANDS.step')
            dump(E/'shell_changes.json',{'parent_shell_count':494,'shell_count':len(shell),'modified':modified,'added':list(added),'parts':report,'roof_centreline_XZ_mm':nodes,'glasholes':holes,'unchanged_A_post':True,'inherited_pocket_closures':inherited_closures})
            with (HERE/'GLAND_FIXINGS.csv').open('w',newline='') as f:
                wr=csv.DictWriter(f,fieldnames=list(holes[0]));wr.writeheader();wr.writerows(holes)
        save(dampers,WORK/f'D04_{state}.step',(.18,.55,.65))
        print('Composing',state,len(shell),len(dampers),flush=True)
        paths=[('SHELL',CAD/'C10_SHELL.step'),('DAMPERS',WORK/f'D04_{state}.step'),
               ('HEAT_EXCHANGERS',HX/'H01_FOUR_HX_INSTALLED.step'),('WATER_RACK',HYD/'S2_RACK.step'),
               ('FIRST_SPOOLS',HX/'H01_EIGHT_FIRST_SPOOLS.step')]
        combine(paths,CAD/f'C10_INSTALLED_{state}.step')
        build[state]={'source_D04_sha256':sha(D04/f'cad/D04_C09R1_INSTALLED_{state}.step'),'output_sha256':sha(CAD/f'C10_INSTALLED_{state}.step')}
        print('Exported',state,flush=True)
    export_service()
    dump(E/'build.json',build)
if __name__=='__main__':
    if '--service-only' in sys.argv:export_service()
    else:run()
