"""Coarse 3-D plenum pressure network. Stagnation-pressure mixing approximation.
Imposed uniform velocity at the selected P or R inlet. Repeated mirrored
collectors give a half-domain split at the middle of a uniform HX resistance.
No swirl, jet momentum transport, separation or fan curve in this model.
"""
from network import *
from scipy.sparse import coo_matrix,diags
from scipy.sparse.linalg import spsolve
from design import PORTS,THROAT
def solve(tag,flow,mix):
    nx,ny=8,14
    y=np.r_[-358.,np.linspace(-306,306,13),358.]/1000
    breaks=[144,190,535,665,845,THROAT]
    z=np.array([a+(b-a)*i/math.ceil((b-a)/55) for a,b in zip(breaks,breaks[1:]) for i in range(math.ceil((b-a)/55))]+[THROAT])/1000
    nz=len(z)-1;dx=.320/nx;dy=np.diff(y);dz=np.diff(z)
    A=[];B=[];R=[];exits=[]
    def ix(i,j,k):return (i*ny+j)*nz+k
    def edge(a,b,area,k):
        A.append(a);B.append(b);R.append(.5*rho*k/area**2)
    n=nx*ny*nz
    src=np.zeros(n)
    for i,j,k in itertools.product(range(nx),range(ny),range(nz)):
        a=ix(i,j,k)
        if i+1<nx:edge(a,ix(i+1,j,k),dy[j]*dz[k],mix*dx)
        if j+1<ny:edge(a,ix(i,j+1,k),dx*dz[k],mix*(dy[j]+dy[j+1])/2)
        if k+1<nz:edge(a,ix(i,j,k+1),dx*dy[j],mix*(dz[k]+dz[k+1])/2)
        if i==nx-1:
            py=max(0,min(y[j+1],.315)-max(y[j],-.315))
            zl,hh=PORTS[tag]
            pz=max(0,min(z[k+1],(zl+hh)/1000)-max(z[k],zl/1000))
            src[a]=py*pz/(.630*hh/1000)*flow/3600
        if k==nz-1 and 0<j<ny-1:
            exits.append((len(R),i,j-1))
            A.append(a);B.append(n)
            R.append(.5*(loss[i]+screens(diam[i],cd)+60)/(q0/12)**2)
    assert abs(src.sum()-flow/3600)<1e-9
    E=len(R);rows=np.repeat(np.arange(E),2);cols=np.stack((A,B),axis=1).flatten()
    incidence=coo_matrix((np.tile([1.,-1.],E),(rows,cols)),shape=(E,n+1)).tocsr()[:,:n]
    rr=np.array(R);p=np.full(n,105.*(flow/4870)**2)
    # Regularize very small gradients. Exact inversion to better than 0.001 Pa.
    reg=1e-4
    def calc(p):
        h=incidence@p;v=h/(rr**.5*(h*h+reg**2)**.25)
        return h,v,incidence.T@v-src
    for iteration in range(100):
        h,v,res=calc(p)
        if max(abs(res))<2e-8:break
        deriv=(.5*h*h+reg**2)/(rr**.5*(h*h+reg**2)**1.25)
        delta=spsolve((incidence.T@diags(deriv)@incidence).tocsc(),-res)
        step=1.
        while step>1e-5 and np.linalg.norm(calc(p+step*delta)[2])>=np.linalg.norm(res):step/=2
        p+=step*delta
    assert max(abs(res))<2e-8,(iteration,max(abs(res)))
    field=np.zeros((8,12))
    for k,i,j in exits:field[i,j]=v[k]*96/(flow/3600)
    return dict(port=tag,flow_m3h=flow,mixing_loss_per_m=mix,max_mass_residual_m3s=float(max(abs(res))),mean_inlet_dp_pair_Pa=round(2*p@src/src.sum(),2),min_mean=round(field.min(),4),max_mean=round(field.max(),4),CV_pct=round(field.std()*100,3),field=field.round(5).tolist())
if __name__=='__main__':
    import math
    rows=[solve(tag,flow,k) for tag,flow in [('P',4870),('R',4870),('R',2435)] for k in (1.,4.,10.)]
    (OUT/'selector_results.json').write_text(json.dumps(rows,indent=2))
    for r in rows:print({k:v for k,v in r.items() if k!='field'})
