"""Versioned inputs, cached CAD readback, component and drawing definitions."""
from geometry_io import *
import csv,math
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
BASE=HERE.parent/'C10'
WS=HERE.parents[3]
BASE_HASH={'S1':'55f43f07d34ba2ec186b634673f06bc3efdf6dfdc911c11433e07fd720a67f09',
           'S2':'5e547cd158b5c6d3692a940d672a6aa8a1ae074655237abf4ff09e1fbfe0ecff'}

def bounds(s):
    b=Bnd_Box();BRepBndLib.Add_s(s.wrapped,b,False);return list(b.Get())

def table(path,rows):
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def baseline(state='S1',groups=None):
    src=BASE/f'cad/C10_INSTALLED_{state}.step'
    assert sha(src)==BASE_HASH[state],'Unrecognised C10 baseline'
    target=WORK/f'baseline_{state}'
    # Optional read-only development cache; final isolated rebuild uses STEP.
    hint=os.environ.get('C11_C10_CACHE')
    if hint and state=='S1':target=Path(hint)
    index=target/'index.json'
    if not index.exists():
        target.mkdir(exist_ok=True);rows=[]
        for i,(p,s) in enumerate(leaves(src)):
            group=next(g for g in ['SHELL','DAMPERS','HEAT_EXCHANGERS','WATER_RACK','FIRST_SPOOLS'] if g in p.split('/'))
            filename=f'{i}.brep';s.exportBrep(str(target/filename))
            rows.append({'name':p.split('/')[-1],'path':p,'group':group,'file':filename,'bbox':bounds(s)})
        dump(index,{'sha256':sha(src),'parts':rows})
    data=json.loads(index.read_text(encoding='utf-8'));assert data['sha256']==BASE_HASH[state]
    return [(r,cq.Shape.importBrep(str(target/r['file']))) for r in data['parts'] if groups is None or r['group'] in groups]

def box(*b):return block(*b)
def cyl(r,length,origin,direction):return cq.Solid.makeCylinder(r,length,cq.Vector(*origin),cq.Vector(*direction))
def annulus_x(x0,x1,y,z,ro,ri):return cyl(ro,x1-x0,(x0,y,z),(1,0,0)).cut(cyl(ri,x1-x0+2,(x0-1,y,z),(1,0,0)))
def ring_xy(x0,y0,x1,y1,z0,z1,width):
    return box(x0,y0,z0,x1,y1,z1).cut(box(x0+width,y0+width,z0-1,x1-width,y1-width,z1+1))
def hexnut_x(x0,y,z,af,height,bore):
    wire=cq.Wire.makePolygon([cq.Vector(x0,y+af/math.sqrt(3)*math.cos(k*math.pi/3),z+af/math.sqrt(3)*math.sin(k*math.pi/3)) for k in range(6)],close=True)
    s=cq.Solid.extrudeLinear(wire,[],cq.Vector(height,0,0))
    return s.cut(cyl(bore/2,height+2,(x0-1,y,z),(1,0,0))) if bore else s

class Design:
    def __init__(self,shell):
        self.parts=dict(shell);self.before=dict(shell);self.change={};self.material={};self.drawings=[];self.connections=[];self.required_contacts=[];self.interfaces=[]
    def add(self,name,shape,material,reason,drawing=None):
        assert name not in self.parts,name
        assert shape.Solids() and shape.isValid(),name
        self.parts[name]=shape;self.change[name]=reason;self.material[name]=material
        if drawing:self.drawings.append(dict(part=name,**drawing))
    def replace(self,name,shape,material,reason):
        assert name in self.before,name
        assert shape.Solids() and shape.isValid(),name
        self.parts[name]=shape;self.change[name]=reason;self.material[name]=material
    def remove(self,name,reason):
        assert name in self.before,name
        del self.parts[name];self.change[name]='SUPERSEDED: '+reason
    def contact(self,a,b,purpose):self.required_contacts.append({'a':a,'b':b,'purpose':purpose})

def screen_parts(left,right,skip_same=False):
    hits=[];count=0;rb={n:bounds(s) for n,s in right.items()}
    for n,s in left.items():
        a=bounds(s)
        for k,t in right.items():
            if skip_same and k==n:continue
            if overlap(a,rb[k],-1e-6):
                count+=1;v=s.intersect(t).Volume()
                if v>.001:hits.append([n,k,v])
    return {'candidate_pairs':count,'hits':hits}
