"""Read the export and measure four pipe clearances and nominal split-gland contact."""
from pathlib import Path
import sys, json
from xcaf_leaves import leaves
from relieve import targets

def plane_faces(shape, x):
    return [f for f in shape.Faces()
            if all(abs(a-x)<1e-4 for a in (f.BoundingBox().xmin, f.BoundingBox().xmax))]

def inspect(path):
    parts = leaves(path)
    def one(fragment):
        found = [s for k,s in parts if fragment in k.split('/')]
        assert len(found)==1,(fragment,len(found))
        return found[0]
    report = {}
    for bed in 'AB':
        pipe, = [s for k,s in parts if bed+'_UPPER' in k.split('/') and 'W2_D35_END_PIPE' in k.split('/')]
        for name in targets:
            if '_'+bed+'_' not in name:
                continue
            shape=one(name)
            distance=shape.distance(pipe)
            assert distance>=2.999, (name,distance)
            report[name]={'pipe_clearance_mm':round(distance,5)}
            if 'STATIC_GASKET' in name:
                contact={}
                for half in ('LOW','HIGH'):
                    gland=one(f'C09_SPLIT_GLAND_{bed}_UPPER_W2_{half}')
                    contact[half]=round(sum(a.intersect(b).Area() for a in plane_faces(shape,-501.5)
                                            for b in plane_faces(gland,-501.5)),5)
                report[name]['nominal_contact_mm2_by_gland_half']=contact
    return report

if __name__=='__main__':
    Path(sys.argv[2]).write_text(json.dumps(inspect(sys.argv[1]),indent=2))
