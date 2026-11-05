"""C04 design dimensions in mm. u measures outward from each HX frame."""
from math import hypot, sqrt
N=8
W,H=612.,1000.
BAND=H/N
DEPTH=320.
SLOPE=DEPTH/H
LAND,BLEND=28.,32.
Z0=1204.
THROAT=Z0-80
T=1.5
FOOT=LAND+BLEND/2+(Z0-THROAT)*SLOPE
OUTER=FOOT+DEPTH
PORTS={'P':(190.,345.), 'R':(665.,180.)}
CENTRES={'A':-434.4,'B':405.6}

def guide(i):
    """Polyline for a guide, from core seat to open throat."""
    z=Z0+i*BAND
    points=[(0.,z),(LAND,z)]
    for j in range(1,17):
        t=j/16
        points.append((LAND+BLEND*t,z-BLEND*t*t/(2*SLOPE)))
    return points+[(FOOT+i*DEPTH/N,THROAT)]

def path_length(i):
    p=guide(i+.5)
    return sum(hypot(u-v,z-w) for (u,z),(v,w) in zip(p,p[1:]))
