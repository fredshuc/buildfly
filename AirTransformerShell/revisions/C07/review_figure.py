"""Make the review figure from the C07 rod register and CAD construction dimensions."""
from pathlib import Path
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE=Path(__file__).resolve().parent
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.spines.top":False,"axes.spines.right":False})
ink="#16354a"; steel="#54869a"; green="#20836a"; amber="#bd6a28"; gray="#6c7984"
def rect(ax,x,y,w,h,**kw):
    p=Rectangle((x,y),w,h,**kw);ax.add_patch(p);return p

def main():
    fig,(a,b)=plt.subplots(1,2,figsize=(11,7),gridspec_kw={"width_ratios":[1.03,1.05]})
    fig.subplots_adjust(left=.08,right=.965,bottom=.24,top=.84,wspace=.22)
    fig.suptitle("C07   |   The two seal carriers clamp to one another across the exchanger",x=.065,ha="left",fontsize=17,fontweight="bold",color=ink)
    fig.text(.065,.895,"Nominal geometry in mm. Bed A coordinates are relative to its centre along Y.",color=gray)
    a.set_title("Clamp and service-guide centres",loc="left",color=ink,fontweight="bold")
    for w,h,co in ((770,1156,steel),(650,1036,steel),(644,1032,green),(622,1008,green)):
        rect(a,-w/2,1704-h/2,w,h,facecolor="none",edgecolor=co,linewidth=1.3)
    with (HERE/"tie_rods.csv").open() as f:
        rods=[r for r in csv.DictReader(f) if r["bed"]=="A"]
    a.scatter([float(r["global_y_mm"])+434.4 for r in rods],[float(r["global_z_mm"]) for r in rods],s=39,c=amber,marker="o",label="14 front-to-rear tie rods")
    for z in (1182,2071.97):
        a.scatter([-340,340],[z,z],s=38,c=ink,marker="s",label="4 service guides" if z==1182 else None)
    a.set(xlim=(-435,435),ylim=(1090,2320),xlabel="Y relative to bed centre (mm)",ylabel="Global Z (mm)",aspect="equal")
    a.grid(alpha=.14);a.legend(frameon=False,loc="upper center",bbox_to_anchor=(.5,-.16),ncol=2,fontsize=8)
    b.set_title("Clamp reaction along X",loc="left",color=ink,fontweight="bold")
    b.set(xlim=(205,545),ylim=(0,1));b.set_yticks([]);b.set_xlabel("Global X (mm)");b.set_xticks([228,265,375,485,522])
    rect(b,265,.25,220,.33,facecolor="#deebef",edgecolor=steel,linewidth=1.3)
    b.text(375,.415,"M101 C05\n220 mm",ha="center",va="center",color=ink,fontsize=12)
    for x0,gx,mx in ((238.8,260.8,231),(489.2,485,511.2)):
        rect(b,x0,.21,22,.42,facecolor=steel,edgecolor=ink)
        rect(b,gx,.25,4.2,.33,facecolor=green,edgecolor=green)
        rect(b,mx,.70,7.3,.09,facecolor=amber,edgecolor=amber)
    for x0 in (238.8,489.2):
        rect(b,x0,.58,22,.22,facecolor=steel,edgecolor=ink)
    b.plot([228,522],[.746,.746],color=amber,lw=3)
    b.annotate("",xy=(263,.655),xytext=(228,.655),arrowprops={"arrowstyle":"->","color":amber,"lw":2.4})
    b.annotate("",xy=(487,.655),xytext=(522,.655),arrowprops={"arrowstyle":"->","color":amber,"lw":2.4})
    b.text(375,.84,"Opposed nuts tension the tie rod",ha="center",color=amber,fontweight="bold")
    b.text(375,.16,"4.2 mm gasket thickness at the metal stops",ha="center",color=green)
    b.text(375,.085,"Release both carriers outward by 6 mm",ha="center",color=ink)
    b.grid(axis="x",alpha=.14)
    fig.text(.065,.037,"Service: guide nuts seat the two rings against fixed shoulders before the eleven upper/side rods park toward -X. Three lower rods stay seated.",fontsize=9,color=ink)
    fig.savefig(HERE/"C07_SEAL_AND_SERVICE.png",dpi=175,facecolor="white")
def air_section():
    import sys
    sys.path.insert(0,str(HERE.parent/"C04"))
    from design import guide,FOOT,OUTER,THROAT,Z0,BAND,PORTS
    from matplotlib.patches import Polygon
    fig,ax=plt.subplots(figsize=(8.0,8.2))
    fig.subplots_adjust(left=.115,right=.95,bottom=.13,top=.86)
    fig.suptitle("C07   |   Air paths across one vertical bed",x=.08,ha="left",fontsize=18,fontweight="bold",color=ink)
    fig.text(.082,.905,"Section through bed centre. Both beds use the same guide profile.",color=gray)
    for x,sign in ((265,-1),(485,1)):
        xf=lambda u:x+sign*u
        throat_inner,throat_outer=FOOT-2,OUTER+2
        rect(ax,min(xf(throat_inner),xf(throat_outer)),144,throat_outer-throat_inner,THROAT-144,facecolor="#edf2f4",edgecolor=steel)
        for i in range(8):
            def trace(j):
                pts=list(guide(j));pts[0]=(5,pts[0][1])
                return [(xf(u),z) for u,z in pts]
            ax.add_patch(Polygon(trace(i)+trace(i+1)[::-1],closed=True,facecolor=("#e1eef0" if i%2 else "#c4e0e2"),edgecolor=steel,lw=.85))
        for mode,col in (("P","#1c6b92"),("R","#c26f2b")):
            z,h=PORTS[mode]
            ax.plot([xf(throat_outer)]*2,[z,z+h],lw=4.5,color=col,solid_capstyle="butt")
            ax.text(xf(throat_outer+38),z+h/2,mode,ha="center",va="center",weight="bold",color=col)
        ax.plot([xf(FOOT),xf(OUTER)],[THROAT,THROAT],linestyle=":",lw=1,color=ink)
    rect(ax,265,Z0,220,1000,facecolor="#eddac2",edgecolor=amber)
    ax.text(375,Z0+500,"M101  •  active face 612 × 1000",ha="center",va="center",rotation=90,color="#70471e",fontsize=10)
    ax.annotate("Eight 125 mm bands",xy=(165,1815),xytext=(-320,2230),ha="left",color=ink,arrowprops={"arrowstyle":"->","color":ink})
    ax.annotate("Common selector throat",xy=(55,THROAT),xytext=(-310,970),ha="left",color=ink,fontsize=8,arrowprops={"arrowstyle":"->","color":ink})
    ax.set(xlim=(-358,1104),ylim=(45,2360),aspect="equal",xlabel="Global X (mm)",ylabel="Global Z (mm)")
    ax.grid(alpha=.12)
    fig.text(.082,.045,"P  Process     R  Regeneration     •     Net openings 630 × 345 and 630 × 180 mm",color=ink)
    fig.text(.082,.012,"The section establishes geometric coverage. Face velocity and leakage require the G0/G1 tests.",color=gray,fontsize=9)
    fig.savefig(HERE/"C07_AIR_SECTION.png",dpi=160,facecolor="white")
if __name__=="__main__":
    main()
    air_section()
