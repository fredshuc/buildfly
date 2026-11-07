"""Exact common volume, exploiting validated disjoint trap-spool segments."""
from common import bounds,overlap

def common_volume(a,b,name_a='',name_b=''):
    if name_a.endswith('_COND_TRAP_PIPE'):
        parts=a.Solids();assert len(parts)==15
        bb=bounds(b)
        return sum(s.intersect(b).Volume() for s in parts if overlap(bounds(s),bb,-1e-5))
    if name_b.endswith('_COND_TRAP_PIPE'):
        return common_volume(b,a,name_b,name_a)
    return a.intersect(b).Volume()
