from common import *
for r,s in baseline(groups={'SHELL'}):
    if not r['name'].startswith('P_FOOT_'):continue
    holes=[]
    for e in s.Edges():
        if e.geomType()=='CIRCLE':
            c=e._geomAdaptor().Circle();p=c.Location()
            holes.append([round(p.X(),3),round(p.Y(),3),round(p.Z(),3),round(c.Radius(),3)])
    print(r['name'],holes,flush=True)
